import rospy
import baxter_interface
from std_msgs.msg import Point
import roslib

roslib.load_manifest('joint_position')
holdlocation=False
limb = baxter_interface.Limb('right')

def invalid_data(data):
    return False #todo, filter

def current_angle(joint):
    return limb.joint_angles()[joint] #simple facade

logged_moves = []
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
        rospy.loginfo("Goal heard (x,y):", data.x, data.y)
        # math logic goes here -- track difference between current center and found
        move_direction('right_s0', data.x)
        move_direction('right_s1', data.y)
    else:
        rospy.loginfo("Holding location currently.")

def main():
    rospy.loginfo("Initializing control node...")
    rospy.init_node('hotshot_control')
    
    rospy.loginfo("Subscribing to hotshot_goal topic...")
    rospy.Subscriber("/hotshot_goal", Point, process_imagelocation)
    
    rs = baxter_interface.RobotEnable()
    rospy.loginfo("Enabling robot, if not enabled...")
    rs.enable()
    
    rospy.spin()     # spin() simply keeps python from exiting until this node is stopped
    
"""
So, guys, some quick thoughts on this.

We need a filter to make sure that invalid object recognition messages don't make baxtor slap someone in the face or something. 
We need a 
"""

