"""
Description:
	My restructured class version of Aubry's class
	Removed seemingly unnecessary lines
	Added comments & some exception catches
	Taken aspect from other class -> dictionary creation
	--> Find cause of segmentation fault - memory?
	

Class called by 'main.py'
"""
## IMPORT DEPENDENCIES ##
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.metawear import MetaWear
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
		self.device = MetaWear(device)
		self.board = self.device.board
		#self.sensordatastr = ""					# Don't seem to need this ? ?
		self.euler_signal =  None					# only needed in 'close()'
		
		## Attempt to connect to Device ##
		try:
			self.device.connect()
		except:
			print("FAILED TO CONNECT...")


	## SETUP VARIOUS VARIABLES ##
	def startup(self):
		
		try:
			self.sensordatastr = ""
			self.EulerAngels= None
			self.euler_signal =  None
			
			## Create Data Dictionary ##
			self.sensorData = {"epoch"	:0,
							   "heading":0,
							   "pitch"	:0,
							   "roll"	:0,
							   "yaw"	:0,
							   "logs"	:0}				# removed 'filename'
						   
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
			print("\r\nEscape (START) - Device Closed...")
			sys.exit(0)	
		## Unknown Error ##
		except:
			print("\r\nUnexpected Error:", sys.exc_info()[0])
			self.DevClose()
			print("Device Closed Properly...")
			sys.exit() 


	## CONTINUOUS RUN - Threaded? ##
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
			sensor1.DevClose()
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


	## EXTRACT THE DEVICE DATA TO DICTIONARY ##
	def data_handler(self,content,data):
		
		## Extract data values? ##
		EulerAngels = parse_value(data)
		pi = pointer(EulerAngels)
		#self.sensordatastr = str(data.contents.epoch)+","+ str(("%.4f" %pi.contents.heading)) +","+ str(("%.4f" %pi.contents.pitch))+","+ str(("%.4f" %pi.contents.roll))+","+str(("%.4f" %pi.contents.yaw))
		
		## Update Dictionary data fields ##
		self.sensorData["epoch"] 	= (data.contents.epoch)
		self.sensorData["heading"] 	= ("%.3f" %pi.contents.heading)
		self.sensorData["pitch"] 	= ("%.3f" %pi.contents.pitch)
		self.sensorData["roll"] 	= ("%.3f" %pi.contents.roll)
		self.sensorData["yaw"]  	= ("%.3f" %pi.contents.yaw)
		self.sensorData["logs"] 	= self.cnt
		
		self.cnt = self.cnt +1
		print (self.sensorData)								# View Dictionary
		
