#!/bin/bash

#Note: ran full upgrades + install "xterm"

# Command to be executed in xterm:
DISPLAY=:0 xterm -hold -e bash -c "python /home/pi/main/main.py"  &