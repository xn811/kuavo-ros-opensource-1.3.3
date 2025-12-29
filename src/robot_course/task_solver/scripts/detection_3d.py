#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D检测节点
根据YOLO检测结果和深度图，计算物体的3D位置
使用TF变换计算物体相对于base_link和odom的3D位置
"""

import rospy
import json
import math
import numpy as np
import cv2
from collections import deque
from std_msgs.msg import String
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray
from cv_bridge import CvBridge
import tf2_ros
import tf2_geometry_msgs
from dynamic_reconfigure.server import Server
from task_solver.cfg import GraspControllerConfig


class Detection3D:
    def __init__(self):
        rospy.init_node('detection_3d', anonymous=True)
        
        # 加载参数
        self.camera_frame = rospy.get_param('~camera_frame', 'camera_color_optical_frame')
        self.base_frame = rospy.get_param('~base_frame', 'base_link')
        self.odom_frame = rospy.get_param('~odom_frame', 'odom')
        
        # 相机内参
        self.fx = self.fy = self.cx = self.cy = None
        self.camera_info_received = False
        
        # TF2
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        # 图像数据
        self.bridge = CvBridge()
        self.cv_depth_image = None
        self.cv_color_image = None
        self.detected_objects_3d = []
        self.detected_objects_3d_odom = []
        
        # 订阅话题
        self.detection_sub = rospy.Subscriber('/yolo/detections', String, self.detection_callback, queue_size=10)
        self.depth_sub = rospy.Subscriber('/camera/depth/image_rect_raw', Image, self.depth_callback, queue_size=1)
        self.camera_info_sub = rospy.Subscriber('/camera/color/camera_info', CameraInfo, self.camera_info_callback, queue_size=1)
        self.color_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.color_callback, queue_size=1)
        
        # 发布话题
        self.detection_3d_pub = rospy.Publisher('/yolo/detections_3d', String, queue_size=10)
        self.detection_3d_odom_pub = rospy.Publisher('/yolo/detections_3d_odom', String, queue_size=10)
        self.marker_pub = rospy.Publisher('/yolo/markers', MarkerArray, queue_size=10)
        self.marker_odom_pub = rospy.Publisher('/yolo/markers_odom', MarkerArray, queue_size=10)
        self.vis_image_pub = rospy.Publisher('/yolo/detection_image', Image, queue_size=1)
        
        # 颜色映射
        self.class_colors = {
            'cup': (0.0, 1.0, 0.0, 0.8),
            'plate': (0.0, 0.0, 1.0, 0.8),
            'scissors': (1.0, 0.0, 0.0, 0.8),
        }
        self.class_colors_bgr = {
            'cup': (0, 255, 0),
            'plate': (255, 0, 0),
            'scissors': (0, 0, 255),
        }
        
        # 物体高度补偿 (检测点到底部的高度差)
        # 因为深度相机看到的是物体表面，需要补偿到底部
        self.object_height_offset = {
            'cup': -0.08,       # 杯子高约8cm，检测点在中上部
            'plate': -0.02,     # 盘子很薄
            'scissors': -0.02,  # 剪刀很薄
        }
        
        # 滤波参数
        self.window_size = rospy.get_param('~window_size', 5)
        self.position_history = {}
        
        # 物体追踪 (为每个物体分配稳定ID) - 使用odom坐标系
        self.tracked_objects = {}  # {track_id: {'class': str, 'pos_odom': deque, 'last_seen': time}}
        self.archived_objects = {}  # 消失的物体存档，用于重新匹配
        self.next_track_id = 0
        self.track_distance_threshold = 0.15  # 15cm内认为是同一物体
        self.track_timeout = 2.0  # 2秒未见则标记为inactive
        self.archive_timeout = 30.0  # 30秒后彻底删除存档
        
        # 桌面高度过滤
        table_height_param = rospy.get_param('~table_height', 'None')
        self.table_height = None if table_height_param in ['None', None] else float(table_height_param)
        self.table_height_enabled = self.table_height is not None
        self.table_height_tolerance = rospy.get_param('~table_height_tolerance', 0.15)
        
        # 动态参数服务器
        self.dyn_srv = Server(GraspControllerConfig, self.dynamic_reconfigure_callback)
        
        rospy.loginfo(f"Detection3D initialized, window_size={self.window_size}")

    def dynamic_reconfigure_callback(self, config, level):
        self.window_size = config.depth_sample_radius
        self.table_height_enabled = config.table_height_enabled
        self.table_height = config.table_height if self.table_height_enabled else None
        self.table_height_tolerance = config.table_height_tolerance
        rospy.loginfo(f"Config updated: window={self.window_size}, table={self.table_height}±{self.table_height_tolerance}")
        return config

    def camera_info_callback(self, msg):
        if not self.camera_info_received:
            self.fx, self.fy = msg.K[0], msg.K[4]
            self.cx, self.cy = msg.K[2], msg.K[5]
            self.camera_info_received = True
            rospy.loginfo(f"Camera: fx={self.fx:.1f}, fy={self.fy:.1f}, cx={self.cx:.1f}, cy={self.cy:.1f}")
    
    def depth_callback(self, msg):
        try:
            if msg.encoding == "16UC1":
                self.cv_depth_image = self.bridge.imgmsg_to_cv2(msg, "16UC1")
            elif msg.encoding == "32FC1":
                self.cv_depth_image = (self.bridge.imgmsg_to_cv2(msg, "32FC1") * 1000).astype(np.uint16)
            else:
                self.cv_depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        except Exception as e:
            rospy.logerr(f"Depth convert failed: {e}")
    
    def color_callback(self, msg):
        try:
            self.cv_color_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logerr(f"Color convert failed: {e}")
    
    def detection_callback(self, msg):
        try:
            detections = json.loads(msg.data)
            if detections:
                self.calculate_3d_positions(detections)
                self.publish_detection_image(detections)
        except json.JSONDecodeError as e:
            rospy.logerr(f"JSON parse failed: {e}")

    def get_filtered_position(self, track_key, new_pos):
        """
        位置滤波 - 使用track_key区分不同物体
        track_key: 可以是 "class_name_x_y" 格式，用于区分同类不同物体
        """
        if track_key not in self.position_history:
            self.position_history[track_key] = deque(maxlen=self.window_size)
        
        history = self.position_history[track_key]
        
        # 异常值检测：如果新位置与历史平均差距太大，可能是跳变
        if len(history) >= 2:
            avg_x = np.mean([p['x'] for p in history])
            avg_y = np.mean([p['y'] for p in history])
            avg_z = np.mean([p['z'] for p in history])
            dist = math.sqrt((new_pos['x']-avg_x)**2 + (new_pos['y']-avg_y)**2 + (new_pos['z']-avg_z)**2)
            
            # 如果跳变超过30cm，可能是误检，不加入历史
            if dist > 0.3:
                rospy.logwarn_throttle(2.0, f"位置跳变 {track_key}: {dist*100:.1f}cm，忽略此帧")
                # 返回历史平均值
                return {'x': avg_x, 'y': avg_y, 'z': avg_z}
        
        history.append(new_pos)
        
        if len(history) < 2:
            return new_pos
        
        return {
            'x': np.mean([p['x'] for p in history]),
            'y': np.mean([p['y'] for p in history]),
            'z': np.mean([p['z'] for p in history])
        }
    
    def update_tracking(self, class_name, position_odom):
        """
        更新物体追踪，返回稳定的track_id
        使用odom坐标系位置进行匹配，确保机器人移动后ID仍然稳定
        """
        current_time = rospy.get_time()
        pos_tuple = (position_odom['x'], position_odom['y'], position_odom['z'])
        
        # 1. 清理超时的活跃追踪 -> 移到存档
        for tid in list(self.tracked_objects.keys()):
            obj = self.tracked_objects[tid]
            if current_time - obj['last_seen'] > self.track_timeout:
                # 存档而不是删除
                if len(obj['pos_odom']) > 0:
                    avg_pos = (
                        np.mean([p[0] for p in obj['pos_odom']]),
                        np.mean([p[1] for p in obj['pos_odom']]),
                        np.mean([p[2] for p in obj['pos_odom']])
                    )
                    self.archived_objects[tid] = {
                        'class': obj['class'],
                        'last_pos_odom': avg_pos,
                        'archived_time': current_time
                    }
                del self.tracked_objects[tid]
        
        # 2. 清理过期存档
        for tid in list(self.archived_objects.keys()):
            if current_time - self.archived_objects[tid]['archived_time'] > self.archive_timeout:
                del self.archived_objects[tid]
        
        # 3. 先在活跃追踪中找匹配
        best_match_id = None
        min_dist = self.track_distance_threshold
        
        for tid, obj in self.tracked_objects.items():
            if obj['class'] != class_name:
                continue
            if len(obj['pos_odom']) > 0:
                avg_pos = (
                    np.mean([p[0] for p in obj['pos_odom']]),
                    np.mean([p[1] for p in obj['pos_odom']]),
                    np.mean([p[2] for p in obj['pos_odom']])
                )
                dist = math.sqrt(sum((a-b)**2 for a, b in zip(pos_tuple, avg_pos)))
                if dist < min_dist:
                    min_dist = dist
                    best_match_id = tid
        
        if best_match_id is not None:
            # 更新已有追踪
            self.tracked_objects[best_match_id]['pos_odom'].append(pos_tuple)
            self.tracked_objects[best_match_id]['last_seen'] = current_time
            return best_match_id
        
        # 4. 在存档中找匹配 (恢复消失的物体)
        for tid, archived in self.archived_objects.items():
            if archived['class'] != class_name:
                continue
            dist = math.sqrt(sum((a-b)**2 for a, b in zip(pos_tuple, archived['last_pos_odom'])))
            if dist < min_dist:
                min_dist = dist
                best_match_id = tid
        
        if best_match_id is not None:
            # 从存档恢复
            rospy.loginfo(f"恢复追踪 ID:{best_match_id} ({class_name})")
            del self.archived_objects[best_match_id]
            self.tracked_objects[best_match_id] = {
                'class': class_name,
                'pos_odom': deque([pos_tuple], maxlen=self.window_size),
                'last_seen': current_time
            }
            return best_match_id
        
        # 5. 创建新追踪
        new_id = self.next_track_id
        self.next_track_id += 1
        self.tracked_objects[new_id] = {
            'class': class_name,
            'pos_odom': deque([pos_tuple], maxlen=self.window_size),
            'last_seen': current_time
        }
        rospy.loginfo(f"新建追踪 ID:{new_id} ({class_name})")
        return new_id
    
    def get_sorted_objects(self, objects_3d):
        """按距离排序，返回带序号的物体列表"""
        # 按类别分组
        by_class = {}
        for obj in objects_3d:
            cls = obj['class_name']
            if cls not in by_class:
                by_class[cls] = []
            by_class[cls].append(obj)
        
        # 每个类别内按距离排序
        result = []
        for cls, objs in by_class.items():
            sorted_objs = sorted(objs, key=lambda x: x['distance'])
            for idx, obj in enumerate(sorted_objs):
                obj['class_index'] = idx  # 类内序号 (0, 1, 2...)
            result.extend(sorted_objs)
        
        return result

    def get_robust_depth_and_center(self, bbox):
        """
        从bbox区域获取稳健的深度值和采样中心点
        改进：使用bbox中心区域而不是下半部分，避免采到桌面
        """
        if self.cv_depth_image is None:
            return None, None, None
        
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        h, w = self.cv_depth_image.shape
        x1, x2 = max(0, x1), min(w, x2)
        y1, y2 = max(0, y1), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return None, None, None
        
        # 使用bbox中心区域 (缩小到60%范围，避免边缘和桌面)
        bbox_w = x2 - x1
        bbox_h = y2 - y1
        margin_x = int(bbox_w * 0.2)
        margin_y = int(bbox_h * 0.2)
        
        roi_x1 = x1 + margin_x
        roi_x2 = x2 - margin_x
        roi_y1 = y1 + margin_y
        roi_y2 = y2 - margin_y
        
        if roi_x2 <= roi_x1 or roi_y2 <= roi_y1:
            roi_x1, roi_x2 = x1, x2
            roi_y1, roi_y2 = y1, y2
        
        roi = self.cv_depth_image[roi_y1:roi_y2, roi_x1:roi_x2].astype(np.float32) / 1000.0
        
        if roi.size == 0:
            return None, None, None
        
        valid_mask = (roi > 0.1) & (roi < 5.0)
        valid_depths = roi[valid_mask]
        
        if len(valid_depths) < 10:
            # 回退到中心点
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if 0 <= cy < h and 0 <= cx < w:
                d = float(self.cv_depth_image[cy, cx]) / 1000.0
                if 0.1 < d < 5.0:
                    return d, cx, cy
            return None, None, None
        
        # 使用直方图找最近的峰值（物体表面，而不是背景）
        hist, bin_edges = np.histogram(valid_depths, bins=50)
        
        # 找最近的显著峰值（深度最小的峰）
        peak_idx = None
        for i in range(len(hist)):
            if hist[i] > len(valid_depths) * 0.05:  # 至少5%的点
                peak_idx = i
                break
        
        if peak_idx is None:
            peak_idx = np.argmax(hist)
        
        peak_depth = (bin_edges[peak_idx] + bin_edges[peak_idx + 1]) / 2
        
        depth_tolerance = 0.05
        near_peak_mask = (roi > peak_depth - depth_tolerance) & (roi < peak_depth + depth_tolerance) & valid_mask
        
        if np.sum(near_peak_mask) < 5:
            return float(np.median(valid_depths)), (x1 + x2) // 2, (y1 + y2) // 2
        
        ys, xs = np.where(near_peak_mask)
        if len(xs) > 0:
            center_x = int(np.mean(xs)) + roi_x1
            center_y = int(np.mean(ys)) + roi_y1
            robust_depth = float(np.median(roi[near_peak_mask]))
            return robust_depth, center_x, center_y
        
        return float(np.median(valid_depths)), (x1 + x2) // 2, (y1 + y2) // 2

    def is_on_table(self, z_odom):
        if not self.table_height_enabled or self.table_height is None:
            return True
        return (self.table_height - self.table_height_tolerance) <= z_odom <= (self.table_height + self.table_height_tolerance)
    
    def calculate_3d_positions(self, detections):
        if self.cv_depth_image is None or not self.camera_info_received:
            return
        
        self.detected_objects_3d.clear()
        self.detected_objects_3d_odom.clear()
        
        for det in detections:
            bbox = det['bbox']
            depth, x_sample, y_sample = self.get_robust_depth_and_center(bbox)
            
            if depth is None or depth <= 0.1 or depth > 5.0:
                continue
            
            X_cam = depth * (x_sample - self.cx) / self.fx
            Y_cam = depth * (y_sample - self.cy) / self.fy
            Z_cam = depth
            
            pose_cam = PoseStamped()
            pose_cam.header.frame_id = self.camera_frame
            pose_cam.header.stamp = rospy.Time(0)
            pose_cam.pose.position.x = X_cam
            pose_cam.pose.position.y = Y_cam
            pose_cam.pose.position.z = Z_cam
            pose_cam.pose.orientation.w = 1.0
            
            try:
                transform = self.tf_buffer.lookup_transform(self.base_frame, self.camera_frame, rospy.Time(0), rospy.Duration(0.5))
                pose_base = tf2_geometry_msgs.do_transform_pose(pose_cam, transform)
                
                raw_pos = {
                    'x': pose_base.pose.position.x,
                    'y': pose_base.pose.position.y,
                    'z': pose_base.pose.position.z
                }
                
                # 应用物体高度补偿
                z_offset = self.object_height_offset.get(det['class_name'], 0)
                raw_pos['z'] += z_offset
                
                # 使用bbox中心位置作为track_key，区分同类不同物体
                bbox_cx = (bbox[0] + bbox[2]) / 2
                bbox_cy = (bbox[1] + bbox[3]) / 2
                track_key = f"{det['class_name']}_{int(bbox_cx/50)}_{int(bbox_cy/50)}"
                filtered_pos = self.get_filtered_position(track_key, raw_pos)

                object_3d = {
                    'class_name': det['class_name'],
                    'confidence': float(det['confidence']),
                    'position': {k: float(v) for k, v in filtered_pos.items()},
                    'position_camera': {'x': float(X_cam), 'y': float(Y_cam), 'z': float(Z_cam)},
                    'distance': float(math.sqrt(filtered_pos['x']**2 + filtered_pos['y']**2 + filtered_pos['z']**2)),
                    'bbox': [float(b) for b in det['bbox']],
                    'depth_mm': float(depth * 1000),
                    'sample_point': [x_sample, y_sample],
                    'track_id': -1  # 稍后在odom坐标系中更新
                }
                self.detected_objects_3d.append(object_3d)
                
                try:
                    transform_odom = self.tf_buffer.lookup_transform(self.odom_frame, self.base_frame, rospy.Time(0), rospy.Duration(0.5))
                    pose_odom = tf2_geometry_msgs.do_transform_pose(pose_base, transform_odom)
                    
                    z_odom = pose_odom.pose.position.z
                    if not self.is_on_table(z_odom):
                        self.detected_objects_3d.remove(object_3d)
                        continue
                    
                    # 使用odom坐标更新追踪ID
                    pos_odom = {
                        'x': float(pose_odom.pose.position.x),
                        'y': float(pose_odom.pose.position.y),
                        'z': float(z_odom)
                    }
                    track_id = self.update_tracking(det['class_name'], pos_odom)
                    object_3d['track_id'] = track_id
                    
                    object_3d_odom = object_3d.copy()
                    object_3d_odom['position'] = pos_odom
                    self.detected_objects_3d_odom.append(object_3d_odom)
                except Exception as e:
                    rospy.logwarn_throttle(5.0, f"TF to odom failed: {e}")
            except Exception as e:
                rospy.logwarn_throttle(5.0, f"TF to base_link failed: {e}")
        
        # 按距离排序并添加类内序号
        self.detected_objects_3d = self.get_sorted_objects(self.detected_objects_3d)
        self.detected_objects_3d_odom = self.get_sorted_objects(self.detected_objects_3d_odom)
        
        if self.detected_objects_3d:
            self.detection_3d_pub.publish(String(data=json.dumps(self.detected_objects_3d)))
            self.publish_markers(self.detected_objects_3d, self.base_frame, self.marker_pub)
        if self.detected_objects_3d_odom:
            self.detection_3d_odom_pub.publish(String(data=json.dumps(self.detected_objects_3d_odom)))
            self.publish_markers(self.detected_objects_3d_odom, self.odom_frame, self.marker_odom_pub)

    def publish_markers(self, objects_3d, frame_id, publisher):
        marker_array = MarkerArray()
        
        delete_marker = Marker()
        delete_marker.header.frame_id = frame_id
        delete_marker.header.stamp = rospy.Time.now()
        delete_marker.action = Marker.DELETEALL
        marker_array.markers.append(delete_marker)
        
        for i, obj in enumerate(objects_3d):
            sphere = Marker()
            sphere.header.frame_id = frame_id
            sphere.header.stamp = rospy.Time.now()
            sphere.ns = "spheres"
            sphere.id = i * 2
            sphere.type = Marker.SPHERE
            sphere.action = Marker.ADD
            sphere.pose.position.x = obj['position']['x']
            sphere.pose.position.y = obj['position']['y']
            sphere.pose.position.z = obj['position']['z']
            sphere.pose.orientation.w = 1.0
            sphere.scale.x = sphere.scale.y = sphere.scale.z = 0.08
            color = self.class_colors.get(obj['class_name'], (1.0, 1.0, 0.0, 0.8))
            sphere.color.r, sphere.color.g, sphere.color.b, sphere.color.a = color
            sphere.lifetime = rospy.Duration(0.5)
            marker_array.markers.append(sphere)
            
            text = Marker()
            text.header.frame_id = frame_id
            text.header.stamp = rospy.Time.now()
            text.ns = "labels"
            text.id = i * 2 + 1
            text.type = Marker.TEXT_VIEW_FACING
            text.action = Marker.ADD
            text.pose.position.x = obj['position']['x']
            text.pose.position.y = obj['position']['y']
            text.pose.position.z = obj['position']['z'] + 0.15
            text.pose.orientation.w = 1.0
            text.scale.z = 0.08
            text.color.r = text.color.g = text.color.b = text.color.a = 1.0
            text.text = f"{obj['class_name']}#{obj.get('class_index', 0)} [ID:{obj.get('track_id', '?')}]\n{obj['distance']:.2f}m"
            text.lifetime = rospy.Duration(0.5)
            marker_array.markers.append(text)
        
        publisher.publish(marker_array)

    def publish_detection_image(self, detections):
        if self.cv_color_image is None:
            return
        
        vis = self.cv_color_image.copy()
        
        for det in detections:
            class_name = det['class_name']
            x_center, y_center = int(det['x_center']), int(det['y_center'])
            bbox = det['bbox']
            color = self.class_colors_bgr.get(class_name, (255, 255, 0))
            
            cv2.rectangle(vis, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.circle(vis, (x_center, y_center), 4, (128, 128, 128), -1)
            
            for obj in self.detected_objects_3d:
                if obj['class_name'] == class_name and 'sample_point' in obj:
                    sx, sy = obj['sample_point']
                    cv2.circle(vis, (sx, sy), 8, color, -1)
                    cv2.circle(vis, (sx, sy), 10, (255, 255, 255), 2)
                    
                    label = f"{class_name} {det['confidence']:.2f} D:{obj['depth_mm']/1000:.2f}m"
                    cv2.putText(vis, label, (int(bbox[0]), int(bbox[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    pos = obj['position']
                    cv2.putText(vis, f"({pos['x']:.2f},{pos['y']:.2f},{pos['z']:.2f})", 
                               (int(bbox[0]), int(bbox[3]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                    break
        
        try:
            self.vis_image_pub.publish(self.bridge.cv2_to_imgmsg(vis, "bgr8"))
        except Exception as e:
            rospy.logerr(f"Publish image failed: {e}")

    def get_detections_3d(self):
        return self.detected_objects_3d
    
    def get_detections_3d_odom(self):
        return self.detected_objects_3d_odom
    
    def run(self):
        rospy.loginfo("Detection3D running...")
        rospy.spin()


if __name__ == '__main__':
    try:
        node = Detection3D()
        node.run()
    except rospy.ROSInterruptException:
        pass
