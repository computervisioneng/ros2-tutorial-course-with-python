import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from functools import partial
from rcl_interfaces.msg import SetParametersResult


class CustomTurtleOperator(Node):
    def __init__(self, name):
        super().__init__(name)

        self.declare_parameter('random_strength', 3.0)
        self.declare_parameter('teleport_rate', 0.1)
        self.declare_parameter('random_probability_distribution', 'uniform')
        self.declare_parameter('teleport_drawing_off', True)

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.create_timer(1, callback=self.callback)

        self.add_on_set_parameters_callback(self.validate_params)

    def validate_params(self, params):
        for param in params:
            if param.name == 'random_probability_distribution' and param.value not in ['uniform', 'normal']:
                return SetParametersResult(
                    successful=False,
                    reason="random_probability_distribution value needs to be in ['uniform', 'normal']"
                )
        
        return SetParametersResult(successful=True)
        
    def sample(self, a, b, prob_distribution):

        if prob_distribution == 'uniform':
            return random.uniform(a, b)
        elif prob_distribution == 'normal':
            _ = random.gauss(mu=((a + b) / 2), sigma=1.0)
            if _ < a:
                _ = float(a)
            if _ > b:
                _ = float(b)
            return _

    def callback(self):
        message = Twist()

        random_strength = self.get_parameter('random_strength').value
        teleport_rate = self.get_parameter('teleport_rate').value
        teleport_drawing_off = self.get_parameter('teleport_drawing_off').value
        random_probability_distribution = self.get_parameter('random_probability_distribution').value
        
        message.linear.x = random_strength * self.sample(-1, 1, random_probability_distribution)
        message.linear.y = random_strength * self.sample(-1, 1, random_probability_distribution)
        message.linear.z = random_strength * self.sample(-1, 1, random_probability_distribution)
        message.angular.x = random_strength * self.sample(-1, 1, random_probability_distribution)
        message.angular.y = random_strength * self.sample(-1, 1, random_probability_distribution)
        message.angular.z = random_strength * self.sample(-1, 1, random_probability_distribution)

        self.publisher.publish(message)

        if random.random() < teleport_rate:

            if teleport_drawing_off:
                self.call_set_pen_service(255, 255, 255, 3, True)

            x = self.sample(0, 10, random_probability_distribution)
            y = self.sample(0, 10, random_probability_distribution)
            theta = self.sample(0, 10, random_probability_distribution)
            self.call_set_teleport_service(x, y, theta)

            if teleport_drawing_off:
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
