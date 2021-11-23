#! /usr/bin/env python

import smach_ros
from smach import StateMachine
from robot_state import *


if __name__ == '__main__':
    rospy.init_node('Drive')

    DrivingMachine=StateMachine(outcomes=['success'])
    with DrivingMachine:
        StateMachine.add('BLOCKING_BAR', BlockingBarState(), transitions={'success': 'LINETRACE'})
        StateMachine.add('LINETRACE',LineTrace(),transitions={'success': 'STOP_LINE2_SECTION'})
        StateMachine.add('STOP_LINE2_SECTION', StopLine2_section(), transitions={'success': 'GO_7SEC'})
        StateMachine.add('GO_7SEC', Go_7sec_class(), transitions={'success': 'S_course'})
        StateMachine.add('S_course', S_course(), transitions={'success': 'T_course'})
        StateMachine.add('T_course', T_course(), transitions={'success': 'success'})
    DrivingMachine.execute()
    rospy.spin()
