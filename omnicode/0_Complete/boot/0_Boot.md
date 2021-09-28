# Run from Boot / Startup:

---
### METHOD 1: sudo crontab:		[YES]

If necessary, create "master.py" that runs the full script with extensions:

Run:
```
sudo crontab -e
```
Select [2] **nano** and add the following:
```
# must fork code with '&' character
#@reboot python /home/pi/security/main.py --conf /home/pi/security/conf.json &
@reboot sleep 35 && sudo python /home/pi/master.py &
```

**If still not running at boot, use Method 2**

---
### METHOD 2: crontab + xterm: [YES]

**Not running full code at boot - FIX:**

The following will install "xterm" and then run new terminal window at boot before executing python command inside that terminal window.

* Run full updates + upgrades

* Update to latest PIP:
```
/usr/bin/python -m pip install --upgrade pip
```
* Install:
```
sudo apt install xterm
```
* Create **booot.sh** (make executable):
```
#!/bin/bash

DISPLAY=:0 xterm -hold -e bash -c "python /home/pi/main/main.py"  &
```
* Add to **crontab -e** (with 45 sec delay):
```
crontab -e
# Add the following
@reboot sleep 45 && /home/pi/boot.sh
```

---
### METHOD 3: rc.local		[NO]

Run:
```
sudo nano /etc/rc.local
```
Insert:
```
# must fork code with '&' character
sudo python /home/pi/sample.py &
```

**NOTE:**
If you add a script into /etc/rc.local, it is added to the boot sequence. 
If your code gets stuck then the boot sequence cannot proceed. So be careful as to which code you 
are trying to run at boot and test the code a couple of times. You can also get the script’s 
output and error written to a text file (say log.txt) and use it to debug.

Eg.
```
sudo python /home/pi/main/main.py & > /home/pi/Desktop/log.txt 2>&1
```

---
### METHOD 4: .bashrc		[NO]

**Runs when:**

* log in
* Terminal is opened
* SSH connection

Run:
```
sudo nano /home/pi/.bashrc
```
Insert:
```
sleep 20        # 20 second delay
sudo python /home/pi/main/main.py
```

**Note:**
Added delay before running to allow for all minor processes to be running first

---
### To kill the Process:

In terminal:
```
ps aux
```
Find the PID of the python script
```
sudo kill "ṔID"	# eg. sudo kill 541
```

---
### RasPi Boot Publishing Error:

**ERROR:**
```
errors = backend._consume_errors()
           assert errors[0].lib == backend._lib.ERR_LIB_RSA
           AssertionError
```
* Update to latest PIP:
```
/usr/bin/python -m pip install --upgrade pip
```
* Install package dependancies:
```
sudo apt install libffi-dev
sudo apt install libssl-dev
```
* Update to latest 'cryptography':
```
sudo pip install cryptography --upgrade
-OR-
sudo pip install -U cryptography
```
* Update + Upgrade and reboot
```
sudo apt update
sudo apt -y upgrade
sudo reboot
```