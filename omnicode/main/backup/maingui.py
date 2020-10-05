#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Description:
Main control class for omnigo IoT project
Includes:
	apds9960 gesture sensor counting method
	PiCamera QR Code reading and storage method

USAGE:
python main.py
"""
###################
# import packages #
###################
from Tkinter import *
import tkFont
import sys
from time import sleep
import traceback
import RPi.GPIO as GPIO
from picamera import PiCamera
import qrClass as qrRead
#import gestClass as gestRead

#####################
##   GLOBAL DEFS   ##
#####################
btn_state1 = True
btn_state2 = True

###################
## MAIN FUNCTION ##
###################
def main():
	ID_match = 0							# initial staff ID status
	try:
		try:
			QR = qrRead.qrClass()			# QR Reader Class instantuate
			#gest = gestRead.gestClass()		# Gesture Sensor Class instantuate
			camera = PiCamera()				# Initialise the camerac
			
			def btn_scan():
				print("BUTTON 1 PRESSED")
				global btn_state1
				
				if btn_state1 == False:
					print("READING QR CODE...")
					# start reading QR Code
					ID_match = QR.qr_read()
					
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
			
			def btn_cnt():
				print("BUTTON 2 PRESSED")
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
