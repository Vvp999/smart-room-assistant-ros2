import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped
from cv_bridge import CvBridge

import cv2
import numpy as np
import time


class RoomScanner(Node):

    def __init__(self):

        super().__init__('room_scanner')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        self.detected = False
        self.last_frame = None

        print("Starting 360 degree room scan...")

        self.rotate_and_scan()

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        self.last_frame = frame.copy()

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

                x, y, w, h = cv2.boundingRect(largest)

                cx = x + w // 2
                cy = y + h // 2

                self.detected = True

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "BLUE DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Room Scan", frame)
        cv2.waitKey(1)

    def rotate_and_scan(self):

        twist = TwistStamped()

        twist.twist.angular.z = 0.5

        start_time = time.time()

        while time.time() - start_time < 12.5:

            self.cmd_pub.publish(twist)

            rclpy.spin_once(
                self,
                timeout_sec=0.05
            )

        twist.twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

        print("\n====================")

        if self.detected:

            print("BLUE OBJECT DETECTED")

        else:

            print("NO BLUE OBJECT DETECTED")

            if self.last_frame is not None:

                cv2.putText(
                    self.last_frame,
                    "NO BLUE OBJECT DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                cv2.imshow(
                    "Room Scan",
                    self.last_frame
                )

                cv2.waitKey(3000)

        print("SCAN COMPLETE")
        print("====================\n")


def main():

    rclpy.init()

    node = RoomScanner()

    rclpy.spin(node)


if __name__ == '__main__':
    main()