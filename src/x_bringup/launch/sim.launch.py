from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    mission = LaunchConfiguration('mission_file')
    return LaunchDescription([
        DeclareLaunchArgument('mission_file', default_value='mission_test.yaml'),
        Node(package='x_mission', executable='mission_handler', parameters=[{'mission_file': mission}]),
        Node(package='x_navigation', executable='waypoint_follower'),
        Node(package='x_control', executable='pid_controller'),
        Node(package='x_vision', executable='detector'),
    ])
