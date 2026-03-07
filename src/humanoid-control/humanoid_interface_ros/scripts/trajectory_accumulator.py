#!/usr/bin/env python3
"""
累积 /humanoid/optimizedStateTrajectory 中的 CoM 和手臂轨迹历史路径。

发布：
  /humanoid/accumulated_com_path      (nav_msgs/Path)
  /humanoid/accumulated_hand_markers  (visualization_msgs/MarkerArray)  左右手各一条
"""

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import MarkerArray, Marker

# type=4 是 LINE_STRIP，type=7 是 SPHERE_LIST
LINE_STRIP = 4


class TrajectoryAccumulator:
    def __init__(self):
        rospy.init_node("trajectory_accumulator")

        self.frame_id = rospy.get_param("~frame_id", "odom")
        self.max_points = rospy.get_param("~max_points", 10000)

        # CoM 历史路径
        self.com_path = Path()
        self.com_path.header.frame_id = self.frame_id

        # 两只手的历史点，key 为 marker id（首次出现时确定）
        # {id: [geometry_msgs/Point, ...]}
        self.hand_history: dict = {}
        self.hand_ids: list = []          # 按顺序记录两个手的 id
        self.hand_colors = [
            (1.0, 0.4, 0.0, 1.0),        # 左手橙色
            (0.0, 0.7, 1.0, 1.0),        # 右手青色
        ]

        self.com_pub = rospy.Publisher(
            "/humanoid/accumulated_com_path", Path, queue_size=1, latch=True
        )
        self.hand_pub = rospy.Publisher(
            "/humanoid/accumulated_hand_markers", MarkerArray, queue_size=1, latch=True
        )

        rospy.Subscriber(
            "/humanoid/optimizedStateTrajectory",
            MarkerArray,
            self._callback,
            queue_size=1,
        )

        rospy.loginfo("[trajectory_accumulator] 已启动，订阅 /humanoid/optimizedStateTrajectory ...")
        rospy.spin()

    def _callback(self, msg: MarkerArray):
        if not msg.markers:
            return
        stamp = msg.markers[0].header.stamp

        for marker in msg.markers:
            if marker.type != LINE_STRIP or not marker.points:
                continue

            # CoM 轨迹
            if marker.ns == "CoM Trajectory":
                # 取当前帧第一个点（机器人当前位置）追加到历史路径
                pose = PoseStamped()
                pose.header.stamp = stamp
                pose.header.frame_id = self.frame_id
                pose.pose.position = marker.points[0]
                pose.pose.orientation.w = 1.0
                self.com_path.poses.append(pose)
                if len(self.com_path.poses) > self.max_points:
                    self.com_path.poses = self.com_path.poses[-self.max_points:]
                self.com_path.header.stamp = stamp
                self.com_pub.publish(self.com_path)

            # 手臂轨迹：ns 为空字符串
            elif marker.ns == "":
                mid = marker.id
                if mid not in self.hand_history:
                    self.hand_history[mid] = []
                    self.hand_ids.append(mid)

                # 追加当前规划的第一个点（手的当前位置）
                self.hand_history[mid].append(marker.points[0])
                if len(self.hand_history[mid]) > self.max_points:
                    self.hand_history[mid] = self.hand_history[mid][-self.max_points:]

        # 发布手臂历史
        if self.hand_history:
            self._publish_hand_markers(stamp)

    def _publish_hand_markers(self, stamp):
        ma = MarkerArray()
        for idx, mid in enumerate(sorted(self.hand_ids)):
            m = Marker()
            m.header.frame_id = self.frame_id
            m.header.stamp = stamp
            m.ns = "accumulated_hand"
            m.id = idx
            m.type = LINE_STRIP
            m.action = Marker.ADD
            m.scale.x = 0.008
            r, g, b, a = self.hand_colors[idx % len(self.hand_colors)]
            m.color.r, m.color.g, m.color.b, m.color.a = r, g, b, a
            m.pose.orientation.w = 1.0
            m.points = list(self.hand_history[mid])
            m.lifetime = rospy.Duration(0)
            ma.markers.append(m)
        self.hand_pub.publish(ma)


if __name__ == "__main__":
    TrajectoryAccumulator()
