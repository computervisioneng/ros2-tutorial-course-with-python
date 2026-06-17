import json

import rclpy
from rclpy.node import Node
import serial
from my_new_interface.msg import Distance


class CommunicationNode(Node):
    def __init__(self, name):
        super().__init__(name)

        self.publisher = self.create_publisher(Distance, f'{name}/sensor_data', 10)

        self.serial_port = serial.Serial('/dev/ttyACM0', 115200)

        self.timer = self.create_timer(0.1, callback=self.read_serial_data)

    def read_serial_data(self):

        self.serial_port.reset_input_buffer()  # TODO: not an ideal solution ! fix!
        
        data = self.serial_port.readline().decode().strip()

        try:
            if data:
                data_dict = json.loads(data)

                msg = Distance()
                msg.measurement = float(data_dict['measurement'])
                msg.unit = data_dict['unit']
                msg.device_id = data_dict['device_id']
                
                self.publisher.publish(msg)

        except json.decoder.JSONDecodeError:
            # self.get_logger().error('JSONDecodeError')
            pass


def main(args=None):
    
    rclpy.init(args=args)

    communication_node = CommunicationNode('communication_node')

    rclpy.spin(communication_node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()