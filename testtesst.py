import sys
import rclpy
from rclpy.node import Node
import random

from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TwistNode(Node):
    def __init__(self):
        super().__init__('twist_node')

        print('Creating publisher')
        self.twist_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.i = 0

    def turn_left(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = -0.4
        self.twist_publisher.publish(twist)

    def turn_right(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.4
        self.twist_publisher.publish(twist)

    def go_straight(self):
        twist = Twist()
        twist.linear.x = 0.3
        twist.angular.z = 0.0
        self.twist_publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)

    twist_node = TwistNode()
    
    user_input = input("Enter a number: ")

    while True:
        if user_input == '1':
            for i in range(8):
                twist_node.turn_left()
                rclpy.spin_once(twist_node, timeout_sec=0.5)
        elif user_input == '2':
            for i in range(8):
                twist_node.turn_right()
                rclpy.spin_once(twist_node, timeout_sec=0.5)
        else: 
            twist_node.go_straight()
            rclpy.spin_once(twist_node, timeout_sec=0.5)

    print("Done")
    twist_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
