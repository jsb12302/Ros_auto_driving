#!/usr/bin/env python
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist


class Detect_Sign:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.contours = []

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = numpy.array([0, 50, 50])
        upper_red = numpy.array([15, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        masked = cv2.bitwise_and(image, image, mask=mask)

        h, w, d = image.shape

        mask[0:0, 0:w] = 0
        mask[10:h, 0:w] = 0

        mask, self.contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # if len(self.contours) > 0:
        #     print("STOP")
            # self.twist.linear.x = 0.0
            # # sleep(3000)
            # self.cmd_vel_pub.publish(self.twist)

        # if len(self.contours) == 0:
        #     print("GO")
        #     self.twist.linear.x = 0.8
        #     self.cmd_vel_pub.publish(self.twist)

        # cv2.imshow("window", mask)
        # cv2.waitKey(3)


# rospy.init_node('detect_sign')
# detect_sign = Detect_Sign()
# rospy.spin()