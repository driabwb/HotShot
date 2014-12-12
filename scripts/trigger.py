#!/usr/bin/env python                                                   
  	#untested, 10 second adaption ofprior code. I'd assume already tried but worth a shot.
import rospy
import serial 
from std_msgs.msg import Bool

def fire(data):
	rospy.loginfo("I heard a fire command")
	port = serial.Serial("/dev/ttyACM0", 9600)                         
	port.write('f')                                         
	port.close()

def listener():
    rospy.init_node('node_name')
    rospy.Subscriber("/fire_command", Bool, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
	fire()
