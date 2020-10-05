"""
Date: 02-10-2020

Description:
main function handling system errors and calling
bluetooth connectivity and run function in class

Usage:
python3 main.py
"""
#import sensClass1 as sens						# Tutorial Version
import sensClass3 as sens						# Aubry version
import sys, time								# system things


## Sensor ID ##
#ID = MetaWear("FB:E2:B9:C5:60:AA")
ID = "FB:E2:B9:C5:60:AA"

## MAIN FUNCTION ##
def main():
	sensor1 = sens.sens1()						# instantuate class
		
	## Initialise the Device ##
	sensor1.DevConnect(ID)
	#sensor1.startup()

	while True:
		try:
			sensor1.DevRun() 						# run?
			
			print("<-------------->")
			print(" WE DO COME HER ")
			print("<-------------->")
			time.sleep(2)						# SKIPS THE BREAK?
			
			
		## Ran into Error: ##
		except Exception as e:
			print ("MAIN ERROR - {}".format(e))
			sensor1.DevClose()
			print("\r\nEXIT1 PROGRAM!!")		# 
			sys.exit(0)							# 
			
		## Keyboard Exit ##
		except KeyboardInterrupt:
			sensor1.DevClose()
			print("\r\nEXIT2 PROGRAM!!")		# 
			sys.exit(0)							# 

if __name__ == "__main__":	main()
