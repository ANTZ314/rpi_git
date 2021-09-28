"""
Quick TEXT: 
	- Open file OR Create new 
	- Read data & print
	- Overwrite
	- Re-read data & print
"""

import sys

myfile = "/home/antz/Desktop/temp/read.txt"			# CHECK FILE PATH!!

def main():
	try:
		## Read dat and print it ##
		with open(myfile, "r") as f:
			data = f.read()
			print(data)
			f.close()
	except:
			print("File was created with default string...")
			f= open(myfile,"a+")		# Create/open file then Append data 
			f.write("THRU")				# text to new file
			f.close()					# Exit the opened file

	print("File was closed")

	## OverWrite with new string ##
	with open(myfile, "w") as f:
		f.write("New data overwritten...")
		f.close()

	## Read dat and print it ##
	with open(myfile, "r") as f:
		data = f.read()
		print(data)
		f.close()

	print("File was closed again")

	print("Exit")
	sys.exit(0)	

if __name__ == "__main__": main()
