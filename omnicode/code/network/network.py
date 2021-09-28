# -*- coding: utf-8 -*-
"""
Description:
	Catch network connection errors and restart from check point

Functionality:
	
"""

import sys, time, os
import requests

failFile = 'fail.txt'
JSONString1 = '{"COUNT": 3, "STAFF_ID": "258", "BOARDS": "55", "STOP": "00:00", "PROJECT": "369", "START": "15:25:22", "REASON": "none", "CLIENT": "DailyPlanet", "TIME": "15:25:45", "DATE": "2020-08-24", "SERIAL": "456123", "PANELS": "0", "STAGE": "INSP"}'
JSONString2 = '{"COUNT": 11, "STAFF_ID": "159", "BOARDS": "111", "STOP": "00:00", "PROJECT": "852", "START": "15:25:22", "REASON": "none", "CLIENT": "DailyPlanet", "TIME": "15:25:45", "DATE": "2020-08-24", "SERIAL": "789132", "PANELS": "0", "STAGE": "SMT"}'
global Cnt
global fail

def failCheck(Cnt):
	exists = False										# file exists or not?
	fail = 'check'										# stored json string
	## Try to read file ##
	try:												# Skip if file doesn't exist
		file = open(failFile, 'r') 						# Open to read file
		fail = file.read()								# read file contents
		#print("STORED: {}".format(fail))				# REMOVE
		file.close()									# Close the file
	## Create - No File to Read ##
	except:
		exists = True									# Avoid writing twice if file exists
		fail = '0'										# 
		#print("STORE 0")								# REMOVE
		file = open(failFile,"w")						# Create/Open file then write data 
		file.write("0") 								# write first zero
		file.close()									# Exit the opened file
	## Seen File - Now overwrite ##
	if exists == False:									# overwrite data after printing contents
		if  Cnt != 0:									# Only if count is already going
			#print("STORE {}".format(str(Cnt)))			# REMOVE
			file = open(failFile,"w")					# Open file then Overwrite data 
			file.write(str(Cnt))						# Write new string
			file.close()								# Exit the opened file
	## Notify File Created ##
	else:												# 
		print ("On Startup - Create New Fail File!")		# REMOVE
	return fail


def main():
	print("Start")
	
	## Continuously Publish Data ##
	try:
	    r = requests.get('http://www.google.com/nothere')
	    r.raise_for_status()
	except requests.exceptions.HTTPError as errh:
	    print ("Http Error:",errh)
	except requests.exceptions.ConnectionError as errc:
	    print ("Error Connecting:",errc)
	except requests.exceptions.Timeout as errt:
	    print ("Timeout Error:",errt)
	except requests.exceptions.RequestException as err:
	    print ("OOps: Something Else",err)

	print("EXIT")
	
if __name__ == "__main__": main()