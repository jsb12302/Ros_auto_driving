#! /usr/bin/env python

import cv2
import numpy
from convert_image import ConvertImage
from functools import reduce

class LineDetector(ConvertImage):
    def __init__(self, topic_name):
        ConvertImage.__init__(self, topic_name)
        self.cx=0

    def image_callback(self,msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_white = numpy.array([10, 40, 135])
        upper_white = numpy.array([135, 135, 255])
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        h, w, d = image.shape
        search_top = 3 * h / 8
        search_bot = search_top + 20

        mask_white[0:search_top, 0:w] = 0
        mask_white[search_bot:h, 0:w] = 0

        M_w = cv2.moments(mask_white)

        if M_w['m00'] > 0:
            self.cx = int(M_w['m10'] / M_w['m00'])
            self.cy = int(M_w['m01'] / M_w['m00'])
            self.err = self.cx - w / 2
