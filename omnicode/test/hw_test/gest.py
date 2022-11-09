"""
Description:
Simple directional test of the APDS9960 gesture sensor

Dependencies:
sudo pip install apds9960 
"""

from apds9960.const import *
from apds9960 import APDS9960
import smbus
from time import sleep
import sys

port = 1
bus = smbus.SMBus(port)

apds = APDS9960(bus)


###################
## MAIN FUNCTION ##
###################
def main():
    Cnt = 0						# Double defined?
    direct = 'none'				# Direction of swipe
    
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
        ## Threshold does NOTHING ##
        apds.setProximityIntLowThreshold(80)
        apds.setProximityIntHighThreshold(110)
        #apds.setGestureProximityThreshold(50)

        
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
                direct = dirs.get(motion, "unknown")
                print("Gesture = {}".format(direct))
                print("PCBoard Count = {}".format(Cnt))
                
                if direct == "none":
                    Cnt += 1					# increment board count
                    #print("up1")                 ## Upper limit? ##
                    
                if direct == "left":
                    Cnt += 1					# increment board count
                    #print("up2")                 ## Upper limit? ##
                    
                elif direct == "up":
                    Cnt += 1					# increment board count
                    #print("up3")                 ## Upper limit? ##
                    
                elif direct == "right":
                    Cnt += 1					# increment board count
                    #print("up4")                 ## Upper limit? ##
                    
                elif direct == "down":
                    ## Avoid negative situations ##
                    if Cnt > 0:
                        Cnt -= 1
                        #print("Remove a board!!")

        # Ctrl+C will exit the program correctly
    except KeyboardInterrupt:
        print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
        sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":  main()
