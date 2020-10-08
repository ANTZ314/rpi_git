"""
Description:
	My restructured class version of Aubry's class
	Removed seemingly unnecessary lines & commented lines
	Added comments & some exception catches
	Find cause of segmentation fault - memory?
	

Class called by 'main.py'
"""
## IMPORT DEPENDENCIES ##
from __future__ import print_function
from mbientlab.metawear import *
from mbientlab.warble import *

## Various System Tools ##
import time, os, sys


class sens1:
	## INSTANTIATE THE CLASS ##
	def __init__(self, **kwargs):
		self.cnt = 0
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
		self.euler_signal =  None			# runs without
			
		## Create Data Dictionary ##
		self.sensorData = {"epoch"	:0,
						   "heading":0,
						   "pitch"	:0,
						   "roll"	:0,
						   "yaw"	:0,
						   "logs"	:0}				# removed 'filename'
		print("necessary?")


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
			
			#self.e.wait()		# what is this for ? ? - removed
			#input('')			# what is this for ? ? - removed
			
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
		self.device = MetaWear(device)
		self.board = self.device.board
		self.euler_signal =  None
		
		## Attempt to RE-Connect to Device ##
		try:
			self.device.connect()
		except:
			print("FAILED TO CONNECT...")
	

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
		if tmpHead   > 999 or tmpHead   < -999:
			tmpHead  = 999.000		# Only needed here - SAME VALUES?
		if tmpPitch  > 999 or tmpPitch   < -999:
			tmpPitch = 999.000		# Only needed here - SAME VALUES?
		if tmpRoll   > 999 or tmpRoll   < -999:
			tmpRoll  = 999.000
		if tmpYaw    > 999 or tmpYaw   < -999:
			tmpYaw   = 999.000
		
		## Get bottom of Epoch ##
		num = data.contents.epoch
		num = int(str(num)[-6:])
		
		## Update Dictionary data fields ##
		self.sensorData["epoch"] 	= (num)				# epoch type = int
		self.sensorData["heading"] 	= ("%.3f" %tmpHead)
		self.sensorData["pitch"] 	= ("%.3f" %tmpPitch)
		self.sensorData["roll"] 	= ("%.3f" %tmpRoll)
		self.sensorData["yaw"]  	= ("%.3f" %tmpYaw)
		self.sensorData["logs"] 	= self.cnt
		"""
		self.sensorData["epoch"] 	= (data.contents.epoch)
		self.sensorData["heading"] 	= ("%.3f" %pi.contents.heading)
		self.sensorData["pitch"] 	= ("%.3f" %pi.contents.pitch)
		self.sensorData["roll"] 	= ("%.3f" %pi.contents.roll)
		self.sensorData["yaw"]  	= ("%.3f" %pi.contents.yaw)
		self.sensorData["logs"] 	= self.cnt
		"""
		self.cnt = self.cnt +1
		print(self.sensorData)								# View Dictionary
		
		
