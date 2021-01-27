# -*- coding: utf-8 -*-
"""
Description:
Blink single LED on pin 8 multiple times
"""
#import RPi.GPIO as GPIO
from gpiozero import LED
import sys, time


class LEDClass:
	# Define Pins (Using GPIO not header numbers)
	RED = LED(5)
	GREEN = LED(6)
	
	def __init__(self, **kwargs):
		print("LED Class Init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def All_Off1(self):		
		RED.off()			# Green OFF
		RED.off()			# Green OFF
		
		
	def Blink_1(self):
		RED.on()			# Green ON
		time.sleep(0.2)
		RED.off()			# Green OFF
		time.sleep(0.2)
		RED.on()			# Green ON
		time.sleep(0.2)
		RED.off()			# Green OFF
		time.sleep(0.2)
		print("Blink 1")
		
	def Blink_2(self):
		try:
			GREEN.on()			# Green ON
			time.sleep(0.2)
			GREEN.off()			# Green OFF
			time.sleep(0.2)
			GREEN.on()			# Green ON
			time.sleep(0.2)
			GREEN.off()			# Green OFF
			time.sleep(0.2)
		
		print("Blink 2")

	def Blink_3(self):
		RED.on()			# Green ON
		time.sleep(0.2)
		RED.off()			# Green OFF
		time.sleep(0.2)
		GREEN.on()			# Green ON
		time.sleep(0.2)
		GREEN.off()			# Green OFF
		time.sleep(0.2)

	def Blink_4(self):
		GREEN.on()			# Green ON
		time.sleep(0.2)
		GREEN.off()			# Green OFF
		time.sleep(0.2)
		RED.on()			# Green ON
		time.sleep(0.2)
		RED.off()			# Green OFF
		time.sleep(0.2)
