import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_new_interface.action import Factorial


class FactorialActionServer(Node):
    def __init__(self, name):
        super().__init__(name)
        self.action_server = ActionServer(self, Factorial, 'factorial', self.execute_callback)

    def execute_callback(self, goal_handle):
        feedback = Factorial.Feedback()
        feedback.sequence_factorial_from_1_to_n = []

        for j in range(goal_handle.request.n):
            if j == 0:
                feedback.sequence_factorial_from_1_to_n.append(1)
            else:
                feedback.sequence_factorial_from_1_to_n.append((j + 1) * feedback.sequence_factorial_from_1_to_n[j - 1])
            self.get_logger().info('Feedback: {}'.format(feedback.sequence_factorial_from_1_to_n))
            goal_handle.publish_feedback(feedback)

            time.sleep(1)

        goal_handle.succeed()

        result = Factorial.Result()
        result.n_factorial = feedback.sequence_factorial_from_1_to_n[-1]

        return result


def main(args=None):
    rclpy.init(args=args)

    factorial_action_server = FactorialActionServer('factorial_action_server_node')

    rclpy.spin(factorial_action_server)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
