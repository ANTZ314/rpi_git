# -*- coding: utf-8 -*-
"""
Description: 
Test blink LED
"""

from gpiozero import LED 				# Import GPIO library
import time 					## Import 'time' library. Allows us to use 'sleep'
import sys

RED = LED(5)
GREEN = LED(6)


def main():
	
	try:
		while True:
			print("RED")
			RED.on()
			time.sleep(1)
			RED.off()
			time.sleep(1)
			print("GREEN")
			GREEN.on()
			time.sleep(1)
			GREEN.off()
			time.sleep(1)
			

	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# 
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
