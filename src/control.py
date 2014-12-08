#!/usr/bin/python

import rospy
import baxter_interface
import roslib
from pid import PID
from hotshot.msg import centeringDirection
x_pid = PID()
y_pid = PID()
roslib.load_manifest('joint_position')
holdlocation=False
limb = baxter_interface.Limb('right')
X = 'right_s0'
Y = 'right_s1'
def invalid_data(data):
    return False #todo, filter

def current_angle(joint):
    return limb.joint_angles()[joint] #simple facade

def move_direction(joint, incr_value):
    old_location = limb.joint_angles()[joint]
    new_location += incr_value
    rospy.loginfo('Moving joint %s from old location %d to new location %d' % (joint, old_location, new_location))
    limb.joint_angles()[joint] = new_location
    
def process_imagelocation(data):
    if not hold_location:
        if not invalid_data(data):
            rospy.loginfo("Some sort of invalid data was caught by the filter.")
            return
        rospy.loginfo("Goal heard (x,y):", data.deltaX, data.deltaY)
        x_pid.setPoint(data.deltaX)
	y_pid.setPoint(data.deltaY)
	x_pid.update(current_angle(X))
	y_pid.update(current_angle(Y))
	# math logic goes here -- track difference between current center and found
        move_direction(X, data.deltaX)
        move_direction(Y, data.deltay)
    else:
        rospy.loginfo("Holding location currently.")

def main():
    rospy.loginfo("Initializing control node...")
    rospy.init_node('hotshot_control')
    
    rospy.loginfo("Subscribing to hotshot_goal topic...")
    rospy.Subscriber("/centering", centeringDirection, process_imagelocation)
    
    rs = baxter_interface.RobotEnable()
    rospy.loginfo("Enabling robot, if not enabled...")
    rs.enable()
    
    rospy.spin()     # spin() simply keeps python from exiting until this node is stopped
    
"""
So, guys, some quick thoughts on this.

We need a filter to make sure that invalid object recognition messages don't make baxtor slap someone in the face or something. 
We need a 
"""

