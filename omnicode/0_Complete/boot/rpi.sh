#!/bin/bash

# Pasword: "omnigo"

## COPY FILE TO PI ##
scp /home/antz/Desktop/temp/omnigo/boot/boot.sh pi@192.168.0.191:/home/pi/
scp /home/antz/Desktop/temp/omnigo/boot/crontab.txt pi@192.168.0.191:/home/pi/

## COPY FILE TO PI ##
#scp /home/antz/Desktop/temp/omnigo/boot/boot.sh pi@192.168.0.167:/home/pi/
#scp /home/antz/Desktop/temp/omnigo/boot/crontab.txt pi@192.168.0.167:/home/pi/