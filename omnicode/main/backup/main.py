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
# import the necessary packages
import sys, time
import traceback
import RPi.GPIO as GPIO
import qrClass as qrRead
import gestClass as gestRead


###################
## MAIN FUNCTION ##
###################
def main():
	ID_match = 0							# initial staff ID status
	try:
		try:
			QR = qrRead.qrClass()			# QR Reader Class instantuate
			gest = gestRead.gestClass()		# Gesture Sensor Class instantuate
			
			while True:
				print("'gest' - Gesture")
				print("'qr' - QR Scan")
				print("'q' - Quit")
				## Select gesture/QR mode:
				#key = input("q - QR Code or g - Gesture:")		# linux input method
				key = raw_input()
				
				if key == 'qr':
					print("READING QR CODE...")
					# start reading QR Code
					ID_match = QR.qr_read()
					print("QR Scan Complete!!")
					# If ID matches stored ID
					if ID_match == 1:
						print("staff member recognised")
					else:
						print("Not a staff member?")
				
				## or read qr data after captured
				
				elif key == 'gest':
					# start reading gestures
					gest.get_gesture()
					## return gesture captured?
					print("Counting Complete!!")
				
				elif key == 'q':
					break
				
				else:
					print("Incorrect option selected :(")
			
			print("DONE!!")					# Guess what this does??
			sys.exit(0)						# exit properly
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("main.py - keyboard interupt")
			#GPIO.cleanup()
			sys.exit(0)
		
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("master.py - Exception reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		#GPIO.cleanup()
		sys.exit(0)


if __name__ == "__main__":	main()
