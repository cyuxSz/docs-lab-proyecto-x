import os

import yaml
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from x_interfaces.msg import Waypoint, Detection
from x_interfaces.srv import SetMission


class MissionHandler(Node):
    """Recorre los pasos de una mision y publica el waypoint actual."""

    def __init__(self):
        super().__init__('mission_handler')
        self.steps = []
        self.index = 0
        self.last_detection = None
        self.wp_pub = self.create_publisher(Waypoint, '/x/nav/waypoint', 10)
        self.create_subscription(Detection, '/x/vision/detections', self.on_detection, 10)
        self.create_service(SetMission, '/x/mission/set', self.on_set_mission)
        self.load(self.declare_parameter('mission_file', 'mission_1.yaml').value)
        self.create_timer(0.5, self.step)

    def load(self, name):
        path = os.path.join(get_package_share_directory('x_mission'), 'missions', name)
        with open(path) as f:
            self.steps = yaml.safe_load(f)['steps']
        self.index = 0
        self.get_logger().info(f'Mision cargada: {name} ({len(self.steps)} pasos)')

    def on_set_mission(self, req, res):
        try:
            self.load(req.mission_file)
            res.success = True
        except (OSError, KeyError) as e:
            res.success, res.message = False, str(e)
        return res

    def on_detection(self, msg):
        self.last_detection = msg

    def step(self):
        if self.index >= len(self.steps):
            return
        s = self.steps[self.index]
        wp = Waypoint(tolerance=0.3)
        if s['type'] == 'dive':
            wp.position.z = s['depth']
        elif s['type'] == 'goto':
            wp.position.x, wp.position.y, wp.position.z = s['x'], s['y'], s['z']
        elif s['type'] == 'search':
            if self.last_detection and self.last_detection.label == s['label']:
                self.index += 1
            return
        elif s['type'] == 'surface':
            wp.position.z = 0.0
        self.wp_pub.publish(wp)
        # TODO: avanzar solo al llegar al waypoint, ahora avanza cada tick
        self.index += 1


def main():
    rclpy.init()
    rclpy.spin(MissionHandler())
    rclpy.shutdown()
