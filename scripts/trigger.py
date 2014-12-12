#!/usr/bin/env python                                                   
                                                                            
import serial                                                
def fire():
	port = serial.Serial("/dev/ttyACM0", 9600)                         
	port.write('f')                                         
	port.close()
if __name__ == '__main__':
	fire()
