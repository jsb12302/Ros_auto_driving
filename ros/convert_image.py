#! /usr/bin/env python

import rospy
import cv_bridge
import cv2
from sensor_msgs.msg import Image

class ConvertImage:
    def __init__(self,image):
        self.bridge=cv_bridge.CvBridge()
        self.image_sub=rospy.Subscriber(image,Image,self.image_callback)

    def image_converter(self,image,type):
        if type=='hsv':
            converted_img=self.bridge.imgmsg_to_cv2(image,desired_encoding='bgr8')
            converted_img=cv2.cvtColor(converted_img,cv2.COLOR_BGR2HSV)
            return converted_img

    def image_callback(self,msg):
        raise NotImplementedError