"""
Date: 		01-03-2021
Editted:	A.Smith

Description:
	Class called by 'main.py'
	Class for initialisation and logging od sensor 2
"""
## IMPORT DEPENDENCIES ##
from __future__ import print_function
from mbientlab.metawear import *
from mbientlab.warble import *

## Various System Tools ##
import time, os, sys
import csv											# write data to file


class sens2:
	filename = 'log2.csv'							# Log file - CSV format
	fileCnt = 0
	
	## INSTANTIATE THE CLASS ##
	def __init__(self, **kwargs):
		self.cnt = 0
		self.cnt2 = 0
		print("Go Sensor Class!!")

		
	## INITIALISE THE DEVICE CONNECTION ##
	def DevConnect(self, device):
		conPass = True
		
		self.device = MetaWear(device)
		self.board = self.device.board
		#self.euler_signal =  None					# only used in 'close()' ?
		
		## Attempt to connect to Device ##
		try:
			self.device.connect()
		except:
			print("FAILED TO CONNECT...")
			conPass = False
			
		return conPass


	## SETUP VARIOUS VARIABLES ##
	def startup(self):
		self.sensordatastr = ""
		self.EulerAngels= None
		self.euler_signal =  None				# runs without this?
			
		## Create Data Dictionary ##
		self.sensorData = {"epoch"	:0,
						   "heading":0,
						   "pitch"	:0,
						   "roll"	:0,
						   "yaw"	:0,
						   "logs"	:0}			# removed 'filename'
		
		self.filename = ("log{}.csv".format(str(self.fileCnt)))
		#self.checkLogFiles(self.filename)		# create/check log.txt file
		print("Log File Done...")				# indentation error?


	## CONTINUOUS RUN ##
	def DevRun(self):
		try:
			## Retrieve Sensor Data? ##
			self.euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.board, SensorFusionData.EULER_ANGLE)
			
			## View Data Directly - Removed ##
			#self.euler_callback = FnVoid_VoidP_DataP(lambda context,data:print("epoch: %s, euler %s\n" % (data.contents.epoch, parse_value(data))))
			
			## From initi function ##
			self.euler_callback = FnVoid_VoidP_DataP(self.data_handler)
			
			## All required for Data Extraction? ##
			libmetawear.mbl_mw_datasignal_subscribe(self.euler_signal, None, self.euler_callback)
			libmetawear.mbl_mw_sensor_fusion_enable_data(self.board, SensorFusionData.EULER_ANGLE)
			libmetawear.mbl_mw_sensor_fusion_set_mode(self.board, SensorFusionMode.NDOF)
			libmetawear.mbl_mw_sensor_fusion_write_config(self.board)
			libmetawear.mbl_mw_sensor_fusion_start(self.board)
			
			
			## Only check every 5 sec ? ? ? ##
			## Return "still runnning" ##
			#return self.cnt
						
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
			self.DevClose()
			print("\r\nEscape (RUN) - Device Closed...")
			sys.exit(0)	
		## Unknown Error ##
		except:
			print("\r\nUnexpected Error:", sys.exc_info()[0])
			self.DevClose()
			print("Device Closed Properly...")
			sys.exit()
	
	
	## CLOSE THE CONNECTION PROPERLY ##
	def DevClose(self):
		libmetawear.mbl_mw_sensor_fusion_stop(self.board)
		libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(self.board)
		libmetawear.mbl_mw_datasignal_unsubscribe(self.euler_signal)
		self.device.disconnect()
		time.sleep(1)


	## INITIALISE THE DEVICE CONNECTION ##
	def DevReConnect(self, device):
		conPass = True							# CONNECTION STATUS
		
		self.device = MetaWear(device)
		self.board = self.device.board
		self.euler_signal =  None
		
		## Attempt to RE-Connect to Device ##
		try:
			self.device.connect()
		except:
			print("FAILED TO CONNECT...")
			conPass = False
			
		return conPass
	

	## EXTRACT THE DEVICE DATA TO DICTIONARY ##
	def data_handler(self,content,data):
		
		## Extract data values? ##
		EulerAngels = parse_value(data)
		pi = pointer(EulerAngels)
		
		## Temporary Copy of the Data ##
		tmpHead	 = pi.contents.heading
		tmpPitch = pi.contents.pitch
		tmpRoll	 = pi.contents.roll
		tmpYaw	 = pi.contents.yaw
		
		
		## Limit Extreme Output Values ##
		if tmpHead   > 999 or tmpHead  < -999:
			tmpHead  = 999.000								# SAME VALUES?
		if tmpPitch  > 999 or tmpPitch < -999:
			tmpPitch = 999.000								# SAME VALUES?
		if tmpRoll   > 999 or tmpRoll  < -999:
			tmpRoll  = 999.000
		if tmpYaw    > 999 or tmpYaw   < -999:
			tmpYaw   = 999.000
		
		## Get bottom of Epoch ##
		num = data.contents.epoch
		num = int(str(num)[-6:])
				
		## Update Dictionary data fields ##
		self.sensorData["epoch"] 	= (num)					# epoch type = int
		self.sensorData["heading"] 	= ("%.3f" %tmpHead)
		self.sensorData["pitch"] 	= ("%.3f" %tmpPitch)
		self.sensorData["roll"] 	= ("%.3f" %tmpRoll)
		self.sensorData["yaw"]  	= ("%.3f" %tmpYaw)
		self.sensorData["logs"] 	= self.cnt
		
		## Backup every one to csv file ##
		#self.logData(self.filename,self.sensordatastr)		# backup original data
		self.logData(self.sensorData)						# backup disctionary
		
		#self.cnt = self.cnt + 1							# increment counter
		self.cnt += 1										# increment counter
		
		## overall RUN Exit/Re-Connect ##
		if self.cnt >= 9999:
			self.cnt = 0									# External funtion
		
		## print every 100th Data list ##
		if self.cnt % 100 == 0:
			print(self.sensorData)							# View Dictionary
			print(self.filename)
			if self.cnt2 == 10:
				self.fileCnt += 1							# increment file counter
				self.filename = ("log{}.csv".format(str(self.fileCnt)))	# increment filename
				self.cnt2 = 0
			self.cnt2 += 1
	

	## LOG DATA TO CSV FILE ##
	def logData(self,data):
		
		## OPTION 3 ##
		with open(self.filename, "+a") as f:
			w = csv.writer(f)
			w.writerow(data.values())
	

	## CHECK/CREATE CSV FILE ##
	def checkLogFiles(self,filename):
		## Does CSV file exist ##
		res =  os.path.exists(filename)
		## Create if doesn't exist ##
		if res == False:
			f = open(filename,"w+")
			f.close()
			print ("File Created")
		## File already existed ##
		else:
			print ("File Found...")
	
	
	## CHECK STILL RUNNING ##
	def logVal(self):
		#print("Cnt {}".format(self.cnt))
		## Return Log Value ##
		return self.cnt
