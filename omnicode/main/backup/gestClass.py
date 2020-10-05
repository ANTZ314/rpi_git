#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
Simple directional test of the APDS9960 gesture sensor

Dependencies:
sudo pip install apds9960 
"""
import traceback
from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep

class gestClass:
    port = 1
    bus  = smbus.SMBus(port)
    apds = APDS9960(bus)
    
    def intH(channel):
        print("INTERRUPT")          # for what?
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    
    def __init__(self, **kwargs):
        print("Gesture Sensor is GO!!")
        
    def get_gesture(self):
        exitCnt = 0
        exitKey = 'n'
        
        try:
            dirs = {
                APDS9960_DIR_NONE:  "none",
                APDS9960_DIR_LEFT:  "left",
                APDS9960_DIR_RIGHT: "right",
                APDS9960_DIR_UP:    "up",
                APDS9960_DIR_DOWN:  "down",
                APDS9960_DIR_NEAR:  "near",
                APDS9960_DIR_FAR:   "far",
            }
            try:
                # Interrupt-Event [add rising edge??]
                GPIO.add_event_detect(7, GPIO.FALLING, callback = self.intH)
                self.apds.setProximityIntLowThreshold(50)
                
                print("CAPTURE GESTURES:")
                print("=================")
                self.apds.enableGestureSensor()
                while True:
                    sleep(0.5)
                    if self.apds.isGestureAvailable():
                        motion = self.apds.readGesture()
                        print("Gesture = {}".format(dirs.get(motion, "unknown")))
                        if exitCnt == 5:
                            print("Exit gesture Counting: y/n")
                            exitKey = raw_input()   # get exit code
                            exitCnt = 0             # clear counter
                        exitCnt += 1
                    if exitKey == 'y':
                        break
            finally:
                GPIO.cleanup()
                print ("Exit gesture class!")
            
                    
        # Any Main Errors saved to log.txt file:
        except Exception:
            log = open("log.txt", 'w')
            traceback.print_exc(file=log)
            print ("main gesture error")
