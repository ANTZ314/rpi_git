#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
Main control class for omnigo IoT project
Includes:
	apds9960 gesture sensor counting method
	PiCamera QR Code reading and storage method
	
Notes:
	Gesture throws Error is sensor is not plugged in.
	Removed the QR Class due to VVideoStream instantiation issues
	Moved to function in "maingui.py".

USAGE:
python main.py
"""
###################
# import packages #
###################
from Tkinter import *					# GUI package
import tkFont							# GUI package
import sys, time						# Possibly remove ? ?
import RPi.GPIO as GPIO					# Possibly remove ? ?
from time import sleep					# Delays
import traceback						# Error logging
#import gestClass as gestRead			# Gesture sensor must be connected

## 	QR CODE IMPORTS ##
from picamera import PiCamera			# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar				# Decoding the QR Code
import datetime							# piece of shit
import imutils 							# Magic
import cv2

###################
##  GLOBAL DEFS  ##
###################
btn_state1 = True
btn_state2 = True
csv_file = "barcodes.csv"

###################
##   FUNCTIONS   ##
###################
def QR_Scan():
	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(usePiCamera=True).start()
	sleep(2.0)
	
	# open the output CSV file for writing
	csv = open(csv_file, "w")
	found = set()
	sleep(3.0)		# test
	
	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
	 
		# find the barcodes in the frame and decode each of the barcodes
		barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	 
			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
	 
			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	 
			# if the barcode text is currently not in our CSV file, write
			# the timestamp + barcode to disk and update the set
			if barcodeData not in found:
				csv.write("{},{}\n".format(datetime.datetime.now(),
					barcodeData))
				csv.flush()
				found.add(barcodeData)

		# show the output frame
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	
	# close the output CSV file do a bit of cleanup
	print("[INFO] cleaning up...")
	csv.close()
	cv2.destroyAllWindows()
	vs.stop()

###################
## MAIN FUNCTION ##
###################
def main():
	ID_match = 0								# initial staff ID status
	try:
		try:
			#gest = gestRead.gestClass()		# Gesture Sensor Class instantuate
			#camera = PiCamera()				# Initialise the camerac
			
			## BUTTON: EMPLOYEE ID SCAN ##
			def btn_scan():
				print("READ EMPLOYEE ID")
				global btn_state1
				
				if btn_state1 == False:
					print("READING QR CODE...")
					# start reading QR Code
					#ID_match = QR.qr_read()
					QR_Scan()
					
					## Camera Test ##
					#camera.start_preview()
					#sleep(5)
					#camera.stop_preview()
					print("QR Scan Complete!!")
					
					scanButton["text"] = "SCAN ON"
					btn_state1 = not btn_state1
					
				else:
					scanButton["text"] = "SCAN OFF"
					btn_state1 = not btn_state1
			
			## BUTTON: GESTURE COUNING ##
			def btn_cnt():
				print("START COUNTING PCBs")
				global btn_state2
				
				if btn_state2 == False:
					print("COUNTING!!")					
					# start counting PCB's
					#gest.get_gesture()
					## return gesture captured?
					sleep(5)
					print("Counting Complete!!")
					
					cntButton["text"] = "COUNT ON"
					btn_state2 = not btn_state2
					
				else:
					cntButton["text"] = "COUNT OFF"
					btn_state2 = not btn_state2
			
			def exitProgram():
				print("Exit Button pressed")
				win.quit()
			
			win = Tk()

			myFont = tkFont.Font(family = 'Helvetica', size = 24, weight = 'bold')

			win.title("OMNIGO")
			win.geometry('480x320')

			exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =1 , width = 5) 
			exitButton.pack(side = BOTTOM)

			scanButton = Button(win, text = "SCAN", font = myFont, command = btn_scan, height = 3, width = 10)
			scanButton.pack(side = LEFT)
			
			cntButton = Button(win, text = "COUNT", font = myFont, command = btn_cnt, height = 3, width = 10)
			cntButton.pack(side = RIGHT)

			mainloop()
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("main.py - keyboard interupt")
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("master.py - Exception reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)


if __name__ == "__main__":	main()
