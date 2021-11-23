#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
import numpy as np
from robot_drive_controller import RobotDriveController

class s_course_class():
    def __init__(self):
        self.robot_controller = RobotDriveController()

    def s_course(self):
        pass