#!/usr/bin/python3
##NOTE PYTHON3
import rospy
import baxter_interface
import roslib; roslib.load_manifest('hotshot')
from hotshot.msg import centeringDirection

class _P:
	def __init__(self, nm,P=1):
		self.name=n
		self.Kp=P
		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		self.last=self.new
		self.error = self.set_point - current_value
		self.new = self.Kp * self.error
		rospy.loginfo("Updating joint %s from %d to value %d" % (self.name, self.last, self.new))
		return self.new
		
	def setPoint(self,set_point):
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

hold_location=False
rate=.1
RIGHT = baxter_interface.Limb('right')
LEFT =  baxter_interface.Limb('left')
CURRENT
X = 'right_s0'
Y = 'right_s1'
Ps= { X:_P(), Y:_P() }
	
def invalid_data(data):
    return False #todo, filter

def current_angle(joint):
    return CURRENT.joint_angles()[joint] #simple facade

def move_direction(joint, upd):
	p=Ps[joint]
	p.setPoint(upd)
	new_value = p.update(current_angle(joint))
	new_angles = CURRENT.joint_angles()
	new_angles[joint] = new_value
	CURRENT.set_joint_positions(new_value)

def update(data):
    if not hold_location:
        if invalid_data(data):
            rospy.loginfo("Some sort of invalid data was caught by the filter.")
            return
        rospy.loginfo("Goal heard (x,y):", data.deltaX, data.deltaY)
        move(X, data.deltaX)
        move(Y, data.deltaY)
    else:
        rospy.loginfo("Holding location currently.")

def main():
    rospy.loginfo("Initializing control node...")
    rospy.init_node('hotshot_control')
    rospy.get_param('image_channel')
    rospy.loginfo("Subscribing to hotshot_goal topic...")
    rospy.Subscriber("/centering", centeringDirection, update)
    
    rs = baxter_interface.RobotEnable()
    rospy.loginfo("Enabling robot, if not enabled...")
    rs.enable()
    while True:
    	rospy.spin()

if __name__ == '__main__':
	main()
