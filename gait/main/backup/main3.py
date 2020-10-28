"""
Date: prior 16-10-2020

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
import sensClass1 as sens						# Tutorial Version
#import sensClass2 as sens						# Aubry version
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
	log1 	= 0									# get log value
	log2 	= 0									# comparitive value
	conPass = False								# connected successfully?
	reCon 	= False								# reconnection flag
	
	faulthandler.enable()						# enable fault handler
	sensor1 = sens.sens1()						# instantuate device class
		
	## Initialise the Device ##
	conPass = sensor1.DevConnect(ID)
	sensor1.startup()

	try:
		## CONNECTION PASS ##
		while conPass == True:
			
			## ----RUN---- ##
			sensor1.DevRun()					# Execute once per connection
						
			## Stay Here While Running ##
			while stopCnt == True:
				time.sleep(3)					# check every 3 sec
				log1 = sensor1.logVal()			# get log count value
				print("Log: {}".format(log1))	# REMOVE
				
				## CHECK RUNNING ##
				if log1 > log2:	log2 = log1		# get new comp value
				## GOT STUCK ##
				else: stopCnt = False 			# break loop
			
			## CLOSE DEVICE ##
			print("1. CLOSE DEVICE")			# REMOVE
			time.sleep(1.5)						# REMOVE
			sensor1.DevClose()					# 
			
			## Didn't Help with SegFault ##
			#print("2. CLOSE DEVICE AGAIN?")	# REMOVE
			#time.sleep(3.5)					# REMOVE
			#sensor1.DevClose()					# 
			
			## Attempt ReConnection ##
			print("2. ATTEMPT RECONNECT")		# REMOVE
			time.sleep(1.5)						# REMOVE
			conPass = sensor1.DevReConnect(ID)	# IF FAILS BREAKS MAIN LOOP
			## ReConnect Successful ##
			if conPass == True: 
				## Reset Values ##
				stopCnt = True
				log2 	= 0
		
		## END OF RUN ##
		print("RE-CONNECTION FAILED")			# REMOVE
		
	## System Error: ##
	except OSError as err:
		sensor1.DevClose()
		print ("\r\nOS ERROR {}".format(err))
		sys.exit()
	## Value Error ##
	except ValueError:
		sensor1.DevClose()
		print("\r\nError with variable...")
		sys.exit()
	## Keyboard Exit ##
	except KeyboardInterrupt:
		sensor1.DevClose()
		print("\r\nEscape (MAIN) - Device Closed...")
		sys.exit(0)	
	## NameError - Suggested ##
	except NameError:
		sensor1.DevClose()
		print("\r\nNameError:")
		sys.exit(0)	
	## Unknown Error ##
	except:
		sensor1.DevClose()
		print("\r\nUnexpected Error:", sys.exc_info()[0])
		sys.exit() 
	
	finally:
		## CLOSE DEVICE ##
		sensor1.DevClose()						# Check already closed??
		print("Closed Device - Final!!")
		sys.exit(0)	

if __name__ == "__main__":	main()
