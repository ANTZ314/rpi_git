#!/bin/bash

######################
## Make executable: ##
#chmod u+x hello-world

## Get Ip Address: ##
# hostname -I

## SSH: ##
# ssh pi@192.168.0.xxx

######  Usage: ######
# cd ~/Desktop/temp/
# ./rpi.sh
#####################

##########
# FROM PI:
##########

## FILE ##
#scp pi@192.168.0.188:/home/pi/screen.png /home/antz/Desktop/

## FOLDER ##
#scp -r pi@192.168.0.104:/home/pi/main3 /home/antz/Desktop/

##########
# TO PI:
##########

## FILE ##
scp /home/antz/Desktop/temp/omnigo/main/main.py pi@192.168.0.188:/home/pi/main/

## FOLDER ##
#scp -r /home/antz/Desktop/iot/main pi@192.168.1.110:/home/pi/



###############################
# MULTIPLE FILES TO MULTI-RPIs:
###############################

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.150:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.151:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.152:/home/pi/main/

##scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.153:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.154:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.155:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.156:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.157:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.158:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.159:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.160:/home/pi/main/

#scp /home/antz/Desktop/temp/omnigo/main/main.py pi@172.17.30.161:/home/pi/main/