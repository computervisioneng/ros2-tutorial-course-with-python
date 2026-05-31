import rclpy
from rclpy.node import Node


class CustomNode(Node):
    def __init__(self, name):
        super().__init__(name)

        self.create_timer(2, callback=self.callback)

    def callback(self):
        self.get_logger().info('hey!')


def main(args=None):
    rclpy.init(args=args)

    node = CustomNode('example_node_name')

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
