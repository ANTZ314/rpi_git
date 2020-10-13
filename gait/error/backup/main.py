"""
Date: 02-10-2020

Description:
	main function handling system errors and calling
	bluetooth connectivity and run function in class
	
Segmentation Fault Note:
	View current Stack Size 	-> ulimit -a
	Increase Stack Size (1mb) 	-> ulimit -s 1024
	untested maximum (16mb) ? ?	-> 16384 = 8192 (x2)
	Added Connection Fail Skip

Usage:
python3 main.py
-OR-
python3 /home/pi/Documents/rpi_git/aubry/main/main.py
"""
#import sensClass1 as sens						# Tutorial Version
import sensClass2 as sens						# Aubry version
import sys, time								# system things
import faulthandler

## Sensor ID ##
#ID = MetaWear("FB:E2:B9:C5:60:AA")
ID = "FB:E2:B9:C5:60:AA"
crash = "crash.log"

## MAIN FUNCTION ##
def main():
	stopCnt = 0
	conPass = False
	
	## Handle - segmentation fault ##
	faulthandler.enable()						# enable handler
	
	sensor1 = sens.sens1()						# instantuate device class
		
	## Initialise the Device ##
	conPass = sensor1.DevConnect(ID)
	sensor1.startup()

	#while True:
	try:
		if(conPass == True):
			# REMOVE
			print("Start 1st RUN")			# REMOVE
			time.sleep(2.5)
			
			#################
			## ----RUN---- ##
			#################
			sensor1.DevRun()
					
			## RUN for 'x' Seconds ##
			while stopCnt < 15:
				stopCnt += 1
				time.sleep(1)
						
			## Close Device ##
			sensor1.DevClose()
			print("Closed Device")			# REMOVE
			stopCnt = 0						# Clear
			time.sleep(1.5)
			
			## Attempt ReConnection ##
			sensor1.DevReConnect(ID)
			print("Started 2nd RUN")		# REMOVE
			time.sleep(1)
			
			#################
			## ----RUN---- ##
			#################
			sensor1.DevRun()
			
			## RUN for 'x' Seconds ##
			while stopCnt < 10:
				stopCnt += 1
				time.sleep(1)
		## Connection Failed ##
		else:
			## Reset Everything ##
			print("RESET BLE and SENSOR??")
			time.sleep(1)
			
		print("COMPLETE")				# REMOVE
		
	## System Error: ##
	except OSError as err:
		print ("\r\nOS ERROR {}".format(err))
		sensor1.DevClose()
		print("Device closed properly...")
		sys.exit()
	## Value Error ##
	except ValueError:
		print("\r\nError with variable...")
		sensor1.DevClose()
		print("Device closed properly...")
		sys.exit()
	## Keyboard Exit ##
	except KeyboardInterrupt:
		sensor1.DevClose()
		print("\r\nEscape (MAIN) - Device Closed...")
		sys.exit(0)	
	## NameError - Suggested ##
	except NameError:
		print("\r\nNameError:")
	## Unknown Error ##
	except:
		print("\r\nUnexpected Error:", sys.exc_info()[0])
		sensor1.DevClose()
		print("Device Closed Properly...")
		sys.exit() 
	
	finally:
		sensor1.DevClose()
		print("Closed Device - Final!!")

if __name__ == "__main__":	main()
