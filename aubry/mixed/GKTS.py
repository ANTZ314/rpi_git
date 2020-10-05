# usage: python scan_connect.py

from __future__ import print_function
from mbientlab.metawear import MetaWear
from mbientlab.metawear.cbindings import *
from mbientlab.warble import * 
from mbientlab.metawear import *

from datetime import *
import json, csv
import sys,platform,six
from time import sleep


try:
	from StringIO import StringIO
	
except ImportError:
	
	from io import StringIO
cnt = 0
	
#I hard coded the address in, just not displaying it here
device = MetaWear("FB:E2:B9:C5:60:AA")
device.connect()
board = device.board
i = 0
output = StringIO()
buf = [100]
limit = 10
char = None
lis_t = [80]

#_______________________________________________________________________

def csvLog():
	
	fin = open("log.csv","rt")
	updateData = fin.read()	
	oldData = updateData
	updateData = updateData.replace(updateData,buf[0:89])
	fin.close()
	
	updateData = updateData.replace(" ","")
	updateData = updateData.replace("{","")
	updateData = updateData.replace("}"," ")
	updateData = updateData.replace(" ","")
	updateData = updateData.replace("epoch:","")
	updateData = updateData.replace("heading:","")
	updateData = updateData.replace("pitch","")
	updateData = updateData.replace("roll:","")
	updateData = updateData.replace("yaw:","")
	updateData = updateData.replace(":","")		
	
	fin = open("log.csv","wt")
	fin.write(updateData)
	fin.close()	
	
	fin = open("log.csv","rt")
	updateData = fin.read()
	fin.close()
#_______________________________________________________________________

try:
	
	euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(board, SensorFusionData.EULER_ANGLE)	
	#euler_callback = FnVoid_VoidP_DataP(lambda context, data: output.write("epoch: %s, euler %s\n" % (data.contents.epoch, parse_value(data))))
	
	euler_callback = FnVoid_VoidP_DataP(lambda context, data: output.write("epoch:%s,%s\n" % (data.contents.epoch, parse_value(data))))
	
	libmetawear.mbl_mw_datasignal_subscribe(euler_signal, None, euler_callback)
	libmetawear.mbl_mw_sensor_fusion_enable_data(board, SensorFusionData.EULER_ANGLE)
	libmetawear.mbl_mw_sensor_fusion_set_mode(board, SensorFusionMode.NDOF)
	libmetawear.mbl_mw_sensor_fusion_write_config(board)
	
	while True:
		
		libmetawear.mbl_mw_sensor_fusion_start(board)
		sleep(0.3)
		libmetawear.mbl_mw_sensor_fusion_stop(board)
		
				
		buf = str(output.getvalue())
		output = StringIO()
		csvLog()
				
		with open('log.csv') as csvfile:
			
			readcsv = csv.reader(csvfile,delimiter=',')
			for row in readcsv:
				timeStamp = row[0]
				pitch = row[2]
				roll = row[3]
				yaw = row[4]
				break
				
		print (pitch,roll,yaw)
				

	libmetawear.mbl_mw_sensor_fusion_stop(board)
	libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(board)
	libmetawear.mbl_mw_datasignal_unsubscribe(euler_signal)

	device.disconnect()
	print ('disconnected')
	sleep(1)
	
except:
	
	libmetawear.mbl_mw_sensor_fusion_stop(board)
	libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(board)
	libmetawear.mbl_mw_datasignal_unsubscribe(euler_signal)

	device.disconnect()
	print ('disconnected')
#_______________________________________________________________________
