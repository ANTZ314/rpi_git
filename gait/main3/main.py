"""
Date: 		01-03-2021
Editted:	A.Smith

Description:
	-> Main function handling system errors and calling
		bluetooth connectivity and run function in class.
	-> Run function is parallel to main code, so loops in 
		line 53 unless connection is lost.

IDs Found:
[0] - "FB:E2:B9:C5:60:AA"
[1] - "F9:DC:59:47:98:6A"
[2] - "C6:22:44:10:EE:D9"

Usage:
python3 main.py
"""
import sensClass1 as sens1						# Latest Version
import sensClass2 as sens2						# Latest Version
import sys, time								# system things
import faulthandler								# guess what this handles

## Sensor ID ##
ID1 = "F9:DC:59:47:98:6A"
ID2 = "C6:22:44:10:EE:D9"
crash = "crash.log"


###################
## MAIN FUNCTION ##
###################
def main():
	stopCnt  = True								# initially stay in check loop
	log1 	 = 0								# get log value
	log2 	 = 0								# comparitive value
	conPass1 = False							# SENSOR1 connected successfully?
	#conPass2 = False							# SENSOR2 connected successfully?
	reCon 	 = False							# reconnection flag
	
	faulthandler.enable()						# enable fault handler
	sensor1 = sens1.sens1()						# instantuate device class 1
	sensor2 = sens2.sens2()						# instantuate device class 2
	
	## Initialise the 1st Device ##
	conPass1 = sensor1.DevConnect(ID1)
	sensor1.startup()

	####

	## Initialise the 2nd Device ##
	conPass2 = sensor2.DevConnect(ID2)
	sensor2.startup()

	try:
		## CHECK CONNECTION PASS ##
		while conPass1 == True and conPass2 == True:
			
			## ----RUN---- ##
			sensor1.DevRun()					# Execute once per connection
			sensor2.DevRun()					# Execute once per connection
						
			## Stay Here While Running ##
			while stopCnt == True:
				time.sleep(3)					# check every 3 sec
				log1 = sensor1.logVal()			# get log count value
				print("Log: {}".format(log1))	# REMOVE
				## CHECK SENSOR1 RUNNING ##
				if log1 > log2:	log2 = log1		# get new comp value
				## GOT STUCK ##
				else: stopCnt = False 			# break loop
			
			## CLOSE DEVICE ##
			print("1. CLOSE DEVICE")			# REMOVE
			time.sleep(1.5)						# Can this be shorter??
			sensor1.DevClose()					# 
			time.sleep(1.5)						# Can this be shorter??
			sensor2.DevClose()					# 
			
			##--------- Attempt ReConnection ---------##
			"""
			#** Temporarily removed 'reconnect' **#
			print("2. ATTEMPT RECONNECT")		# REMOVE
			time.sleep(1.5)					# Can this be shorter??
			
			## IF FAILS BREAKS MAIN LOOP ##
			conPass1 = sensor1.DevReConnect(ID1)
			
			# IS DELAY BEFORE 2ND RECONNECT REQUIRED???
			time.sleep(1.5)					# Can this be shorter??
			conPass2 = sensor1.DevReConnect(ID2)
			
			## ReConnect Successful ##
			if conPass1 == True:
				## Reset Values ##
				stopCnt = True
				log2 	= 0
			else:
				print("RE-CONNECTION FAILED")	# REMOVE
			"""
			##--------- Attempt ReConnection ---------##
			
			
			##--------- END LOOP AT log=9999 ---------##
			print("STOP LOGGING HERE...")		# REMOVE
			time.sleep(1.5)						# REMOVE
			conPass1 = False					# REMOVE
			# Unnecessary to do both #
			#conPass2 = False					# REMOVE
			##--------- END LOOP AT log=9999 ---------##
		
		## END OF RUN ##
	
	#########################################
	## CATCH ANY EXCEPTIONS THAT MAY OCCUR ##
	#########################################
	## System Error: ##
	except OSError as err:
		sensor1.DevClose()
		sensor2.DevClose()						# 
		print ("\r\nOS ERROR {}".format(err))
		sys.exit()
	## Value Error ##
	except ValueError:
		sensor1.DevClose()
		sensor2.DevClose()						# 
		print("\r\nError with variable...")
		sys.exit()
	## Keyboard Exit ##
	except KeyboardInterrupt:
		sensor1.DevClose()
		sensor2.DevClose()						# 
		print("\r\nEscape (MAIN) - Device Closed...")
		sys.exit(0)	
	## NameError - Suggested ##
	except NameError:
		sensor1.DevClose()
		sensor2.DevClose()						# 
		print("\r\nNameError:")
		sys.exit(0)	
	## Unknown Error ##
	except:
		sensor1.DevClose()
		sensor2.DevClose()						# 
		print("\r\nUnexpected Error:", sys.exc_info()[0])
		sys.exit() 
	## Do after none/any Error? ##
	finally:
		## CLOSE DEVICE ##
		sensor1.DevClose()						# Check already closed??
		sensor2.DevClose()						# 
		print("Closed Device - Final!!")
		sys.exit(0)	

if __name__ == "__main__":	main()
