#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from ament_index_python.packages import get_package_share_directory
import csv
import time
import os
import yaml


class ArucoLogger(Node):
    def __init__(self):
        super().__init__('aruco_logger')

        # -----------------------
        # Internal State
        # -----------------------
        self.last_seen_bay = "Unknown"  # To track where the robot is

        # -----------------------
        # Subscriber
        # -----------------------
        self.id_sub = self.create_subscription(
            Int32MultiArray,
            'aruco_ids',
            self.ids_callback,
            10
        )

        # -----------------------
        # Load YAML
        # -----------------------
        # We need to parse the specific structure of your YAML file
        try:
            pkg_path = get_package_share_directory('inventory_verification')
            yaml_path = os.path.join(pkg_path, 'config', 'aruco_ids.yaml')
            
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                # Load the specific dictionaries from the file
                self.sku_map = data.get('sku_by_id', {})
                self.bay_map = data.get('bay_by_id', {})
                self.expected_rules = data.get('expected_bay_by_sku', {})
                
            self.get_logger().info("YAML Loaded Successfully")
            
        except Exception as e:
            self.get_logger().error(f"Failed to load YAML: {e}")
            self.sku_map = {}
            self.bay_map = {}
            self.expected_rules = {}

        # -----------------------
        # CSV logging
        # -----------------------
        self.csv_file = open('aruco_log.csv', 'a', newline='')
        self.writer = csv.writer(self.csv_file)

        # write header once if file is empty
        if self.csv_file.tell() == 0:
            self.writer.writerow(['Timestamp', 'Detected_ID', 'Type', 'Name/Bay', 'Location_Status'])

        self.get_logger().info("Aruco Logger Ready")

    # -----------------------
    # Callback
    # -----------------------
    def ids_callback(self, msg: Int32MultiArray):
        current_ids = msg.data
        if not current_ids:
            return

        # STEP 1: Update Location
        # Check if any visible ID is a Bay ID (1, 2, 3) to update our location
        current_bay = None
        for arid in current_ids:
            arid_str = str(arid)
            if arid_str in self.bay_map:
                current_bay = self.bay_map[arid_str]
                self.last_seen_bay = current_bay
                break   # use the first bay marker in view

        # STEP 2: Process & Log Items
        for arid in current_ids:
            arid_str = str(arid)
            timestamp = time.strftime("%H:%M:%S")
            
            # CASE A: It is a BAY (ID 1, 2, 3)
            if arid_str in self.bay_map:
                bay_name = self.bay_map[arid_str]
                self.log_entry(timestamp, arid, "BAY", bay_name, "Reference Point")

            # CASE B: It is a PRODUCT (ID 4, 5, 6)
            elif arid_str in self.sku_map:
                product_name = self.sku_map[arid_str] # e.g., "salsa"
                expected_bay = self.expected_rules.get(product_name) # e.g., "Bay1"
                
                # Verify Logic
                status = "Unknown Location"
                if self.last_seen_bay != "Unknown":
                    if self.last_seen_bay == expected_bay:
                        status = "CORRECT"
                    else:
                        status = f"WRONG (Found in {self.last_seen_bay}, Expected {expected_bay})"
                
                self.log_entry(timestamp, arid, "PRODUCT", product_name, status)
                
                # Console Output for debugging
                color = "\033[92m" if status == "CORRECT" else "\033[91m" # Green/Red
                reset = "\033[0m"
                self.get_logger().info(f"{color}Found {product_name} at {self.last_seen_bay} -> {status}{reset}")

            # CASE C: Unknown ID
            else:
                self.get_logger().warn(f"Detected unknown ID: {arid}")

    def log_entry(self, timestamp, arid, type_str, name, status):
        self.writer.writerow([timestamp, arid, type_str, name, status])
        self.csv_file.flush()

def main():
    rclpy.init()
    node = ArucoLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'csv_file'):
            node.csv_file.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()