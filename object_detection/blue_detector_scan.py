import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class BlueDetector(Node):

    def __init__(self):

        super().__init__('blue_detector')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.detected = False

        print("Blue Detector Started")

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower_blue,
            upper_blue
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:

            largest = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(largest)

            if area > 500:

                if not self.detected:

                    self.detected = True

                    print("\nBLUE OBJECT DETECTED\n")

        cv2.imshow("Blue Detection", frame)

        cv2.waitKey(1)


def main():

    rclpy.init()

    node = BlueDetector()

    rclpy.spin(node)


if __name__ == '__main__':
    main()