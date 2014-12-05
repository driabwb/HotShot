#! /usr/bin/python


import rospy
import roslib
import baxter_interface
roslib.load_manifest('joint_position')

def movement():
    right = baxter_interface.Limb('right')
    


def main():
    print("Initializing node...")
    rospy.init_node("hot_shot_move_robot")
    print("Getting robot state...")
    rs = baxter_interface.RobotEnable()
    print("Enabling robot...")
    rs.enable()

