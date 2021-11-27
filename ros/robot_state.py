#! /usr/bin/env python
# coding=utf-8

import rospy
import time
from std_msgs.msg import String
from smach import State
from block_bar_detect import BlockBarDetect
from lane_follower2 import LineTracer2
from stop_line_detect import DetectStopLine
from go_7sec import Go_7sec
import time
from detect_box import Detectbox
from right_lane_follower import Right_lane_follower
from detect_sign import Detect_Sign

class BlockingBarState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.blocking_bar_sub = rospy.Subscriber('blocking_bar', String)
        self.stop_sign = False

    def execute(self, ud):
        block_finder = BlockBarDetect()
        rate = rospy.Rate(20)
        while True:
            if block_finder.go_sign:
                rospy.loginfo("Start Driving")
                block_finder.drive_controller.set_velocity(1)
                start_time = time.time() + 5

                while True:
                    block_finder.drive_controller.drive()
                    if time.time() - start_time > 0:
                        break
                block_finder.drive_controller.set_velocity(0)
                return 'success'

class LineTrace(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    def execute(self,ud):
        line=LineTracer2()

        stop_line=DetectStopLine()
        rate=rospy.Rate(10)
        stop_line_count=0

        while not rospy.is_shutdown():
            line_stop=0
            cx=(line.cx_yellow+line.cx_white)/2-230
            err=-float(cx)/100

            if stop_line_count==1:
                line_stop=6000
            else:
                line_stop=8600
            if stop_line.area>line_stop:
                line.robot_controller.set_velocity(0)
                line.robot_controller.set_angular(0)
                stop_line_count = stop_line_count + 1
                print('stop!')
                print "stop_line_count",stop_line_count
                rospy.sleep(3)

            if abs(err) < 0.5:
                line.robot_controller.set_velocity(0.7)
            if abs(err) >= 0.5:
                line.robot_controller.set_velocity(0.7)
            line.robot_controller.set_angular(err)
            line.robot_controller.drive()

            if stop_line_count==2:
                print "end-----------------------------"
                return 'success'

class StopLine2_section(State):
    def __init__(self):
        State.__init__(self,outcomes=['success'])
    def execute(self, ud):

        line=LineTracer2()
        stop_line = DetectStopLine()
        rate = rospy.Rate(10)
        stop_line_count=2
        while not rospy.is_shutdown():

            cx = (line.cx_yellow-50 + line.cx_white) / 2 - 230
            err=-float(cx)/100

            if stop_line_count==3:
                cx = (line.cx_yellow - 50 + line.cx_white+20) / 2 - 230

            if stop_line.area>9500.0:
                line.robot_controller.set_velocity(0)
                line.robot_controller.set_angular(0)
                stop_line_count = stop_line_count + 1
                print('stop!')
                print "stop_line_cout",stop_line_count
                rospy.sleep(3)

            if abs(err) < 0.5:
                line.robot_controller.set_velocity(0.4)
            if abs(err) >= 0.5:
                line.robot_controller.set_velocity(0.4)
            line.robot_controller.set_angular(err+0.6)
            line.robot_controller.drive()

            if stop_line_count == 4:
                print "end-----------------------------"
                return 'success'

class Go_7sec_class(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

    def execute(self, ud):
        start_time=time.time()+6.5
        go=Go_7sec()
        tmp_time = time.time() + 0.2

        while not rospy.is_shutdown():
            go.robot_controller.set_angular(0.3)
            go.robot_controller.set_velocity(0)
            go.robot_controller.drive()
            if time.time() - tmp_time > 0:
                break

        while not rospy.is_shutdown():
            go.robot_controller.set_angular(0)
            go.robot_controller.set_velocity(0.8)
            go.robot_controller.drive()
            if time.time() - start_time >0:
                break
        return 'success'

class S_course(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

    def execute(self, ud):
        line = LineTracer2()
        stop_line = DetectStopLine()
        stop_line_count = 4
        start_time = 0
        while not rospy.is_shutdown():
            rate = rospy.Rate(20)
            while not rospy.is_shutdown():

                cx = (line.cx_white+5  + line.cx_yellow-30 ) / 2 - 320
                err = -float(cx) / 100

                if stop_line.area > 8800.0:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_count", stop_line_count
                    rospy.sleep(3)

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.6)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.6)
                line.robot_controller.set_angular(err - 0.3)
                line.robot_controller.drive()

                if stop_line_count == 5:
                    print "stoppppppp"
                    break

            while True:
                rate = rospy.Rate(20)

                if stop_line.area > 12500.0:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_cout", stop_line_count
                    rospy.sleep(3)

                cx = (line.cx_white + line.cx_yellow ) / 2 - 320
                err = -float(cx) / 100
                line.robot_controller.set_angular(err - 0.4)

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.5)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.5)

                line.robot_controller.set_angular(err - 0.4)
                line.robot_controller.drive()

                if stop_line_count == 6:
                    print "stoppppppp"
                    break

            go_time=time.time()+5.5
            turn_time = time.time() + 7
            while True:
                line.robot_controller.set_velocity(0.5)
                line.robot_controller.set_angular(0)
                line.robot_controller.drive()

                if time.time() - go_time > 0:
                    break

            while True:
                line.robot_controller.set_velocity(0.3)
                line.robot_controller.set_angular(-0.6)
                line.robot_controller.drive()

                if time.time() - turn_time > 0:
                    break

            while not rospy.is_shutdown():
                line_stop = 0
                print "left"
                cx = (line.cx_white + 170) / 2 - 230
                err = -float(cx) / 100
                rate = rospy.Rate(20)

                if stop_line.area > 11000:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_count", stop_line_count
                    rospy.sleep(3)

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.6)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.6)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()

                if stop_line_count == 7:
                    return 'success'
                    break

        rospy.spin()

