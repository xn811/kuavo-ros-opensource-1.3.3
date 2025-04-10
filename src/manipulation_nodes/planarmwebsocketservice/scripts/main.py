from model_utils import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LOAD YOLO model path')
    parser.add_argument('--model_path', type=str, default="")
    args = parser.parse_args()
    
    yolo_detection = YOLO_detection()

    yolo_detection.init_ros_node()

    model = yolo_detection.load_model(args.model_path)

    rate = rospy.Rate(20)

    while not yolo_detection.node_is_shutdown():

        results = yolo_detection.detect_objects(model)

        yolo_detection.show_results(results)

        yolo_detection.publish_results(results)

        rate.sleep() 
