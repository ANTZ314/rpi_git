# -*- coding: utf-8 -*-
"""
Description:
	Read text string & convert to JSON string
	PROBLEM: creates JSON in wrong object order
	NOTE: must run in python 2.7 for RPi results

INPUT:
CLIENT=Omnigo,PROJECT=123456789,STAGE=SETUP,BOARDS=1000,PANELS=50,STAFF_ID=357,TIME=08:35,DATE=11-06-2020,START=00:00,STOP=00:00,FAULT=NULL,SERIAL=987654321

OUTPUT:
{"STAFF_ID": "6", "BOARDS": "4", "FAULT": "11", "STOP": "10", "PROJECT": "2", "START": "9", "CLIENT": "1", "TIME": "7", "DATE": "8", "SERIAL": "12", "PANELS": "5", "STAGE": "3"}
"""
import json
from datetime import datetime
from collections import OrderedDict 

## General Information dictionary ##
dataDict = OrderedDict()
dataDict = {'CLIENT'	: 'xxx',				# Client Name
			'PROJECT'	: '0',				# Project ID
			'STAGE'		: 'xxx',				# Operational Stage (setup/smt/thru/insp)
			'BOARDS'	: '0',				# number PC-Boards
			'PANELS'	: '0',				# number of panels
			'STAFF_ID'	: '0',				# staff member ID number
			'TIME'		: '00:00',			# 
			'DATE'		: '00-00-2020',		# 
			'START'		: '00:00',			# 
			'STOP'		: '00:00',			# 
			'FAULT'		: 'null',				# if production stopped early?
			'SERIAL'	: '0' }				# barcose serial number - Later


## DATA CLASS FOR JSON CONVERSION ##
class OmniData:
	CLIENT = 'TSE'
	PROJECT = 515151515
	STAGE = 'NULL'
	BOARDS = 0
	PANELS = 0
	STAFF_ID = 000
	TIME = '00:00'
	DATE = '01-01-2020'
	START = '00:00'
	STOP = '00:00'
	FAULT = 'NULL'
	SERIAL = 121212121


## UPDATE ALL INFO DATA | CREATE JSON STRING | STORE TO FILE ##
def createJSON(qrData):
	exists = 0											# append after printing contents

	## Extract data with ',' delimiter - Directly into Global Disctionary ##
	dataDict = dict(i.split('=') for i in qrData.split(','))

	## Get Startup Information - Time & Date on 'SETUP' stage ##
	## At each Stage Start/Stop - Update Time ##
	now = datetime.now()								# Get 'nows' date & time
	#current_date = now.strftime("%Y-%m-%d")			# Extract date
	current_time = now.strftime("%H:%M:%S")				# Extract time

	## Depending on KIT or STAFF qrScan ##
	dataDict['START'] 	 = current_time					# insert current time
	dataDict['STOP'] 	 = current_time					# insert current time
	#dataDict['STAFF_ID'] = '159'						# everything in strings?


	"""
	########################################
	## Attempt to Re-Order the dictionary ##
	########################################
	for key, value in dataDict.items(): 
		print(key, value)

	print("\nThis is an Ordered Dict:\n") 
	dataDict1 = OrderedDict() 
	dataDict1['CLIENT'] = '1'
	dataDict1['PROJECT'] = '2'
	dataDict1['STAGE'] = '3'
	dataDict1['BOARDS'] = '4'
	dataDict1['PANELS'] = '5'
	dataDict1['STAFF_ID'] = '6'
	dataDict1['TIME'] = '7'
	dataDict1['DATE'] = '8'
	dataDict1['START'] = '9'
	dataDict1['STOP'] = '10'
	dataDict1['FAULT'] = '11'
	dataDict1['SERIAL'] = '12'

	for key, value in dataDict1.items(): 
		print(key, value) 
	#print(dataDict)
	print("\n")
	
	## Use loop to import new data ##
	OmniData1 = OmniData()								# get object characteristics
	OmniData1.CLIENT 	= dataDict1['CLIENT']
	OmniData1.PROJECT 	= dataDict1['PROJECT']
	OmniData1.STAGE 	= dataDict1['STAGE']
	OmniData1.BOARDS 	= dataDict1['BOARDS']
	OmniData1.PANELS 	= dataDict1['PANELS']
	OmniData1.STAFF_ID 	= dataDict1['STAFF_ID']
	OmniData1.TIME 		= dataDict1['TIME']
	OmniData1.DATE 		= dataDict1['DATE']
	OmniData1.START 	= dataDict1['START']
	OmniData1.STOP 		= dataDict1['STOP']
	OmniData1.FAULT 	= dataDict1['FAULT']
	OmniData1.SERIAL 	= dataDict1['SERIAL']
	"""
	## Use loop to import new data ##
	OmniData1 = OmniData()								# get object characteristics
	OmniData1.CLIENT 	= dataDict['CLIENT']
	OmniData1.PROJECT 	= dataDict['PROJECT']
	OmniData1.STAGE 	= dataDict['STAGE']
	OmniData1.BOARDS 	= dataDict['BOARDS']
	OmniData1.PANELS 	= dataDict['PANELS']
	OmniData1.STAFF_ID 	= dataDict['STAFF_ID']
	OmniData1.TIME 		= dataDict['TIME']
	OmniData1.DATE 		= dataDict['DATE']
	OmniData1.START 	= dataDict['START']
	OmniData1.STOP 		= dataDict['STOP']
	OmniData1.FAULT 	= dataDict['FAULT']
	OmniData1.SERIAL 	= dataDict['SERIAL']


	print("Dictionary:")
	print(dataDict)
	#print("Ordered Dictionary:")
	#print(dataDict1)
	print("\n")

	#convert to JSON string
	jsonStr = json.dumps(OmniData1.__dict__)
	#print(jsonStr)										# REMOVE (view json string)
	return jsonStr
	
## Send JSON file to Google IoTCore ##
def iotCore():
	print("Send to Google")



## THE BIG KAHUNA ##
def main():	
	qrData = "data from qr code"
	jsonStr = "json string"

	#############################################
	## Read "QR_Code" data - text file for now ##
	#############################################
	file = open('qrCode.txt', 'r')
	qrData = file.read()
	file.close()
	#############################################
	print("QR STRING")
	print(qrData)

	jsonStr = createJSON(qrData)
	print("JSON STRING:")
	print(jsonStr)

	iotCore()

	print("COMPLETE!!")



if __name__ == "__main__": main()
