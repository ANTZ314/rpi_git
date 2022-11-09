"""
Description:
Simple directional test of the APDS9960 gesture sensor

Dependencies:
sudo pip install apds9960 
"""

from apds9960.const import *
from apds9960 import APDS9960
#import RPi.GPIO as GPIO
import smbus
from time import sleep
import sys

port = 1
bus = smbus.SMBus(port)

apds = APDS9960(bus)

def main():
    Cnt = 0                     # Double defined?

    dirs = {
        APDS9960_DIR_NONE: "none",
        APDS9960_DIR_LEFT: "left",
        APDS9960_DIR_RIGHT: "right",
        APDS9960_DIR_UP: "up",
        APDS9960_DIR_DOWN: "down",
        APDS9960_DIR_NEAR: "near",
        APDS9960_DIR_FAR: "far",
    }
    try:
        #apds.setProximityIntLowThreshold(50)
        apds.setProximityIntLowThreshold(80)
        apds.setProximityIntHighThreshold(110)

        print("Gesture Test")
        print("============")
        apds.enableGestureSensor()
        apds.setGestureEnterThresh(90)
        apds.setGestureExitThresh(100)
        apds.clearAmbientLightInt()
        apds.setGestureLEDDrive(3)

        while True:
            sleep(0.5)
            if apds.isGestureAvailable():
                motion = apds.readGesture()
                #print("Gesture = {}".format(dirs.get(motion, "unknown")))
                Cnt += 1
                print("Count: {}".format(Cnt))


    finally:
        #GPIO.cleanup()
        print ("Bye")
        sys.exit(0)


if __name__ == "__main__":  main()