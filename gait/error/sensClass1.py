"""
Description:
	Seems to be original tutorial code
	After connection
	Prints output data directly to console - ERROR
	Questions:
		Format of data?
		Extraction point?

Class called by 'main.py'
"""
## IMPORT DEPENDENCIES ##
from __future__ import print_function
from mbientlab.warble import *
from mbientlab.metawear import *

from subprocess import call 
import time,csv
import sys,platform,six,os.path,threading,subprocess
from os import path
from time import sleep

#ID1 = MetaWear("FB:E2:B9:C5:60:AA")				# REMOVED

class sens1:
	## INSTANTIATE THE CLASS ##
	def __init__(self, **kwargs):
		print("Go Sensor Class!!")

		
	## INITIALISE THE DEVICE CONNECTION ##
	def DevConnect(self, device):
		self.device = MetaWear(device)
		self.board = self.device.board
		#self.sensordatastr = ""					# Don't seem to need this ? ?
		self.euler_signal =  None
		try:
			self.device.connect()					# Attempt connection
		except:
			print("FAILED TO CONNECT...")

	## Do Nothing Here - For other Class ##
	def startup(self):
		print("For Posterity...")

	## CONTINUOUS RUN ##
	def DevRun(self):
		try:
			## Get data and print to console ##
			self.euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.board, SensorFusionData.EULER_ANGLE)
			self.euler_callback = FnVoid_VoidP_DataP(lambda context,data:print("epoch: %s, euler %s\n" % (data.contents.epoch, parse_value(data))))
			
			## Required for data extraction ##
			libmetawear.mbl_mw_datasignal_subscribe(self.euler_signal, None, self.euler_callback)
			libmetawear.mbl_mw_sensor_fusion_enable_data(self.board, SensorFusionData.EULER_ANGLE)
			libmetawear.mbl_mw_sensor_fusion_set_mode(self.board, SensorFusionMode.NDOF)
			libmetawear.mbl_mw_sensor_fusion_write_config(self.board)
			libmetawear.mbl_mw_sensor_fusion_start(self.board)
			#input('')								# Don't seem to need this ? ?
			
		except OSError as err:
			print ("OS ERROR {}".format(err))
			self.DevClose()
			print("Device closed properly...")
			sys.exit()
		except ValueError:
			print("Error with variable...")
			self.DevClose()
			print("Device closed properly...")
			sys.exit()
		except:
			print("Unexpected Error:", sys.exc_info()[0])
			self.DevClose()
			print("Device closed properly...")
			sys.exit()
	
	## CLOSE THE CONNECTION PROPERLY ##
	def DevClose(self):
		libmetawear.mbl_mw_sensor_fusion_stop(self.board)
		libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(self.board)
		libmetawear.mbl_mw_datasignal_unsubscribe(self.euler_signal)
		self.device.disconnect()
		sleep(1)
