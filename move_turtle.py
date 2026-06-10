import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from functools import partial
from my_new_interface.srv import SetRandomStrength


class CustomTurtleOperator(Node):
    def __init__(self, name):
        super().__init__(name)

        self.random_strength = 3

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.create_timer(1, callback=self.callback)

        self.service = self.create_service(
           SetRandomStrength,
           f'{name}/set_random_strength',
           self.set_random_strength_callback
        )

    def set_random_strength_callback(self, request, response):
        self.random_strength = request.random_strength
        return response


    def callback(self):
        message = Twist()
        
        message.linear.x = self.random_strength * random.uniform(-1, 1)
        message.linear.y = self.random_strength * random.uniform(-1, 1)
        message.linear.z = self.random_strength * random.uniform(-1, 1)
        message.angular.x = self.random_strength * random.uniform(-1, 1)
        message.angular.y = self.random_strength * random.uniform(-1, 1)
        message.angular.z = self.random_strength * random.uniform(-1, 1)

        self.publisher.publish(message)

        if random.random() < 0.1:

            self.call_set_pen_service(255, 255, 255, 3, True)

            x = random.uniform(0, 10)
            y = random.uniform(0, 10)
            theta = random.uniform(0, 10)
            self.call_set_teleport_service(x, y, theta)

            self.call_set_pen_service(255, 255, 255, 3, False)

    def call_set_pen_service(self, r, g, b, width, off):

        client = self.create_client(SetPen, '/turtle1/set_pen')

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        response = future.result()


    def call_set_teleport_service(self, x, y, theta):

        client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

        request = TeleportAbsolute.Request()
        request.x = x
        request.y = y
        request.theta = theta

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_teleport))

    def callback_set_teleport(self, future):
        response = future.result()


def main(args=None):
    rclpy.init(args=args)

    node = CustomTurtleOperator('example_node_name')

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
