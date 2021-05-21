#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author:
	Antony Smith - T.S.E. [August 2020]

NOTE:
	-> All windows crashing when code required for stage change
	-> Removed for this version - can be found in "main2.py"

Description:
	GCP MQTT to SIATIK GC-Platform
	Main control GUI for Omnigo IoT project
	Raspberry Pi Zero + PiCamera + APDS9960

Primary Functions:
	GUI functionality:
		-> Widget placement + Colour schemes			- [complete]
		-> Real-time label udpates (count/info)			- [complete]
		-> Multi-Threading								- [complete]
		-> multiple windows in parallel operation		- [complete]
	APDS9960 gesture sensor counting method 			- [complete]
	PiCamera & OPENCV QR Code reading					- [complete]
	Scan Kit & Staff ID + storage method				- [complete]
	Exit code required to leave GUI						- [complete]
	Drop-down menu stage selector						- [complete]
	JSON data format conversion							- [complete]
	Upload data to Google Cloud IoT-Core [SIATIK]		- [complete]
	Indicator LED (counting=GREEN)						- [complete]

Change from main21:
	Continue counting & Catch up publishes				- [complete]
	Kit / Staff ID - Scanned in any order				- [complete]
	QR time-out -> back to scan button					- [complete]
	Check video frame - FULL SCREEN						- [incomplete]
	Clear message - [INFO] network error				- [incomplete] 
	Remove both test functions + ALL comments			- [incomplete]

--------------------------------------
FINAL CLEANUP:
	Remove all unneccessary prints
	Check for unused variables/flags
	Remove commented lines
	Remove test functions
--------------------------------------

Notes:
	GUI EXIT CODE: 	3529# ('*' to Delete)
	STAGE CODE: 	2580# ('*' to Delete)
	QR-Code scanner:
		-> Exits after 3x confirmed QR reads
		-> Time-Out after 35 seconds
		-> 'q' to exit prematurely
	GCP connectivity requirements:
		-> 'jwt_maker.py' to create JWT security key
		-> ssl security files: 
			=> roots.pem
			=> rsa_private.pem

USAGE:
	python main.py
