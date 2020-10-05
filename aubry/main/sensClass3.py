"""
Class called by 'main.py'
"""
## IMPORT DEPENDENCIES ##
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.metawear import MetaWear
from mbientlab.metawear import *
from mbientlab.warble import *

#from subprocess import call 
#import platform,six,threading,subprocess
import time, csv, os, sys							# os.path

#ID1 = MetaWear("FB:E2:B9:C5:60:AA")


class sens1:
	filename = 'log1.csv'							# Log file - remove later
	
	## INSTANTIATE THE CLASS ##
	def __init__(self, **kwargs):
		print("Go Sensor Class!!")

		
	## INITIALISE THE DEVICE CONNECTION ##
	def DevConnect(self, device):
		self.device = MetaWear(device)
		self.board = self.device.board
		#self.sensordatastr = ""					# Don't seem to need this ? ?
		self.euler_signal =  None					# only needed in 'close()'
		print ("Connected to sensor 1")
		try:
			self.device.connect()
		except:
			print("FAILED TO CONNECT...")


	## SETUP VARIOUS VARIABLES ##
	def startup(self):
		self.sensordatastr = ""
		self.EulerAngels= None
		self.euler_signal =  None
		self.checkLogFiles(self.filename)
		
		## SOME MAIN FUNCTION SHIT ##
		#self.euler_callback = FnVoid_VoidP_DataP(self.data_handler)
		
		## Create Data List/Dictionary ##
		self.sensorData = {"Name":self.filename,"epoch":0,"heading":0,"pitch":0,"roll":0,"yaw":0,"logs":0}

	
	## CHECK FOR AND/OR CREATE CSV FILE ##
	def checkLogFiles(self,filename):
		## Does CSV file exist ##
		res =  os.path.exists(filename)
		## Create if doesn't exist ##
		if res == False:
			print("no file found, creating file")
			f = open(filename,"w+")
			f.close()
			print ("file created")
			
			with open(filename, mode='w+') as csv_file:
				fieldnames = ['epoch', 'pitch', 'roll','yaw']
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ',')
				writer.writeheader()
		## File already existed ##
		else:
			print ("File found in the path")


	## CONTINUOUS RUN ##
	def DevRun(self):
		try:
			self.euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.board, SensorFusionData.EULER_ANGLE)
			self.euler_callback = FnVoid_VoidP_DataP(lambda context,data:print("epoch: %s, euler %s\n" % (data.contents.epoch, parse_value(data))))
			libmetawear.mbl_mw_datasignal_subscribe(self.euler_signal, None, self.euler_callback)
			libmetawear.mbl_mw_sensor_fusion_enable_data(self.board, SensorFusionData.EULER_ANGLE)
			libmetawear.mbl_mw_sensor_fusion_set_mode(self.board, SensorFusionMode.NDOF)
			libmetawear.mbl_mw_sensor_fusion_write_config(self.board)
			libmetawear.mbl_mw_sensor_fusion_start(self.board)
			#input('')			# what is this for ? ? - Does nothing
			
		except Exception as e:
			print ("RUN ERROR - {}".format(e))
			self.close()
			print("Device closed properly...")
			sys.exit()
	
	
	## CLOSE THE CONNECTION PROPERLY ##
	def DevClose(self):
		libmetawear.mbl_mw_sensor_fusion_stop(self.board)
		libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(self.board)
		libmetawear.mbl_mw_datasignal_unsubscribe(self.euler_signal)
		self.device.disconnect()
		time.sleep(1)
