#!/usr/bin/python
import rospy
import baxter_interface
import roslib; roslib.load_manifest('hotshot')
from hotshot.msg import centeringDirection

hold_location=False
rate=.1
X = 'right_s0'
Y = 'right_s1'

	
def within_circle(xpos, ypos):
    return 10 > (xpos**2 + ypos**2)**0.5

def current_angle(joint):
    return baxter_interface.Limb('right').joint_angles()[joint] #simple facade

def move_direction(joint, upd):
	new_value = p.update(current_angle(joint))
	new_angles = baxter_interface.Limb('right').joint_angles()
	new_angles[joint] = new_value
        new_angles['right_e0']=0.0
	new_angles['right_e1']=0.0
	new_angles['right_w0']=0.0
	new_angles['right_w1']=0.0
	new_angles['right_w2']=0.0
	baxter_interface.Limb('right').set_joint_positions(new_angles)
HOLD_LOCATION = {'value':False}
def update(data):
    if not HOLD_LOCATION['value']:
	factor = -.01
	x_movement = 1
	y_movement = -1
	xpos = data.deltaX
	ypos = data.deltaY - 50
   	if xpos > 0:
		x_movement = -1
	if ypos > 0:
		y_movement = 1
	if within_circle(xpos, ypos):
	    HOLD_LOCATION['value'] = True
            rospy.loginfo("Within circle.")
            return
        rospy.loginfo("Goal heard (%d, %d):" % (xpos, ypos))
	new_angles = baxter_interface.Limb('right').joint_angles()
	new_angles[X] += x_movement * factor
	new_angles[Y] += y_movement * factor
        new_angles['right_e0']=0.0
	new_angles['right_e1']=0.0
	new_angles['right_w0']=0.0
	new_angles['right_w1']=0.0
	new_angles['right_w2']=0.0
	baxter_interface.Limb('right').set_joint_positions(new_angles)
    else:
        rospy.loginfo("Holding location currently.")


def main():
	rospy.loginfo("Initializing control node...")
	rospy.init_node('hotshot_control')
	#rospy.get_param('image_channel')
	rospy.loginfo("Subscribing to hotshot_goal topic...")
	rospy.Subscriber("/centering", centeringDirection, update)
	rs = baxter_interface.RobotEnable()
	rospy.loginfo("Enabling robot, if not enabled...")
	rs.enable()
	while not rospy.is_shutdown():
		rospy.spin()

if __name__ == '__main__':
    main()
