import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_new_interface.action import Factorial


class FactorialActionClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self.action_client = ActionClient(self, Factorial, 'factorial')

    def send_goal(self, n):
        goal_msg = Factorial.Goal()
        goal_msg.n = n

        self.action_client.wait_for_server()

        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.get_feedback_callback)

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')

        future_ = goal_handle.get_result_async()

        future_.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {}'.format(result.n_factorial))
        rclpy.shutdown()

    def get_feedback_callback(self, feedback):
        self.get_logger().info('Feedback: {}'.format(feedback.feedback.sequence_factorial_from_1_to_n))


def main(args=None):
    rclpy.init(args=args)

    factorial_action_client = FactorialActionClient('factorial_action_client_node')

    factorial_action_client.send_goal(n=7)

    rclpy.spin(factorial_action_client)


if __name__ == '__main__':
    main()