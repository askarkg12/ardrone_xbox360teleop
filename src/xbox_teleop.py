#!/usr/bin/env python

import rospy
import sys
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty


class ardroneXbox360:
	
	def __init__(self):
		sub = rospy.Subscriber('/joy', Joy, self.control)
		self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
		self.got_first_joy_msg = False
		self.droneCmd = Twist()
		
	def control(self, data):
		self.droneCmd.linear.x = data.axes[1]
		self.droneCmd.linear.y = data.axes[0]
		self.droneCmd.linear.z = data.axes[4]
		self.droneCmd.angular.z = data.axes[3]
		self.cmd_vel.publish(self.droneCmd)

	
def main(args):
	teleop = ardroneXbox360();
	rospy.init_node('xbox_to_ar', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
    try:
        main(sys.argv)
    except rospy.ROSInterruptException:
        pass


