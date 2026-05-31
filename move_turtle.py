import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CustomTurtleOperator(Node):
    def __init__(self, name):
        super().__init__(name)

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.create_timer(1, callback=self.callback)

    def callback(self):
        message = Twist()
        
        message.linear.x = random.uniform(-3, 3)
        message.linear.y = random.uniform(-3, 3)
        message.linear.z = random.uniform(-3, 3)
        message.angular.x = random.uniform(-3, 3)
        message.angular.y = random.uniform(-3, 3)
        message.angular.z = random.uniform(-3, 3)

        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)

    node = CustomTurtleOperator('example_node_name')

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
