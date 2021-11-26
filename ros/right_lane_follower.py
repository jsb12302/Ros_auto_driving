#!/usr/bin/env python0 00:15:00.129
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
import numpy as np
from robot_drive_controller import RobotDriveController

class Right_lane_follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.right_image_sub = rospy.Subscriber('right_camera/rgb/image_raw', Image, self.right_image_callback)
        self.robot_controller = RobotDriveController()
        self.cx_yellow=0
        self.cy_yellow=0

    def right_image_callback(self,msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255]) #right white origin

        lower_yellow = numpy.array([10, 40, 135])
        upper_yellow = numpy.array([135, 135, 255])

        mask_yellow = cv2.inRange(hsv,lower_white ,upper_white)

        h, w, d = image.shape
        search_top = 3 * h / 8
        search_bot = search_top + 20

        mask_yellow[0:search_top, 0:w] = 0
        mask_yellow[search_bot:h, 0:w] = 0


        M_y = cv2.moments(mask_yellow)

        if M_y['m00'] > 0:
            self.cx_yellow = int(M_y['m10'] / M_y['m00'])
            self.cy_yellow = int(M_y['m01'] / M_y['m00'])

        # cv2.circle(image, (self.cx_yellow, self.cy_yellow), 20, (0, 255, 255), -1)
        # cv2.imshow('mask', image)
        # cv2.waitKey(3)


