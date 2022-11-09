# -*- coding: utf-8 -*-
"""
Description:
Checks for USB device, if found,
Moves the specified file (if exists) to the USB path
"""

import sys, os, shutil
from glob import glob

path1 = "/home/pi/Pictures/4.jpg"						# path to timelapse directory

def fcount(path):
    """ Counts the number of files in a directory """
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1
    return count

def main():
	#path2 = "/media/pi/"										# path to media on RasPi
	path2 = "/media/antz/"										# path to media on PC
	try:
		path2 = glob(path2 + "*/")								# returns as list item
		print(path2[0])											# must ref item[0]
			
		## Check for USB destination path ##
		directory = os.path.dirname(path2[0])					# check in images file path
		if not os.path.exists(directory):						# if directory doesn't exist
			print("Directory doesn't exist!")					# Notify if directory was created
		else:
			print("path exists")
			try:												# [Skip if file doesn't exist]
				# Copy file to new destination
				src = path1
				dst = path2[0]
				# move the file
				shutil.move(src, dst)
				print("Move complete!")
				#sys.exit(0)									# calls exception every time???
				print("exit")
			except:
				print("No file to copy...")						# Notify user
				sys.exit(0)										# exit properly 
	except:
		print("No USB Device!")
				
if __name__ == "__main__": main()


