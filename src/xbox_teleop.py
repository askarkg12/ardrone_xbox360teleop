#!/usr/bin/env python

import rospy
import sys
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import std_srvs.srv


class ardroneXbox360:

	def __init__(self):
		sub = rospy.Subscriber('/joy', Joy, self.control)
		self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
		self.takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size = 1)
		self.land = rospy.Publisher('/ardrone/land', Empty, queue_size = 1)
		self.scale = rospy.Publisher('/lsd_slam/map_scale', Empty, queue_size = 1)
		self.request = rospy.Publisher('/lsd_slam/map_request', Empty, queue_size = 1)
		self.got_first_joy_msg = False
		self.droneCmd = Twist()

	def control(self, data):
		self.droneCmd.linear.x = data.axes[1]
		self.droneCmd.linear.y = data.axes[0]
		self.droneCmd.linear.z = data.axes[4]
		self.droneCmd.angular.z = data.axes[3]
		self.cmd_vel.publish(self.droneCmd)
		# A button
		if (data.buttons[0]):
			msg = Empty()
			self.takeoff.publish(msg)

		# B button
		if (data.buttons[1]):
			msg = Empty()
			self.land.publish(msg)

		# X button
		if (data.buttons[2]):
			msg = Empty()
			self.scale.publish(msg)

		# Y button
		if (data.buttons[3]):
			print("Checking if service exists")
			rospy.wait_for_service("/octomap_server/reset")
			print("Calling service")
			try:
				empty = rospy.ServiceProxy("/octomap_server/reset", std_srvs.srv.Empty)
				a = empty()
			except rospy.ServiceException, e:
				print "Service call failed: %s"%e
			rospy.wait_for_service("/octomap_server/reset")
			msg = Empty()
			self.request.publish(msg)




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
