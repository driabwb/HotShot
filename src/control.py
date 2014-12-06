import rospy
import baxter_interface
from std_msgs.msg import Point
import roslib

roslib.load_manifest('joint_position')

limb = baxter_interface.Limb('right')
def invalid_data(data):
    return False #todo, filter

def current_angle(joint):
    return limb.joint_angles()[joint] #simple facade

def move_direction(joint, incr_value):
    limb.joint_angles()[joint] += incr_value
    
def process_imagelocation(data):
    if not invalid_data(data):
        rospy.loginfo("Some sort of invalid data was caught by the filter.")
        return
    rospy.loginfo("Goal heard (x,y):", data.x, data.y)
    move_direction('right_s0', data.x)
    move_direction('right_s1', data.y)
 
def main():
    rospy.loginfo("Initializing control node...")
    rospy.init_node('hotshot_control')
    
    rospy.loginfo("Subscribing to hotshot_goal topic...")
    rospy.Subscriber("/hotshot_goal", Point, process_imagelocation)
    
    rs = baxter_interface.RobotEnable()
    rospy.loginfo("Enabling robot, if not enabled...")
    rs.enable()
    
    rospy.spin()     # spin() simply keeps python from exiting until this node is stopped

