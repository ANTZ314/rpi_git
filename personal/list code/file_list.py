# -*- coding: utf-8 -*-
"""
Description:
Create a list of all folders and the files within

Python ??
-> Primary List of Directory Names - [List]						| x
-> Get number of sub-direcotries								| x
-> Get number of files in each sub-directory					| x
-> Directory name heading & list files within					| .
-> Sub-sub-folders??											| .

-> If file doesn't exist, file is created						| .
-> If exists, opens existing file								| .
-> Appends the names of each file in the folder of "file_path2"	| .
-> Write to directory contents to the file						| .
"""

import sys
import os

def fcount(path):
    """ Counts the number of files in a directory """
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1

    return count

def main():
	cnt = 0													# generic counter
	file_path1 = "/home/antz/0_samples/digitRec/"			# path with sub-directories
	file_path2 = "/home/antz/0_samples/colour/"				# path to directory with files
	exists = 0												# Append after printing contents
	file_No = 0												# 
	sub_dir = []
	no_dir = 0

	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path2)					# check in images file path
	
	## Print sub-directories ##
	sub_dir = os.listdir(file_path1)

	no_dir = len(sub_dir)

	for cnt in range(0, no_dir):
		newPath = file_path1 + sub_dir[cnt]
		file_No = fcount(newPath)
		print(newPath + " size: " + str(file_No))
		#file= open("FileCount.txt","a+")
		file_list = os.listdir(newPath)
		#print(file_list)
		for cnt in range(0, file_No):
			print(file_list[cnt])
		#	file.write("{0}\r\n".format(os.listdir(file_list)[cnt]))

	"""
	if not os.path.exists(directory):						# if directory doesn't exist
		os.makedirs(directory)								# Create the directory
		print("Image Directory Created!")					# Notify if directory was created
	else:
		file_No = fcount(file_path2)						# get the number of images in the folder
		print("Image Directory Exists!")					# Notify if image directory exists
		try:												# [Skip if file doesn't exist]
			exists = 0										# Clear flag
			file = open('FileCount.txt', 'r') 				# Open to read file
			print (file.read())								# Print the contents
			file.close()									# Close the file
		except:
			print("No file to read...")						# Notify user
			file= open("FileCount.txt","a+")				# Append to file (will create file also)
			for cnt in range(0, file_No):					# for each file in image folder
				file.write("{0}\r\n".format(os.listdir(file_path2)[cnt]))   # append the file name
			file.write("=" * 18)							# mark last entry
			file.close()									# close the file
			exists = 1										# Don't append twice if file exists
			
		if exists == 0:										# Append after printing contents
			file= open("FileCount.txt","a+")				# Append to file (no need to create file)
			for cnt in range(0, file_No):					# for each file in image folder
				file.write("{0}\r\n".format(os.listdir(file_path2)[cnt]))   # append the file name
			file.write("=" * 18)							# mark last entry
			file.close()									# close the file
			print ("The File was appended...")
		else:												# Notify of file creation
			print ("The File was created...")				# notification	
		"""

if __name__ == "__main__": main()
