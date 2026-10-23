import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from x_interfaces.msg import Waypoint


class WaypointFollower(Node):
    """Toma el waypoint actual y genera setpoints suavizados para el control."""

    def __init__(self):
        super().__init__('waypoint_follower')
        self.max_speed = self.declare_parameter('max_speed', 0.5).value
        self.lookahead = self.declare_parameter('lookahead', 0.8).value
        self.target = None
        self.odom = None
        self.create_subscription(Waypoint, '/x/nav/waypoint', self.on_waypoint, 10)
        self.create_subscription(Odometry, '/x/odom', self.on_odom, 10)
        self.setpoint_pub = self.create_publisher(PoseStamped, '/x/control/setpoint', 10)
        self.create_timer(0.1, self.step)

    def on_waypoint(self, msg):
        self.target = msg

    def on_odom(self, msg):
        self.odom = msg

    def step(self):
        if self.target is None or self.odom is None:
            return
        p = self.odom.pose.pose.position
        t = self.target.position
        dist = math.dist((p.x, p.y, p.z), (t.x, t.y, t.z))
        ratio = min(1.0, self.lookahead / dist) if dist > 0 else 1.0
        sp = PoseStamped()
        sp.header.stamp = self.get_clock().now().to_msg()
        sp.header.frame_id = 'odom'
        sp.pose.position.x = p.x + (t.x - p.x) * ratio
        sp.pose.position.y = p.y + (t.y - p.y) * ratio
        sp.pose.position.z = p.z + (t.z - p.z) * ratio
        self.setpoint_pub.publish(sp)


def main():
    rclpy.init()
    rclpy.spin(WaypointFollower())
    rclpy.shutdown()
