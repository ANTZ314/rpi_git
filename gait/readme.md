
#Gait Kinematic Tracking:


###Description:

* **scan.py** 
	* Scan for devices and display IDs
	* User selects MetaWear device ID no
	* Connects -> checks characteristics & descriptors -> diconnects

* **main1** - Primary single sensor test files. Produces separate folders of gait data at 'x' number of samples per file.

* **main2** 
	* main.py testing 3 different configurations by switching between the separate classes [main - line 17]
	* Each class has various test functions/methods (_sensClass1.py_ / _sensClass2.py_ / _sensClassA.py_)

* **main3** - Adapted _main1_ code to include multiple sensors (indipendent threads)


---
###GITHuB Code Repo:

	git pull https://github.com/ANTZ314/rpi_git.git

---
###Device ID's Identified:
[1] - F9:DC:59:47:98:6A
[2] - C6:22:44:10:EE:D9
[3] - 
[4] - 

--- 
###Device:

MetaMotionC - MMC

---
###ReStart BLE:

	sudo systemctl stop bluetooth
	sudo systemctl start bluetooth

---
**Requirements:**
Installed "Bluez" - Bluetooth Utility

---
Make sure that the Bluetooth hardware (adapter) is recognized by your OS:

	hcitool dev		# Bluetooth ON beforehand!

Devices:

	hci0	D4:3B:04:86:AB:59

Check the bluetooth status:

	systemctl status bluetooth
---

On RasPi -> Installed Bluez for the CSR 4.0 Dongle:
[Link](https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation)


---
Dependencies:

	python3 -m pip install metawear 			# installed in /home/pi/.local/lib
	sudo python3 -m pip install metawear 		# installed in /usr/local/lib

---
###UBUNTU VM BLE ERROR:

**fatal error: bluetooth/bluetooth.h: No such file or directory**

	sudo apt-get install libbluetooth-dev	# packages have unmet dependencies

	find / -name "bluetooth.h"
	
	#Output:
	/usr/src/linux-headers-5.0.0-27/include/net/bluetooth/bluetooth.h
	/usr/src/linux-headers-5.0.0-25/include/net/bluetooth/bluetooth.h


---
**Check:**

	sudo scan_connect.py 	# 'sudo' required

---
###LINKS:

[Tutorials](https://mbientlab.com/tutorials/)
[Forum:](https://mbientlab.com/community/)
[Internal Bluetooth Dis](https://scribles.net/disabling-bluetooth-on-raspberry-pi/)
[github](https://github.com/mbientlab/MetaWear-SDK-Python)
[Docs](https://mbientlab.com/cppdocs/latest/)

---
**Probelm Area:**

	Segmentation Fault!!

---
[Examples of common segfaults](https://kb.iu.edu/d/aqsj#:~:text=A%20segmentation%20fault%20(aka%20segfault,write%20an%20illegal%20memory%20location.)

Segmentation fault is a generic one, there are many possible reasons for this:

* Low memory
* Faulty Ram memory
* Fetching a huge data set from the db using a query (if the size of fetched data is more than swap mem)
* wrong query / buggy code
* having long loop (multiple recursion)

---
[OpenBlas recommends you set it to single thread mode](https://github.com/ageitgey/face_recognition/issues/294
	https://stackoverflow.com/questions/10035541/what-causes-a-python-segmentation-fault)

---
Check and Increase Stack Size:

Current stack size:

	ulimit -s 	-OR-	ulimit -a

Increase to 1Mb:
	
	ulimit -s 1024

---
**ERROR MESSAGE:**
"Failed to write value to characteristic(Error trying to issue command mid state)"
[Failed to write value to characteristic(Error trying to issue command mid state)](https://mbientlab.com/community/discussion/2733/failed-to-write-value-to-characteristic-error-trying-to-issue-command-mid-state)

**Other SegFault:**
[Link1](https://mbientlab.com/community/discussion/comment/10334#Comment_10334)

	data_fuser.py segmentation faults during libmetawear.mbl_mw_datasignal_subscribe()

[Link2](https://mbientlab.com/community/discussion/2761/data-fuser-py-segmentation-faults-during-libmetawear-mbl-mw-datasignal-subscribe)


------------
Aubry LINKS:
------------
[mbientlab](https://mbientlab.com/community/discussion/3446/multiple-metamotionc-connection-error)

[Suggested Parsing](
https://github.com/mbientlab/MetaWear-SDK-Python/search?p=1&q=parse_value&unscoped_q=parse_value)