"""
###################
# import packages #
###################

## GUI PACKAGES ##
from Tkinter import *					# GUI package
import tkFont							# GUI package
from functools import partial			# passing argument to button?

## MULTI-TASKING FUNCTIONS ##
import threading						# Multi-Threading
import multiprocessing

## GENERAL MAINTENANCE ##
import sys, os							# Possibly remove ? ? ?
import time								# time travel
import traceback						# Error logging
import datetime							# Get real-time data
from gpiozero import LED 				# Import GPIO library

## 	QR CODE IMPORTS ##
from picamera import PiCamera			# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar				# Decoding the QR Code
import imutils 							# A little slice of Magic
import cv2								# When you stare into the matrix...

## GESTURE IMPORTS ##
from apds9960.const import *
from apds9960 import APDS9960
import smbus

## JSON & GCP ##
import json								# JSON conversion functions
import jwt								# Create JSON security token 
import paho.mqtt.client as mqtt			# MQTT connectivity
import requests							# 
import base64							# 


###################
##  GLOBAL DEFS  ##
###################
btn_state1 = 0										# changed to tri-state (0/1/2)
csv_file = "barcodes.csv"							# guess what this is?
OptionList = ["SETUP","THRU","SMT","INSP","EXIT"] 	# Drop Down Menu Options

## Gesture Sensor Hardware Requirements ##
port = 1
bus  = smbus.SMBus(port)
apds = APDS9960(bus)

## Define Indicator LED BCM.GPIO pins ##
## NOTE: GPIO 12/13/16 are unusable?? ##
RED 	= LED(5)									# BUSY
GREEN 	= LED(6)									# FREE


###################
## MAIN FUNCTION ##
###################
def main():
	global thr1										# Thread1 flag - Gesture Counting 
	global Cnt										# PCB count value
	global GestDone									# Exit Gesture flag
	global QRDone									# Exit QR Scan flag
	global pin	 									# Exit Code Value
	global CodeDone									# Exit Code - flag
	global qrData									# Get QR Data
	global iotJSON									# Converted to JSON format
	global firstScan								# (createJSON) - store certain data on first scan
	global strtstp									# (createJSON) - project start or stop
	global staffID									# (createJSON) - Extracted Staff ID
	global pubNow									# Publish flag
	global fail										# 
	
	lay=[]											# layering windows??
	CodeDone = False								# Exit Code - negative
	pin  = ''										# Exit Code - blank string
	QRDone   = False								# QR Scan 	- flag
	Cnt = 0											# PCB Counter start value
	info = "feedback..."							# GUI feedback information - OPTIONAL
	ID_match = 0									# ID Scan - initial staff ID status
	qrData = "data from qr code"					# initialise to string format
	iotJSON = "upload"								# initialise to string format
	firstScan = 0									# initialise for 1st data update
	staffKit = 0									# initialise to kit_ID 1st
	failFile = '/home/pi/main/fail.txt'				# If count is interupted - continue
	
	## GCP PROJECT VARIABLES - SIATIK ##
	#ssl_private_key 		 = './certs/rsa.pem'	# '<ssl-private-key-filepath>'
	ssl_private_key 		 = '/home/pi/main/certs/rsa.pem'# '<ssl-private-key-filepath>'
	ssl_algorithm            = 'RS256'              # '<algorithm>' -> RS256 or ES256
	project_id               = 'omnigo'             # '<GCP project id>'
	
	## Project Information Dictionary ##
	global dataDict
	dataDict = {'CLIENT'	: 'xxx',				# Client Name
				'PROJECT'	: '0',					# Project ID
				'STAGE'		: 'xxx',				# Operational Stage (setup/smt/thru/insp)
				'BOARDS'	: '0',					# Total Number PC-Boards
				'PANELS'	: '0',					# Total Number of panels
				'COUNT'		: '0',					# Actual Board Count
				'STAFF_ID'	: '0',					# Staff member ID number
				'DATE'		: '00-00-2020',			# Project start date
				'TIME'		: '00:00',				# Time of each board swiped
				'START'		: '00:00',				# Stage - start time 
				'STOP'		: '00:00',				# Stage - end time
				'REASON'	: 'null',				# Reason the stage was stopped
				'SERIAL'	: '0' }					# Barcode serial number - Later

	## Get the current time/date ##
	cur_time = datetime.datetime.utcnow()
	
	try:
		try:
			thr1 = 0								# thread 1 flag
			###############################
			## TEST FUNCTION - TEMPORARY ##
			###############################
			def fake_scan():
				ender = 0
				global QRDone				# Exit Scan loop
				global qrData
				global staffID
				global firstScan
				global projStat
				global qr_time
				
				## Button click to exit? ##
				while QRDone == False:
					ender += 1
					print("..-SCANNING-..")
					time.sleep(1)
					if ender == 3:
						QRDone = True
				
				qrData = "CLIENT=Omnigo,PROJECT=123456,STAGE=SETUP,BOARDS=1000,PANELS=50,COUNT=0,STAFF_ID=357,TIME=00:00,DATE=01-01-2000,START=00:00,STOP=00:00,REASON=NULL,SERIAL=987654321"
				staffID = 357	# fake staff ID
				firstScan = 0	# update first data
				print("Extracted Data String")
				ender = 0		# Go Again
				QRDone = False	# Go Again
				qr_time = True
			

			###############################
			## DEMO FUNCTION - TEMPORARY ##
			###############################
			def fake_gesture():
				global Cnt					# Double defined?
				global GestDone				# Exit Gesture loop
				global strtstp				# Start Stop times
				
				Cnt = 0						# initialised
				strtstp = 0					# start time
				GestDone = False

				## Button click to exit? ##
				while GestDone == False:
					## ~SWIPE~ ##
					Cnt += 1				# increment board count
					
					## Continuously update GUI Label ##
					update_label()
						
					## ON EVERY COUNT ##
					handleData(Cnt)
					time.sleep(5)			# every 3 seconds
				
				time.sleep(1)				# wait
				print("Last PUBLISH")		# REMOVE
				## Publish Stop Time ##
				strtstp = 2					# stop time
				handleData(Cnt)				# create & publish
				print("Count Complete")		# REMOVE
			
			
			#########################
			## COUNT FAILURE CHECK ##
			#########################
			def failCheck(Cnt):
				exists = False										# file exists or not?
				contCnt = 'x'										# stored json string
				
				## Try to read file ##
				try:												# Skip if file doesn't exist
					file = open(failFile, 'r') 						# Open to read file
					contCnt = file.read()							# read file contents
					#print("STORED: {}".format(contCnt))			# REMOVE
					file.close()									# Close the file
				## Create - No File to Read ##
				except:
					exists = True									# Avoid writing twice if file exists
					contCnt = '0'									# Set to Zero
					#print("STORE 0")								# REMOVE
					file = open(failFile,"w")						# Create/Open file then write data 
					file.write(contCnt) 							# write first zero
					file.close()									# Exit the opened file
				## Seen File - Now overwrite ##
				if exists == False:									# overwrite data after printing contents
					if  Cnt != 0:									# Only if count is already going
						#print("STORE {}".format(str(Cnt)))			# REMOVE
						file = open(failFile,"w")					# Open file then Overwrite data 
						file.write(str(Cnt))						# Write new string
						file.close()								# Exit the opened file
				## Notify File Created - ROMOVE ##
				#else:												# 
				#	print "Start Click -> Create New Fail File!"	# REMOVE
				
				return contCnt										# Return last count value
			
			
			################
			## QR SCANNER ##
			################
			def QR_Scan():
				global qrData									# globalise QR Data
				global staffID									# Extracted Staff ID
				global qr_time									# QR Scan timed out before complete
				init_time = time.time()							# No. of secs since 1 Jan 1970
				winName   = "SCAN-ID"							# Name the video window
				scnCnt 	  = 0									# Number of ID confirmations
				done 	  = "kit"								# which scan is complete
				staffKit  = 0									# Which ID - kit_ID[0] / Staff_ID[1]
				qr_time   = False								# initially unsuccessful
				
				## initialize video stream & warm up camera sensor
				print("[INFO] starting video stream...")
				vs = VideoStream(usePiCamera=True).start()
				time.sleep(2.0)									# Allow video to stabalise
				cv2.namedWindow(winName)
				cv2.moveWindow(winName, 1,1)
				
				## Loop over the frames from the video stream #
				## Time-Out after 35 secs ##
				while time.time()-init_time < 35:
					## grab the frame from the threaded video stream and r
					## resize it to have a maximum width of 400 pixels
					frame = vs.read()
					frame = imutils.rotate(frame, 90)			# rotate 90 due to camera mount
					frame = imutils.resize(frame, width=400)
					
					## Fullscreen Window ##
					cv2.namedWindow(winName,cv2.WND_PROP_FULLSCREEN)
					cv2.setWindowProperty(winName,cv2.WND_PROP_FULLSCREEN,1)
					
					## find & decode the barcodes in each frame
					barcodes = pyzbar.decode(frame)

					## loop over the detected barcodes
					for barcode in barcodes:
						## extract bounding box location & draw around barcode
						(x, y, w, h) = barcode.rect
						cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
				 
						## the barcode data is a bytes object so if we want to draw it
						## on our output image we need to convert it to a string first
						barcodeData = barcode.data.decode("utf-8")
						barcodeType = barcode.type
				 
						## Indicate Which barcode is found ##
						if staffKit == 0:
							text = "- FIRST ID -"
						else:
							text = "- SECOND ID -"
						
						cv2.putText(frame, text, (x, y - 10),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
							
						## REMOVED - Store QR Data to CSV file ##
						
						## Count QR Reads ##
						scnCnt += 1	
						
						## If QR Code is Read 4 times ##
						if scnCnt == 4:
							## Kit ID Found ##
							if len(barcodeData) > 10:
								#print("Kit Data Found!!")		# REMOVE
								qrData = barcodeData			# Store Kit ID
								staffKit += 1					# Increment
							## Staff ID Found ##
							else:
								#print("Staff ID found!!")		# REMOVE
								staffID = barcodeData			# store staff ID
								staffKit += 1					# Increment
							## If both ID's stored - Exit ##
							if staffKit == 2:
								done = "y" 						# exit scan mode
							
							## QR Image - CHANGE INDICATOR ##
							font = cv2.FONT_HERSHEY_SIMPLEX
							text = "~DONE~"
							textsize = cv2.getTextSize(text, font, 1, 2)[0]
							
							## Get coords based on boundry ##
							textX = (frame.shape[1] - textsize[0]) /4
							textY = (frame.shape[0] - textsize[1]) /2	# was 2
							
							## Add text centered in image ##
							cv2.putText(frame, text, (textX, textY), font, 2, (0, 255, 0), 3)

					## Show the output frame ##
					cv2.imshow(winName, frame)
					key = cv2.waitKey(1) & 0xFF
					
					# Pause for QR swap ##
					if scnCnt == 4:
						time.sleep(3)		
						scnCnt = 0	
				 
					## if the `q` key was pressed, break from the loop ##
					if key == ord("q"):
						break
					## if ID confirmed 3 times ##
					elif done == "y":
						qr_time = True							# Completed successfully
						#print(qrData)							# REMOVE
						#print(staffID)							# REMOVE
						break
				
				## close the output CSV file do a bit of cleanup ##
				print("[INFO] cleaning up...")					# REMOVE
				vs.stop()										# stop video stream
				cv2.destroyAllWindows()							# NOT destroying??
				win.lift()										# Put GUI on the top
				
			
			#####################
			## GESTURE COUNTER ##
			#####################
			def get_gesture():
				global strtstp				# Start/Stop (time) Flag
				global Cnt					# Double defined?
				global GestDone				# Exit Gesture loop
				global pubNow				# Publish trigger
				Cnt = 0						# Double defined?
				direct = 'none'				# Direction of swipe

				pubNow   = False			# already set False in 'handledata'
				GestDone = False			# initialise on function call
				
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
					## Set the proximity threshold ##
					apds.setProximityIntLowThreshold(80)	# No Change?
					apds.setProximityIntHighThreshold(110)	# No Change?
						
					print("COUNT MODE:")					# REMOVE
					print("===========")					# REMOVE
					apds.enableGestureSensor()
					apds.setGestureEnterThresh(100)
					apds.setGestureExitThresh(110)
					apds.clearAmbientLightInt()
					apds.setGestureLEDDrive(3)
					
					## EXIT the Gesture Thread ? ##
					while GestDone == False:				# while True:
						time.sleep(0.5)
						if apds.isGestureAvailable():
							motion = apds.readGesture()
							direct = dirs.get(motion, "unknown")
							#print("Gesture = {}".format(direct))	# REMOVE
							
							if direct == "none":
								Cnt += 1					# increment board count
								## Upper limit? ##
								
							if direct == "left":
								Cnt += 1					# increment board count
								## Upper limit? ##
							
							elif direct == "up":
								Cnt += 1					# increment board count
								## Upper limit? ##
							
							elif direct == "right":
								Cnt += 1					# increment board count
								## Upper limit? ##
							
							elif direct == "down":
								## Avoid negative situations ##
								if Cnt > 0:					
									Cnt -= 1
							
							## Continuously update GUI Label ##
							update_label()

							## Publish on swipe ##
							#handleData(Cnt)				# running as own thread now
							pubNow = True					# Pull the trigger - publish flag
						

				## Do before exiting Gesture Mode ##
				finally:
					## Publish Stop Time ##
					strtstp = 2								# stop time
					#handleData(Cnt)							# create & publish
					pubNow = True								# May have already exitted loop?
					## Zero Counter - On Next Count ##
					Cnt = 0 								# zero the count value
					update_label()							# update the GUI label
					print("Last PUBLISH")					# REMOVE 


			##############################
			## BUTTON: EMPLOYEE ID SCAN ##
			##############################
			def btn_start():
				global strtstp										# Start/Stop (time) Flag
				## Gesture counter ##
				global GestDone										# Exit Gesture mode flag
				global Cnt											# make global again?
				## ID Scanner ##
				global btn_state1									# changed to tri-state
				global info											# GUI info bar
				global qr_time										# QR timed out?
				## Threading ##
				global thr1											# 1st thread flag
				global t1											# thread object
				
				###########################
				## START ID SCAN ROUTINE ##
				###########################
				if btn_state1 == 0:
					## Update GUI Labels ##
					bigButton["text"] = "START\nCOUNT"				# Change Button Title
					info = "[INFO] Video Scan Complete"				# 
					update_label()									# Update GUI info bar
					## Start QR Scan ##
					QR_Scan()										# Scan (2x) QR Codes
					#fake_scan()									# REMOVE - testing
					if qr_time == True:
						btn_state1 = 1								# To "START COUNTER"
				
				#########################
				## START COUNT ROUTINE ##
				#########################
				elif btn_state1 == 1:
					## Initialise thread once - can't kill ##
					if thr1 == 0:
						strtstp = 0									# Update Start time
						thr1 = 1									# Only once per Start
						## Setup Gesture Counting Thread ##
						t1 = threading.Thread(name='daemon', target=get_gesture)	# Not started yet
						#t1 = threading.Thread(name='daemon', target=fake_gesture)	# REMOVE - test function
						t1.setDaemon(True)											# Make Daemonic
						## Setup background Publisher Thread ##
						t2 = threading.Thread(name='daemon', target=handleData)		# Not started yet
						t2.setDaemon(True)											# Make Daemonic

					## Update GUI Labels ##
					bigButton["text"] = "STOP\nCOUNT"				# button label change
					info = "[INFO] Counting..."						# User info
					
					## Check fail file for previous count value	 ##
					## Create new or start count from last value ##
					fail = failCheck(Cnt)							# Returns stored value for next count
					if fail != '0':
						Cnt = int(fail)								# could do this in the function
					else:
						Cnt = 0										# zero counter

					## If thread not started (can't start twice?) ##
					if thr1 == 1:
						#print("Start COUNT Thread")				# REMOVE
						thr1 = 2									# increment flag
						GestDone = False							# start loop
						## BEWARE - THREADS ARE IMMORTAL! ##
						t1.start()									# start gesture thread
						t2.start()									# start publish thread
						## Indicate Count Busy ##
						RED.off()
						GREEN.on()
					
					update_label()									# Update GUI info
					btn_state1 = 2									# To "STOP COUNTER"
				
				######################
				## END COUNT ROUTINE #
				######################
				elif btn_state1 == 2:
					bigButton["text"] = "START\nSCAN"
					info = "[INFO] Counting Complete"
										
					## If Gesture Thread is Running ##
					if t1.isAlive():								#if thr1 == 2:
						thr1 = 0									# Clear thread flag
						#t1.join()									# FREEZE GUI
						GestDone = True								# Break out of Gesture funtion
						os.remove(failFile)							# Delete Fail File
						## Indicate Count Complete ##
						GREEN.off()
						RED.on()
					else:
						print("Due to the immortal thread,")
						print("We should never come here...")
						print("There can be only ONE ! !")
						
					## Update GUI information ##
					update_label()
					
					#print("change button")							# REMOVE
					btn_state1 = 0									# Back to "START SCAN"
			
			
			################################
			## CREATE JSON DATA STRUCTURE ##
			## PUBLISH TO GCP VIA MQTT	  ##
			################################
			def handleData():
				global qrData											# QR Data to create JSON string
				global iotJSON											# returned JSON string
				global GestDone											# loop publish with gesture sensor
				global pubNow											# Publish count flag
				global Cnt												# Current count value
				
				pubNow = False											# clear flag
				CntCpy = 0												# Keep track of publishes
				
				## Backup Count value - unexpected power-down ##
				if Cnt != 0:
					failCheck(Cnt)										# No need for stored count

				## Continuously loop publisher ##
				while GestDone == False:								# same as gesture loop ? ? ?
					## If publish triggered ##
					if pubNow == True:
						## Keep checking for count difference ##
						if CntCpy == (Cnt-1):							# if same, publish current count
							## publish the latest 'Cnt' value ##
							iotJSON = createJSON(qrData, Cnt)			# Convert Data to JSON format
							CntCpy  = Cnt 								# Copy last published count value
							pubNow = False								# count matches -> Exit publish
							
						## until caught up with current/final count value ##
						else:											# if diff, publish until same
							## publish the previous counts ##
							iotJSON = createJSON(qrData, CntCpy)		# Convert Data to JSON format
							CntCpy += 1									# increment until equal to 'Cnt'
						
						## HUNGOVER!!! ##
						if CntCpy > Cnt:
							pubNow = False								# count matches -> Exit publish

						## Publish JSON Data to IoT Core ##
						iot_publish(iotJSON, dataDict['STAGE'])
						#print("\nPublish: {}".format(iotJSON))			# REMOVE

						## Confirm Published - Once per Count ##
						GREEN.off()
						RED.on()
						time.sleep(0.2)									# blink
						RED.off()
						GREEN.on()
						print("[INFO] PUBLISHED...")					# REMOVE

				print("[INFO] Exit Publish Loop...")					# REMOVE

			
			#####################
			## JSON DATA CLASS ##
			#####################
			class OmniData:
				CLIENT 	= 'TSE'
				PROJECT = 515151515
				STAGE 	= 'NULL'
				BOARDS 	= 0
				PANELS 	= 0
				COUNT	= 0
				STAFF_ID = 000
				DATE 	= '01-01-2020'
				TIME 	= '00:00'
				START 	= '00:00'
				STOP 	= '00:00'
				REASON 	= 'NULL'
				SERIAL 	= 121212121


			##################################
			## 	   UPDATE ALL INFO DATA 	##
			## CREATE JSON STRING AND STORE	## 
			##################################
			def createJSON(qrData, Cnt):
				global firstScan									# only store certain data on first scan
				global strtstp										# project start or stop
				global staffID										# Extracted Staff ID from QR Scan2
				global dataDict
				global staffKit										# kitID[0] OR staffID[1]
												
				## Get Startup Information - Time & Date on 'SETUP' stage ##
				now = datetime.datetime.now()						# Get 'nows' date & time
				#current_date = now.strftime("%Y-%m-%d")			# Extract date
				current_time = now.strftime("%H:%M:%S")				# Extract time
				
				## Update only on 1st QR Scan ##
				if firstScan == 0:
					## Extract data with ',' delimiter - Directly into Global Disctionary ##
					dataDict = dict(i.split('=') for i in qrData.split(','))
					firstScan = 1									# RETURN TO '0' EVERY TIME SCAN IS OPENED 
					current_date = now.strftime("%Y-%m-%d")			# Extract date
					dataDict['STAFF_ID'] = staffID					# Update Staff ID		- on startup
					dataDict['DATE'] = current_date					# insert current date

				## @start click ##
				if strtstp == 0:
					strtstp = 1
					dataDict['START'] = current_time				# insert current time
					dataDict['STOP']  = current_time				# blank stop time
				## @stop click ##
				elif strtstp == 2:
					dataDict['STOP']  = current_time				# insert current time

				## Continuously Update these: ##
				dataDict['COUNT'] = Cnt								# Update board count 	- every count
				dataDict['TIME'] = current_time						# insert upload time

				## Mirror dictionary data to data class ##
				## EDIT: Use loop to import new data ##
				OmniData1 = OmniData()								# get object characteristics
				OmniData1.CLIENT 	= dataDict['CLIENT']
				OmniData1.PROJECT 	= dataDict['PROJECT']
				OmniData1.STAGE 	= dataDict['STAGE']
				OmniData1.BOARDS 	= dataDict['BOARDS']
				OmniData1.PANELS 	= dataDict['PANELS']
				OmniData1.COUNT 	= dataDict['COUNT']
				OmniData1.STAFF_ID 	= dataDict['STAFF_ID']
				OmniData1.DATE 		= dataDict['DATE']
				OmniData1.TIME 		= dataDict['TIME']
				OmniData1.START 	= dataDict['START']
				OmniData1.STOP 		= dataDict['STOP']
				OmniData1.REASON 	= dataDict['REASON']
				OmniData1.SERIAL 	= dataDict['SERIAL']

				## Convert Data Class to JSON string ##
				## NOTE: Data fields are not created in the same order ##
				jsonStr = json.dumps(OmniData1.__dict__)

				## Pass JSON string back ##
				return jsonStr
			
			
			##############################
			## CREATE THE JWT TOKEN KEY ##
			##############################
			def create_jwt(project_id, private_key_file, algorithm):
				token = {
					## The time that the token was issued at ##
					'iat': datetime.datetime.utcnow(),
					## The time the token expires ##
					'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
					## The audience field should always be set to the GCP project id ##
					'aud': project_id
				}
				
				## Read the private key file ##
				with open(private_key_file, 'r') as f:
					private_key = f.read()
				
				#print('Creating JWT using {} from private key file {}'.format(algorithm, private_key_file))
				return jwt.encode(token, private_key, algorithm=ssl_algorithm)
			
			
			##################################
			## CONNECT VIA MQTT AND PUBLISH ##
			##################################
			def iot_publish(message_json, stage):
				global info 									# Update label

				try:
					JWT_token = create_jwt(project_id, ssl_private_key, ssl_algorithm)
					token = JWT_token.decode('utf8')
									
					## Python3 ##
					#base64_message = base64.urlsafe_b64encode(bytes(message_string,'utf8'))
					## Python2 ##
					base64_message = base64.urlsafe_b64encode(bytes(message_json).encode('utf8'))
					
					message = {"binary_data": base64_message.decode('utf8')}
					
					payload = json.dumps(message)
					
					if stage == 'SETUP':
						url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-1:publishEvent'
					elif stage == 'THRU':
						url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-2:publishEvent'
					elif stage == 'SMT':
						url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-3:publishEvent'
					elif stage == 'INSP':
						url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-4:publishEvent'
					
					headers = {
					'Authorization': 'Bearer {}'.format(token),
					'Content-Type': 'application/json'
					}
					
					response = requests.request("POST", url, headers=headers, data = payload)
					response.raise_for_status()
				
				except requests.exceptions.HTTPError as errh:
					print ("NETWORK ERROR: 1")					#print ("Http Error:",errh)
					info = "[INFO] NETWORK ERROR: 1"			# message info
					update_label()								# Update GUI info bar

				except requests.exceptions.ConnectionError as errc:
					print ("NETWORK ERROR: 2")					#print ("Error Connecting:",errc)
					info = "[INFO] NETWORK ERROR: 2"			# message info
					update_label()								# Update GUI info bar
					
				except requests.exceptions.Timeout as errt:
					print ("NETWORK ERROR: 3")					#print ("Timeout Error:",errt)
					info = "[INFO] NETWORK ERROR: 3"			# message info
					update_label()								# Update GUI info bar
					
				except requests.exceptions.RequestException as err:
					print ("NETWORK ERROR: 4")					#print ("Oops: Something Else",err)
					info = "[INFO] NETWORK ERROR: 4"			# message info
					update_label()								# Update GUI info bar
					

			############################
			# DROP DOWN MENU CALLBACK ##
			############################
			def callback(*args):
				global info 
		
				# Update info bar in 'main.py'
				info = "[INFO] stage - {}".format(dropD.get())	# New 'info' message
				update_label()									# Update GUI Info label
				
				## Begin Exit Routine ##
				if dropD.get() == "EXIT":
					exitProgram()
				## Update Stage to Dictionary ##
				else:
					## NO CODE REQUIRED FOR STAGE CHANGE (main2.py) ##
					dataDict['STAGE'] = dropD.get()
			
			
			###########################
			## REALTIME LABEL UPDATE ##
			###########################
			def update_label():
				global Cnt
				global info
				
				## Update Count Label ##
				label_4.config(text="- {} -".format(Cnt), font = myFont1)
				## Update Info Label ##
				label_6.config(text="{}".format(info), font = "Helvetica 10")
			
			
			###############################
			## NUMERICAL EXIT CODE ENTRY ##
			###############################
			def code(value):
				global pin									# 
				global ExCode								# 

				## '*' Key presses ##
				if value == '*':
					## remove last digit from `pin` ##
					pin = pin[:-1]
				
				## '#' Key presses ##
				elif value == '#':
					## check pin ##
					if pin == "3529":						# Set pin number here!
						print("PIN OK")						# console - REMOVE
						pin = ''							# clear `pin`
						#ExCode = True 						# Set ExCode
						KeyPadExit(True)					# Close keypad window
					else:
						print("INCORRECT PIN!")				# console - REMOVE
						pin = ''							# clear `pin`
						
						# After 3 attempts - Close keypad window
						KeyPadExit(False)					# must be repeatable

				## Any digit keys pressed ##
				else:
					pin += value							# Add digit to pin
				
				print("Current: " + pin)					# show input code
			
			
			##########################
			## CREATE KEYPAD WINDOW ##
			##########################
			def KeyPadWin():
				## Define keypad keys ##
				keys = [
					['1', '2', '3'],    
					['4', '5', '6'],    
					['7', '8', '9'],    
					['*', '9', '#'],    
				]
				## Create new Window ##
				keyPadWin = Toplevel(win)
				lay.append(keyPadWin)
				keyPadWin.title("EXIT CODE")
				
				## Create buttons using `keys`
				for y, row in enumerate(keys, 1):
					for x, key in enumerate(row):
						# `lambda` inside `for` has to use `val=key:code(val)` 
						# instead of direct `code(key)`
						b = Button(keyPadWin, text=key, command=lambda val=key:code(val))
						b.grid(row=y, column=x, ipadx=10, ipady=10)
			
			
			########################
			## EXIT KEYPAD WINDOW ##
			########################
			def KeyPadExit(CodeDone):
				global info										# App information
				
				print("[INFO] Destroy Window...")				# REMOVE
				keyPadWin = lay[0]								# DON'T THINK THIS WORKING??
				
				if CodeDone == True:
					print("[INFO] Quit Main Program!!")			# REMOVE
					## Destroy All Windows ##
					## NOT DESTROYING CV2 WINDOW ? ? ##
					win.quit()
					win.destroy()
					sys.exit(0)
				else:
					## Info: Exit Failed ##
					info = "[INFO] Exit Code Incorrect"			# New 'info' message
					update_label()								# Update GUI Info label 
					print("[INFO] Exit Code Incorrect")			# REMOVE
						
					## Destroy Keypad Window ##
					keyPadWin.destroy()							
					keyPadWin.update()							# --- Only works once? ? ?
			
			
			##########################
			## EXIT AND DESTROY GUI ##
			##########################
			def exitProgram():
				global thr1										# Thread exitted correctly
				global info										# App information
				global ExCode									# code correct/incorrect - flag
				
				ExCode = False									# Normally Blocked
				
				## Check thread ended properly ##
				if thr1 == 0:
					## Enter Exit Code ##
					KeyPadWin()									# keypad input
				else:
					print("Still busy...")						# REMOVE
					info = "[INFO] Stop Count to Exit"					# message info
					update_label()								# Update GUI info bar



			## INITIALISE NEW WINDOW ##
			win = Tk()
			## Define the Fonts:
			myFont1 = tkFont.Font(family = 'Helvetica', size = 30, weight = 'bold')
			myFont2 = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

			# SETUP WINDOW PARAMTERS ##
			win.title("OMNIGO")									# define window title
			#win.geometry('480x320+0+0')						# define screen size	- swap
			win.attributes("-fullscreen", True)					# full screen GUI		- swap
			win.configure(background = "gray15")				# set colour
			
			# DROP-DOWN MENU ##
			dropD = StringVar(win)
			dropD.set("Stage")

			opt = OptionMenu(win, dropD, *OptionList)
			opt.config( width=5, 
						font=('Helvetica', 10), 
						bg		= "gray15",
						fg 		= "gray64",)
			opt.pack(side="top", anchor="nw")
			
			# EXIT BUTTON - REMOVED ##
			
			# OMNIGO TITLE ##
			label_2 = Label(win, 
							text 	= "- OMNIGO -", 
							bg 		= "gray15",
							fg 		= "OrangeRed2",
							relief 	= "solid",
							font 	= "Helvetica 36",
							width 	= 11,
							height	= 1)
			# SPACER ##
			label_3 = Label(win, 
							text	= " ", 
							bg 		= "gray15",
							font 	= "Helvetica 18")
			
			# Place objects ##
			label_2.pack(padx=10)
			label_3.pack(padx=10)
			
			# STOP/START BUTTON ##
			bigButton = Button(win, 
								text 	= "SCAN\n- ID -", 
								font 	= myFont1, 
								command = btn_start,	# btn_cnt,
								fg 		= "Red4",
								bg 		= "gray45",
								height 	= 2, 
								width 	= 12)
			bigButton.pack(anchor=CENTER)				# place the object
				
			# SPACER ##
			label_5 = Label(win, 
							text	= " ", 
							bg 		= "gray15",
							font 	= "Helvetica 14")
			# COUNTER ##
			label_4 = Label(win, 
							text	= "- {} -".format(Cnt), 
							fg 		= "OrangeRed2",
							bg 		= "gray15",
							font 	= "Helvetica 30")
			# INFORMATION ##
			label_6 = Label(win, 
							text	= "[INFO] {}".format(info), 
							fg 		= "OrangeRed2",
							bg 		= "gray15",
							font 	= "Helvetica 10")
							
			# Place more objects ##
			label_5.pack(padx=10)						# spcer from button
			label_4.pack(padx=10)						# PCB counter
			label_6.pack(anchor=SW)						# PCB counter
			
			# DROP-DOWN Function Call ##
			dropD.trace("w", callback)
			
			# GUI main loop ##
			mainloop()
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("main.py - keyboard interupt")
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("main.py - Exception reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
