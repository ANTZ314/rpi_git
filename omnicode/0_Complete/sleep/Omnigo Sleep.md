# Disable Sleep Mode Completely

## XSET:

**To see current settings:**

	DISPLAY=:0 xset q

---
#### Method 1:

	sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

Should look like the following:

	@lxpanel --profile LXDE-pi
	@pcmanfm --desktop --profile LXDE-pi
	@xset s noblank
	@xset s off
	@xset -dpms
	# @xscreensaver -no-splash
	@point-rpi

## Method 2:

	sudo nano /boot/cmdline.txt
	
To include:

	consoleblank=0
	
## Method 3:
	
	setterm -blank 0

Check:

	cat /sys/module/kernel/parameters/consoleblank