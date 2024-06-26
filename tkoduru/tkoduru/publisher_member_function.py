# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import random

from std_msgs.msg import String

SIGNAL_STATUS = 1 # Continue transmitting messages until STOP signal is received

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        # Transmit to FLASH (Signals outputted by the subscriber)
        self.publisher_ = self.create_publisher(String, 'FLASH', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Listen to THUNDER (Signals inputted by the subscriber)
        self.subscription = self.create_subscription(
            String,
            'THUNDER',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning


    def timer_callback(self):
        msg = String()
        msg.data = f"{random.randint(0, 100)}"
        self.publisher_.publish(msg)
        self.get_logger().info('FLASH: "%s"' % msg.data)

    def listener_callback(self, msg):
        if(msg.data == 'STOP'):
            self.get_logger().info('STOP RECIEVED.')
            self.destroy_node()
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
