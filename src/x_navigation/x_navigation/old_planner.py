# Planner con curvas de bezier y puntos aleatorios. Ya no lo lanza nadie,
# lo reemplazo waypoint_follower pero no lo borramos por si acaso.
import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class OldPlanner(Node):
    def __init__(self):
        super().__init__('old_planner')
        self.pub = self.create_publisher(PoseStamped, '/planner/goal', 10)
        self.create_timer(2.0, self.tick)

    def tick(self):
        sp = PoseStamped()
        sp.pose.position.x = random.uniform(-5, 5)
        sp.pose.position.y = random.uniform(-5, 5)
        sp.pose.position.z = -1.0
        self.pub.publish(sp)


def main():
    rclpy.init()
    rclpy.spin(OldPlanner())
    rclpy.shutdown()
