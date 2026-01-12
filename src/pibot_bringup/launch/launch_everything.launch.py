import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    ld = LaunchDescription()
    pkg_path = get_package_share_directory('omar_project')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    #paths
    nav2_params = os.path.join(pkg_path, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg_path, 'config', 'nav2_view.rviz')
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    map_file = os.path.join(pkg_path, 'map', 'map.yaml')

    # 1. HARDWARE (The Body)
    # ----------------------
    pibot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("PiBot"), "launch", "PiBot_launch.py")
        )
    )
    
    # Lidar Driver
    lidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
            'range_min': 0.10 
        }],
        output='screen'
    )
    # 2. TRANSFORMS (The Skeleton)
    # ----------------------------
    robot_desc = ParameterValue(
        Command(['cat ', urdf_file]),
        value_type=str
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_desc}],
        output="screen"
    )

    # 3. NAVIGATION (The Brain)
    # -------------------------
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_file,
            'params_file': nav2_params,
            'use_sim_time': 'False',
            'autostart': 'True'
        }.items()
    )

    # 4. VISUALIZATION (The Eyes)
    # ---------------------------
    # UNCOMMENT to enable RViz visualization on the Pi
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': False}],
        output='screen'
    )

    # 5. LOGIC (The Mission)
    # ----------------------
    nav2_test_node = Node(
        package='omar_project',
        executable='nav2_test',
        name='nav2_test',
        output='screen'
    )
    ld.add_action(robot_state_publisher)
    ld.add_action(lidar_node)
    ld.add_action(pibot)
    ld.add_action(nav2)
    ld.add_action(nav2_test_node)
    ld.add_action(rviz_node)
    return ld