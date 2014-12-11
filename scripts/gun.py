#!/usr/bin/env python

import serial

port = serial.Serial("/dev/ttyACM0", 9600)

def calibrate():
    ser.write(bytes("d".encode('ascii')))
    ser.write(bytes("a".encode('ascii')))
    pass

def fire():
    port.write(bytes("f".encode('ascii')))

calibrate();
fire();
