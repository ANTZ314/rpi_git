"""
Adafruit Examples:
https://learn.adafruit.com/adafruit-apds9960-breakout/circuitpython
"""

##------------------------------------------------------------##

from board import SCL, SDA
import busio
from adafruit_apds9960.apds9960 import APDS9960
 
i2c = busio.I2C(SCL, SDA)
 
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True
 
# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE
 
while True:
    gesture = apds.gesture()
 
    if gesture == 0x01:
        print("up")
    elif gesture == 0x02:
        print("down")
    elif gesture == 0x03:
        print("left")
    elif gesture == 0x04:
        print("right")


##------------------------------------------------------------##

import board
import busio
import adafruit_apds9960.apds9960
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_gesture = True

gesture = sensor.gesture()
while gesture == 0:
    gesture = sensor.gesture()
print('Saw gesture: {0}'.format(gesture))


##------------------------------------------------------------##