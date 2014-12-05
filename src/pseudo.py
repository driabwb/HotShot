# make sure baxter is enabled: 
# $ rosrun baxter_tools enable_robot.py -e

import rospy
import baxter_interface
from std_msgs.msg import Point
from pid import PID

limb = baxter_interface.Limb('right')
yaw_pid = PID()
pitch_pid = PID()

def process_imagelocation(data):
    rospy.loginfo("Goal heard (x,y):", data.x, data.y)
    yaw_pid.setPoint(current_value=data.x)
    pitch_pid.setPoint(current_value=data.y)

def process_centerupdate(data):
    angles = limb.joint_angles()
    rospy.loginfo("Center heard x %d, y %d" % data.x, data.y)
    angles['right_s0'] = yaw_pid.update(current_value=data.x)
    angles['right_s1'] = pitch_pid.update(current_value=data.y)
    limb.move_to_joint_positions(angles)
 
def listener():
    rospy.init_node('baxter_controller')
    rospy.Subscriber("/centering_msg", Point, process_centerupdate)
    rospy.Subscriber("/hotshot_goal", Point, process_imagelocation)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
