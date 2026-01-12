#!/usr/bin/env python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import tf_transformations
import time 
import math

def create_pose_stamped(navigator: BasicNavigator, position_x, position_y, orientation_z):
    q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = position_x
    pose.pose.position.y = position_y
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = q_x
    pose.pose.orientation.y = q_y
    pose.pose.orientation.z = q_z
    pose.pose.orientation.w = q_w
    return pose

def main():
    # --- Init
    rclpy.init()
    nav = BasicNavigator()

    # --- Set initial pose
    nav.waitUntilNav2Active()
    initial_pose = create_pose_stamped(nav, 7.62, 0.5, math.pi) #300,20
    nav.setInitialPose(initial_pose)

    # --- Wait for Nav2
    nav.waitUntilNav2Active()

    print("Waiting for AMCL to acknowledge initial pose")
    # wait_until_initial_pose(nav)
    print("AMCL RECEIVED INITIAL POSE")
    # --- Send Nav2 goal
    waypoints = []
    waypoints.append(create_pose_stamped(nav, 5.08, 2.54, 0.0)) #200, 100 
    waypoints.append(create_pose_stamped(nav, 5.84, 1.52, math.pi)) #230, 60 
    waypoints.append(create_pose_stamped(nav, 3.81, 2.00, math.pi)) #150, 80
    waypoints.append(create_pose_stamped(nav, 2.54, 2.54, math.pi)) #100, 100
    
    for i,wp in enumerate(waypoints):
        print(f"Navigate to waypoint {i+1}")
        nav.goToPose(wp)
        
        while not nav.isTaskComplete():
            rclpy.spin_once(nav, timeout_sec=0.1)
            feedback = nav.getFeedback()
        
        result = nav.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"Reached Waypoint {i+1}. Waiting 5 seconds for Inventory Scan")
            time.sleep(5.0) 
        else:
            print(f"Failed to reach Waypoint {i+1}")
            
    # print(nav.getResult())
    print("Navigation Finished")

    # --- Shutdown
    rclpy.shutdown()

if __name__ == '__main__':
    main()