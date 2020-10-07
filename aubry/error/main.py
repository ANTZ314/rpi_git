"""
Date: 02-10-2020

Description:
	main function handling system errors and calling
	bluetooth connectivity and run function in class
	
Segmentation Fault Note:
	View current Stack Size 	-> ulimit -a
	Increase Stack Size (1mb) 	-> ulimit -s 1024
	untested maximum (16mb) ? ?	-> 16384 = 8192 (x2)

Usage:
python3 /home/pi/Documents/rpi_git/aubry/main/main.py
"""
#import sensClass1 as sens						# Tutorial Version
import sensClass3 as sens						# Aubry version
import sys, time								# system things
import faulthandler

## Sensor ID ##
#ID = MetaWear("FB:E2:B9:C5:60:AA")
ID = "FB:E2:B9:C5:60:AA"
crash = "crash.log"

## MAIN FUNCTION ##
def main():
	## Handle - segmentation fault ##
	#faulthandler.enable(file=open(crash, "w"))	# supposed to write to file?
	faulthandler.enable()						# enable handler
	
	sensor1 = sens.sens1()						# instantuate device class
		
	## Initialise the Device ##
	sensor1.DevConnect(ID)
	sensor1.startup()

	while True:
		try:
			sensor1.DevRun() 					# run?
			
			print("<------------------->")		# comes here how often??
			print("SHOW WHERE RUN BREAKS")		# Every 'x' prints??
			print("<------------------->")		#
			time.sleep(2)						# SKIPS THE BREAK?
			
			
		## System Error: ##
		except OSError as err:
			print ("\r\nOS ERROR {}".format(err))
			self.DevClose()
			print("Device closed properly...")
			sys.exit()
		## Value Error ##
		except ValueError:
			print("\r\nError with variable...")
			self.DevClose()
			print("Device closed properly...")
			sys.exit()
		## Keyboard Exit ##
		except KeyboardInterrupt:
			sensor1.DevClose()
			print("\r\nKey Exit - Device Closed")
			sys.exit(0)	
		## Unknown Error ##
		except:
			print("\r\nUnexpected Error:", sys.exc_info()[0])
			self.DevClose()
			print("Device Closed Properly...")
			sys.exit() 

if __name__ == "__main__":	main()
