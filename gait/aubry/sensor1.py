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

 

#subprocess.run("sudo hciconfig hci1 reset",shell=True)

f = 'log1.csv'
ID = "FB:E2:B9:C5:60:AA"

class s1:
	
	def __init__(self, filename,sensorAddress):

		self.device = MetaWear(sensorAddress)
		self.board = self.device.board
		self.filename = filename
		self.device.connect()
		self.cnt = 0
		print("connected to", self.device.address)
		sleep(2)
		self.sensordatastr = ""
		self.EulerAngels= None
		self.euler_signal =  None
		self.checkLogFiles(self.filename)
		self.euler_callback = FnVoid_VoidP_DataP(self.data_handler)
		self.sensorData = {"Name":self.filename,"epoch":0,"heading":0,"pitch":0,"roll":0,"yaw":0,"logs":0}
		self.checkLogFiles("log1.csv")
		
########################################################################

	def close(self):

		libmetawear.mbl_mw_sensor_fusion_stop(self.board)
		libmetawear.mbl_mw_sensor_fusion_clear_enabled_mask(self.board)
		libmetawear.mbl_mw_datasignal_unsubscribe(self.euler_signal)
		self.device.disconnect()
		sleep(1)
		print("DISCONNETED")
	
########################################################################

	def checkLogFiles(self,filename):
		
		path.exists(filename)
		
		res =  path.exists(filename)
		if res == False:
			print("no file found, creating file")
			f = open(filename,"w+")
			f.close()
			print ("file created")
			
			with open(filename, mode='w+') as csv_file:
				fieldnames = ['epoch', 'pitch', 'roll','yaw']
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ',')
				writer.writeheader()
		else:
			print ("File found in the path")

########################################################################

	def logData(self,filename,data):
		
		f = open(filename,"a+")
		f.write(data)
		f.write("\n")
		f.close()
	
########################################################################
	def data_handler(self,content,data):

		EulerAngels = parse_value(data)
		#print (EulerAngels)
		pi = pointer(EulerAngels)
		self.sensordatastr = str(data.contents.epoch)+","+ str(("%.4f" %pi.contents.heading)) +","+ str(("%.4f" %pi.contents.pitch))+","+ str(("%.4f" %pi.contents.roll))+","+str(("%.4f" %pi.contents.yaw))
		#print (sensordatastr)
		self.logData(self.filename,self.sensordatastr)
		#sleep(0.05)
		self.sensorData["epoch"] = (data.contents.epoch)
		self.sensorData["heading"] = ("%.4f" %pi.contents.heading)
		self.sensorData["pitch"] = ("%.4f" %pi.contents.pitch)
		self.sensorData["roll"] = ("%.4f" %pi.contents.roll)
		self.sensorData["yaw"]  = ("%.4f" %pi.contents.yaw)
		self.sensorData["logs"] = self.cnt
		self.cnt = self.cnt +1
		print (self.sensorData)
		sleep(0.02)	
		
	def run(self):

		try:
			self.euler_signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.board, SensorFusionData.EULER_ANGLE)
			
			libmetawear.mbl_mw_datasignal_subscribe(self.euler_signal, None, self.euler_callback)
			libmetawear.mbl_mw_sensor_fusion_enable_data(self.board, SensorFusionData.EULER_ANGLE)
			libmetawear.mbl_mw_sensor_fusion_set_mode(self.board, SensorFusionMode.NDOF)
			libmetawear.mbl_mw_sensor_fusion_write_config(self.board)
			libmetawear.mbl_mw_sensor_fusion_start(self.board)
			self.e.wait()
			input("")

		except KeyboardInterrupt as e:
			print (e)
			self.close()
			sys.exit()	
########################################################################


s = s1(f,ID)

while True:
	try:
		s.run()
	except Exception as e:
		print (e)
		sleep(5)
		s.close()
		

