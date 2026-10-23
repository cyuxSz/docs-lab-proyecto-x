import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from x_interfaces.msg import Detection


class Detector(Node):
    """Detecta la compuerta y la boya en la imagen de la camara frontal."""

    def __init__(self):
        super().__init__('detector')
        self.threshold = self.declare_parameter('confidence_threshold', 0.6).value
        self.model_path = self.declare_parameter('model_path', '').value
        self.bridge = CvBridge()
        self.create_subscription(Image, '/x/camera/image_raw', self.on_image, 10)
        self.pub = self.create_publisher(Detection, '/x/vision/detections', 10)

    def on_image(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # TODO: cargar el modelo ONNX; por ahora siempre reporta la compuerta al centro
        h, w = frame.shape[:2]
        det = Detection(label='gate', confidence=0.7, x=w // 4, y=h // 4, width=w // 2, height=h // 2)
        if det.confidence >= self.threshold:
            self.pub.publish(det)


def main():
    rclpy.init()
    rclpy.spin(Detector())
    rclpy.shutdown()