class T_course(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

    def execute(self, ud):
        right_lane=Right_lane_follower()
        line = LineTracer2()
        stop_line = DetectStopLine()
        stop_line_count = 7
        stop_sign_count=0
        tmp_time = time.time() + 0.1
        start_time = time.time() + 7
        go = Go_7sec()
        box=Detectbox()
        sign=Detect_Sign()
        turn_time = time.time() + 100000
        change_right_follow = time.time() + 100000
        right_follow_time=time.time()+10000

        while not rospy.is_shutdown():
            go.robot_controller.set_angular(0.1)
            go.robot_controller.set_velocity(0)
            go.robot_controller.drive()
            if time.time() - tmp_time > 0:
                break

        while not rospy.is_shutdown():
            go.robot_controller.set_angular(0)
            go.robot_controller.set_velocity(1)
            go.robot_controller.drive()
            if time.time() - start_time > 0:
                break

        while not rospy.is_shutdown():

            rate = rospy.Rate(20)
            while not rospy.is_shutdown():
                print "leftfollow"
                cx=(line.cx_white+170)/2-230
                err=-float(cx)/100
                rate = rospy.Rate(20)

                if stop_line.area>11000:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_count",stop_line_count
                    rospy.sleep(3)

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.8)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.8)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()

                if stop_line_count==8:
                    turn_time = time.time() + 12
                    print "break"
                    break

            while not rospy.is_shutdown():

                line.robot_controller.set_angular(0.2)
                line.robot_controller.set_velocity(0.6)
                line.robot_controller.drive()

                if time.time() - turn_time > 0:
                    line.robot_controller.set_angular(0)
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.drive()
                    break

            while True:
                print "leffollow"
                cx = (line.cx_white + 170) / 2 - 230
                err = -float(cx) / 100
                rate = rospy.Rate(20)
                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.8)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.8)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()

                if len(sign.contours) > 0:  # stop_sign_detect
                    print "stop"
                    stop_sign_count = stop_sign_count + 1
                    print stop_sign_count
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    rospy.sleep(3)

                if stop_sign_count == 1:
                    right_follow_time = time.time() + 20
                    break

            while True:
                rate = rospy.Rate(20)
                print "rightfollow"
                cx = (150 + right_lane.cx_yellow) / 2 - 230
                err = -float(cx) / 100

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.9)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.9)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()

                if box.range_ahead <1.0 and box.range_right<1.2: #box detect
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    line.robot_controller.drive()
                    rospy.sleep(1)

                if time.time() - right_follow_time >0:
                    break

            while True:
                print "leffollow"
                cx = (line.cx_white + 170) / 2 - 230
                err = -float(cx) / 100
                rate = rospy.Rate(20)
                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.8)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.8)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()

                if stop_line.area>11500:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_count",stop_line_count
                    rospy.sleep(3)

                if stop_line_count==9:
                    print "break"
                    break
            return 'success'

class Last_course(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

    def execute(self, ud):
        line = LineTracer2()
        stop_line = DetectStopLine()
        stop_line_count = 0
        turn_time = time.time() + 12.5

        while not rospy.is_shutdown():
            while True:
                line.robot_controller.set_velocity(0.7)
                line.robot_controller.set_angular(-0.3)
                line.robot_controller.drive()

                if time.time() - turn_time > 0:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    line.robot_controller.drive()
                    break
            while True:
                print "go"
                cx = (line.cx_yellow + line.cx_white) / 2 - 230
                err = -float(cx) / 100

                if stop_line.area > 2000:
                    line.robot_controller.set_velocity(0)
                    line.robot_controller.set_angular(0)
                    stop_line_count = stop_line_count + 1
                    print('stop!')
                    print "stop_line_count", stop_line_count
                    break

                if abs(err) < 0.5:
                    line.robot_controller.set_velocity(0.7)
                if abs(err) >= 0.5:
                    line.robot_controller.set_velocity(0.7)
                line.robot_controller.set_angular(err)
                line.robot_controller.drive()
            break