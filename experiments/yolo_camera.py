import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2


class YoloCamera(Node):

    def __init__(self):
        super().__init__('yolo_camera')

        self.bridge = CvBridge()

        self.model = YOLO("yolov8n.pt")

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info("YOLO Camera Node Started")

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        results = self.model(frame, verbose=False)

        annotated = results[0].plot()

        cv2.imshow("YOLO Detection", annotated)
        cv2.waitKey(1)


def main():
    rclpy.init()

    node = YoloCamera()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()