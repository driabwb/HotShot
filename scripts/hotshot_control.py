#!/usr/bin/python
import rospy
import baxter_interface
import roslib; roslib.load_manifest('hotshot')
from hotshot.msg import centeringDirection
def set_unimportant():
	rospy.loginfo('setunimportant')
	angles = baxter_interface.Limb('right').joint_angles()
	angles['right_e0']=0.0
	angles['right_e1']=0.0
	angles['right_w0']=0.0
	angles['right_w1']=0.0
	angles['right_w2']=0.0
	baxter_interface.Limb('right').set_joint_positions(angles)

class _P:
	def __init__(self, nm,P=.0008):
		self.name=nm
		self.Kp=P
		self.set_point=0.0
		self.error=0.0
		self.new = 0.0

	def update(self,current_value):
		self.last=self.new
		self.error = self.set_point - current_value
		self.new = self.Kp * self.error
		rospy.loginfo("Updating joint %s from %f to value %f"
                        % (self.name, self.last, self.new))
		return self.new
		
	def setPoint(self,set_point):
		self.set_point = set_point


hold_location=False
rate=.1
X = 'right_s0'
Y = 'right_s1'
Ps= { X:_P('x'), Y:_P('y') }
	
def within_circle(data):
    return 900 < (data.deltaX**2 + data.deltaY**2)**0.5

def current_angle(joint):
    return baxter_interface.Limb('right').joint_angles()[joint] #simple facade

def move_direction(joint, upd):
	p=Ps[joint]
	p.setPoint(upd)
	new_value = p.update(current_angle(joint))
	new_angles = baxter_interface.Limb('right').joint_angles()
	new_angles[joint] = new_value
        new_angles['right_e0']=0.0
	new_angles['right_e1']=0.0
	new_angles['right_w0']=0.0
	new_angles['right_w1']=0.0
	new_angles['right_w2']=0.0
	baxter_interface.Limb('right').set_joint_positions(new_angles)

def update(data):
    if not hold_location:
   
	if within_circle(data):
            rospy.loginfo("Within circle.")

            return
        rospy.loginfo("Goal heard (%d, %d):" % (data.deltaX, data.deltaY))
        move_direction(X, float(data.deltaX))
        move_direction(Y, float(data.deltaY))
	set_unimportant()
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
    set_unimportant()
    while not rospy.is_shutdown():
    	rospy.spin()

if __name__ == '__main__':
    main()
