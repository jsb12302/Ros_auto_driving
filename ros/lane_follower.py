#! /usr/bin/env python

import rospy
import time
import cv2
import cv_bridge
from line_detector import LineDetector
from robot_drive_controller import RobotDriveController

class LineTracer:
    def __init__(self):
        self.bridge=cv_bridge.CvBridge()
        self.line_one = LineDetector('left_camera/rgb/image_raw')
        self.line_two = LineDetector('right_camera/rgb/image_raw')
        self.robot_controller = RobotDriveController()
        self.err = 0
