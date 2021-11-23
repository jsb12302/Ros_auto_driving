#! /usr/bin/env python
# coding=utf-8

import rospy
import numpy as np
import cv2
from convert_image import ConvertImage
from std_msgs.msg import String
from robot_drive_controller import RobotDriveController

class BlockBarDetect(ConvertImage):
    def __init__(self):
        ConvertImage.__init__(self,'camera/rgb/image_raw')
        self.go_sign=None
        self.go_sign_pub=rospy.Publisher('blocking_bar',String,queue_size=1)
        self.contours = []
        self.drive_controller = RobotDriveController()

    def image_callback(self,msg):
        image=self.image_converter(msg,'hsv')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 0, 90])
        upper_red = np.array([5, 5, 110])
        gray_img = cv2.inRange(image, lower_red, upper_red)

        h, w = gray_img.shape
        block_bar_mask = gray_img
        block_bar_mask[0:180, 0:w] = 0
        block_bar_mask[240:h, 0:w] = 0

        block_bar_mask, self.contours, hierarchy = cv2.findContours(
            block_bar_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(self.contours)==3:
            self.go_sign = True
        if len(self.contours)!=3:
            self.go_sign = False

# rospy.init_node('test')
# sub=BlockBarDetect()
# rospy.spin()