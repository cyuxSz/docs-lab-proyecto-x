# Igual que sim pero con el driver de la camara real.
# Ojo: este launch no se ha probado desde que se cambio a waypoint_follower.
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='usb_cam', executable='usb_cam_node_exe', remappings=[('image_raw', '/x/camera/image_raw')]),
        Node(package='x_mission', executable='mission_handler', parameters=[{'mission_file': 'mission_1.yaml'}]),
        Node(package='x_navigation', executable='waypoint_follower'),
        Node(package='x_control', executable='pid_controller'),
        Node(package='x_vision', executable='detector'),
    ])
