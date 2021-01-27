# -*- coding: utf-8 -*-
"""
Description:
Gesture sensor APDS9960 demo, using led class indicator

Dependencies:
sudo pip install apds9960

Use:
python3 gest1.py
"""
from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus
from time import sleep
import time
import ledClass as leds

port = 1
bus = smbus.SMBus(port)

apds = APDS9960(bus)

def intH(channel):
    print("INTERRUPT")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

dirs = {
    APDS9960_DIR_NONE:  "none",
    APDS9960_DIR_LEFT:  "left",
    APDS9960_DIR_RIGHT: "right",
    APDS9960_DIR_UP:    "up",
    APDS9960_DIR_DOWN:  "down",
    APDS9960_DIR_NEAR:  "near",
    APDS9960_DIR_FAR:   "far",
}
   
###################
## MAIN FUNCTION ##
###################
def main():
    ## CLASS INSTANTIATION ##
    LEDS = leds.LEDClass()                              # LED control class 
    
    try:
        # Interrupt-Event hinzufuegen, steigende Flanke
        GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)

        apds.setProximityIntLowThreshold(50)

        print("Gesture Test")
        print("============")
        apds.enableGestureSensor()
        while True:
            time.sleep(0.5)
            if apds.isGestureAvailable():
                motion = apds.readGesture()
                #print("Gesture={}".format(dirs.get(motion, "unknown")))
                direction = dirs.get(motion, "unknown")

                if direction == "left":
                    LEDS.Blink_1()
                    print("motion left")
                elif direction == "right":
                    LEDS.Blink_2()
                    print("motion right")
                elif direction == "up":
                    LEDS.Blink_3()
                    print("motion up")
                elif direction == "down":
                    LEDS.Blink_4()
                    print("motion down")

    finally:
        LEDS.cleanIO()
        print ("Cleanup and exit...")


if __name__ == "__main__":  main()
