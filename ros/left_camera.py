#!/usr/bin/env python0 00:15:00.129
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image

class camera:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.left_image_sub = rospy.Subscriber('left_camera/rgb/image_raw', Image, self.left_image_callback)

if __name__ == '__main__':
    rospy.init_node('lane_trace')
    c=camera()
