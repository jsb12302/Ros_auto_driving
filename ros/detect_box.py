#!/usr/bin/env python
# coding=utf-8

import math
import rospy
from sensor_msgs.msg import LaserScan
from robot_drive_controller import RobotDriveController

class Detectbox:
    def __init__(self):
        self.range_ahead = 0
        self.range_right = 0
        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_callback)
        self.drive_controller = RobotDriveController()

    def scan_callback(self,msg):
        self.range_ahead = msg.ranges[len(msg.ranges) / 2]
        self.range_right = max(msg.ranges[160],msg.ranges[240])

# if __name__=="__main__":
#     rospy.init_node("range")
#     d=Detectbox()
#     rospy.spin()