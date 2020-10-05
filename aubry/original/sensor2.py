'''
-Inital script that runs once connected sensor withouth any errors
-Sensor values are printed out on the terminal and not data extraction 
or processing is done

'''

from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.metawear import MetaWear
from mbientlab.metawear import *
from mbientlab.warble import *
from subprocess import call 
import time,csv
import sys,platform,six,os.path,threading,subprocess
from os import path
from time import sleep
import sys, time



ID =    MetaWear("FB:E2:B9:C5:60:AA")


class s1:

	def __init__(self,device):

		self.device = device
		self.board = self.device.board
		#self.filename = csvfilename
		self.sensordatastr = ""
		print ("Connected to sensor 1")
		self.euler_signal =  None
		self.device.connect()

	def run(self):
		
		try:
			self.euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.board, SensorFusionData.EULER_ANGLE)
			self.euler_callback = FnVoid_VoidP_DataP(lambda context,data:print("epoch: %s, euler %s\n" % (data.contents.epoch, parse_value(data))))
			libmetawear.mbl_mw_datasignal_subscribe(self.euler_signal, None, self.euler_callback)
			libmetawear.mbl_mw_sensor_fusion_enable_data(self.board, SensorFusionData.EULER_ANGLE)
			libmetawear.mbl_mw_sensor_fusion_set_mode(self.board, SensorFusionMode.NDOF)
			libmetawear.mbl_mw_sensor_fusion_write_config(self.board)
			libmetawear.mbl_mw_sensor_fusion_start(self.board)
			
			input('')
			
		except Exception as e:
			print ("RUN ERROR - {}".format(e))
			self.close()
			sys.exit()

	def close(self):
		libmetawear.mbl_mw_sensor_fusion_stop(self.board)
		libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(self.board)
		libmetawear.mbl_mw_datasignal_unsubscribe(self.euler_signal)
		self.device.disconnect()
		sleep(1)

sensor1 = s1(ID)

while True:
	try:
		#sensor1.run()
		print(...)
		time.sleep(1)
		
	# Ran into Error:
	except Exception as e:
		print ("MAIN ERROR - {}".format(e))
		sleep(2)
		s.close()
	
	## Keyboard Exit ##
	except KeyboardInterrupt:
		sensor1.close()
		print("\r\nEXIT2 PROGRAM!!")				# 
		sys.exit(0)									# 
