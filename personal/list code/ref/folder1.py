# -*- coding: utf-8 -*-
"""
Python 2.7
-> get list of folder names within a folder
-> if existing folders:
	=> check directory's last character "dir_0, dir_1, folder_2..."
	=> compare character sizes and save highest number
	=> create new directory with incremented name
-> if no directories in parent dir:
	=> create new directory for images "dir_0"

Problem: places new folder outside folder checking!!
"""

import sys
import os

""" Counts the number of files in a directory """
def fcount1(path):
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1

    return count
    
""" Counts the number of directories in a parent directory """
def fcount2(path):
    count = 0
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            count += 1

    return count

""" MAIN FUNCTION """
def main():
	comp = 0
	temp = 0
	size = 0
	new_dir    = "/home/antz/0_samples/scrapy/"					# path to new folder location
	file_path1 = "/home/antz/0_samples/scrapy/"					# path to images
	file_path2 = "/home/antz/0_samples/scrapy/dir_0"			# path to wrong directory
	folder     = "scrapy/"
	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path2)						# check in images file path
	if not os.path.exists(directory):							# if directory doesn't exist
		print("Image Directory Created!")						# Notify if directory was created
		os.makedirs(directory)									# Create the directory

	else:
		print(str(file_path2))
		try:													# 
			folders = fcount2(file_path1)						# Get the  number of child directories
			print ("folders {}".format(folders))				# 
			# get the name of all pre-existing folders
			root, dirs, files = os.walk(file_path1).next()		# step thru contents
			for i in range (0,folders):							# for each folder 
				dir_name = dirs[i]								# Get each name for comparison
				#print(dir_name[4])								# print last character ASCII
				temp = ord(dir_name[4])							# get last character & convert to integer for comparison
				if comp < temp:									# compare with previous highest number
					comp = temp									# keep highest number (else keep temp)
			size = len(new_dir)
			new_dir = new_dir[:(size-1)] + str(unichr(comp+1))	# convert back & place into new dir name
			print("Create new directory: {}".format(new_dir))	# show string							
			os.makedirs(new_dir)								# make the new directory
		except:
			print("Exception Ocurred...")
		
		
if __name__ == "__main__": main()
