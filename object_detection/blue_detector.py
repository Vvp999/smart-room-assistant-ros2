import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped
from cv_bridge import CvBridge

import cv2
import numpy as np
import os


class BlueFollower(Node):

    def __init__(self):

        super().__init__('blue_follower')

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

        self.attached = False

        self.get_logger().info("Blue Follower Started")

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

        robot_cmd = TwistStamped()

        if len(contours) > 0:

            largest = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(largest)

            if area > 200:

                x, y, w, h = cv2.boundingRect(largest)

                cx = x + w // 2
                cy = y + h // 2

                image_center = frame.shape[1] // 2

                error = image_center - cx

                print(
                    f"CX={cx} "
                    f"ERROR={error} "
                    f"AREA={int(area)}"
                )

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
                    f"Area={int(area)}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                if area > 8500:

                    robot_cmd.twist.linear.x = 0.0
                    robot_cmd.twist.angular.z = 0.0

                    self.cmd_pub.publish(robot_cmd)

                    if not self.attached:

                        self.attached = True

                        print("\nOBJECT ATTACHED\n")

                        # CHANGED: nohup so it runs cleanly in background
                        os.system(
                            "nohup python3 ~/ros2_yolo/attach_bottle.py "
                            "> /tmp/attach.log 2>&1 &"
                        )

                        cv2.destroyAllWindows()

                        print("EXITING NOW")

                        rclpy.shutdown()

                        os._exit(0)

                else:

                    robot_cmd.twist.linear.x = 0.10

                    robot_cmd.twist.angular.z = (
                        0.003 * error
                    )

                    self.cmd_pub.publish(
                        robot_cmd
                    )

        cv2.imshow(
            "Blue Follower",
            frame
        )

        cv2.waitKey(1)


def main():

    rclpy.init()

    node = BlueFollower()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass


if __name__ == '__main__':
    main()