#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2 as cv
from cv_bridge import CvBridge
from std_msgs.msg import Int32MultiArray

class DetectArucoNode(Node):

    def __init__(self):
        super().__init__("detect_aruco_ids")
        #1- subscribe the camera
        self.camera_sub = self.create_subscription(Image,"/shiv_1/camera/image", self.camera_callback, 10)
        self.ids_pub = self.create_publisher(Int32MultiArray, "aruco_ids", 10)
        self.bridge = CvBridge()
        # ArUco setup
        self.aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
        self.aruco_params = cv.aruco.DetectorParameters_create()


    def camera_callback(self,msg):
        # Convert ROS -> OpenCV
        current_frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        # Detect
        corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(current_frame, self.aruco_dict, parameters=self.aruco_params)
        print(ids)
        # Draw markers
        if ids is not None:
            cv.aruco.drawDetectedMarkers(current_frame, corners, ids)
            id_msg = Int32MultiArray()
            id_msg.data = ids.flatten().tolist()
            self.ids_pub.publish(id_msg)
            self.get_logger().info(f"Detected IDs: {ids.flatten()}")
            self.get_logger().info(f"Published IDs: {id_msg}")
            # cv.imwrite("test_1_map.jpg",current_frame)

def main(args=None):
    rclpy.init(args=args)
    node = DetectArucoNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()

