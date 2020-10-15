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
import faulthandler								# guess what this handles

## Sensor ID ##
ID = "FB:E2:B9:C5:60:AA"
crash = "crash.log"


###################
## MAIN FUNCTION ##
###################
def main():
	stopCnt = True								# initially stay in check loop
	log1 = 0									# get log value
	log2 = 0									# comparitive value
	conPass = False								# connected successfully?
	
	## Handle - segmentation fault ##
	faulthandler.enable()						# enable handler
	
	sensor1 = sens.sens1()						# instantuate device class
		
	## Initialise the Device ##
	conPass = sensor1.DevConnect(ID)
	sensor1.startup()

	#while True:
	try:
		## CONNECTION PASS ##
		if(conPass == True):			
			#################
			## ----RUN---- ##
			#################
			sensor1.DevRun()					# Execute once per connection
			
			#--------------------------------------------#
			
			## RUN for 'x' Seconds ##
			while stopCnt == True:
				#stopCnt += 1
				time.sleep(3)					# check every 3 sec
				log1 = sensor1.logVal()			# get log count value
				print("Log: {}".format(log1))	# REMOVE
				
				## log1 higher: 		 ##
				## - until log is zeroed ##
				## - or RUN loop stops   ##
				if log1 > log2:					# comparison
					log2 = log1					# get new comp value
				else:
					stopCnt = False 			# break loop
				
			
			print("GOT STUCK - RESTART")		# REMOVE
			time.sleep(3.5)						# REMOVE
			
			## CLOSE DEVICE ##
			sensor1.DevClose()
			print("Closed Device - FIRST")		# REMOVE
			stopCnt = 0							# Clear
			time.sleep(1.5)						# REMOVE
			
					
		
		## END OF RUN ##
		print("COMPLETE")						# REMOVE
		
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
		## CLOSE DEVICE ##
		sensor1.DevClose()						# Check already closed??
		print("Closed Device - Final!!")

if __name__ == "__main__":	main()
