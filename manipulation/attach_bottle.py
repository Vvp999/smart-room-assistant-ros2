import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import subprocess
import math


class BottleAttach(Node):
    def __init__(self):
        super().__init__('bottle_attach')
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        # CHANGED: 1.0 second timer
        self.create_timer(1.0, self.follow_robot)
        self.get_logger().info("Bottle Attach Started")

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        self.yaw = 2.0 * math.atan2(qz, qw)

    def follow_robot(self):
        world_x = self.x - 5.58
        world_y = self.y - 1.39

        offset = 0.05
        bottle_x = world_x + offset * math.cos(self.yaw)
        bottle_y = world_y + offset * math.sin(self.yaw)

        print(
            f"Robot X={world_x:.2f} "
            f"Robot Y={world_y:.2f} "
            f"Yaw={self.yaw:.2f} "
            f"Bottle X={bottle_x:.2f} "
            f"Bottle Y={bottle_y:.2f}"
        )

        # CHANGED: timeout 100
        cmd = f"""
gz service -s /world/default/set_pose \
--reqtype gz.msgs.Pose \
--reptype gz.msgs.Boolean \
--timeout 100 \
--req 'name: "water_bottle_1" position {{
x: {bottle_x}
y: {bottle_y}
z: 0.10
}}'
"""
        subprocess.run(
            cmd,
            shell=True,
            capture_output=True
        )


def main():
    rclpy.init()
    node = BottleAttach()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()