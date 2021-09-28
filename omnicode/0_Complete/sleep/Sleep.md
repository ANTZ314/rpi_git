# Screensaver - Sleep Mode - Blank Screen

### METHOD 0 - XSCREENSAVER:
**[Worked]**

Install:

	sudo apt install xscreensaver

Start Menu-> preferences -> Xscreensaver -> Disable

**NOTE:**

* Disabled Screen Blanking 
* Touch wake-up only works with HDMI

---
### METHOD 1 - XSET:

**[Didn't Work]**

To see all commands:

	xset -?
	or
	man xset

To see current settings:

	DISPLAY=:0 xset q

Turn blanking off:

	xset -display :0 dpms 0 0 0
	# Extra commands:
	xset -display :0 dpms force off
	xset -display :0 dpms force off

Turn blanking on:

	xset dpms 0 0 900	# 15 min timeout

#### xset Errors:

If using LCD Display:

	Error: xset: unable to open display ""

Need to set which display to use:

	export DISPLAY=:0
	# If error persists
	xset:  unable to open display ":0"

---
### METHOD 2 - AUTOSTART:

**[Didn't Work]**

	sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

Should look like the following:

	@lxpanel --profile LXDE-pi
	@pcmanfm --desktop --profile LXDE-pi
	@xset s noblank
	@xset s off
	@xset -dpms
	# @xscreensaver -no-splash
	@point-rpi

---
### METHOD 3 - VBETOOL:
**(2020) - untested**

Can try **vbetool** instead:

	sudo vbetool dpms off

---
### METHOD 4 - LIGHTDM.CONF:
**(2020) - untested**

	sudo nano /etc/lightdm/lightdm.conf
	
Add the following lines to the [SeatDefaults] section:

	# don't sleep the screen
	xserver-command=X -s 0 dpms

---
### METHOD 5 - xorg.config:
**(2020) - untested**

Create archive /etc/X11/xorg.conf with this content:

	Section "ServerFlags"
	Option "blank time" "0"
	Option "standby time" "0"
	Option "suspend time" "0"
	Option "off time" "0"
	EndSection

Save and restart.

---
### METHOD 6 - setterm Method:
**[Didn't Work]**

To view system blanking:

	cat /sys/module/kernel/parameters/consoleblank

Set the system blanking time:

	setterm -blank 600
	or
	setterm -blank 0
	
**Notes:**  - '0' should be blanking disabled.

---
### METHOD 7 - Backlight Dimmer:
**(2020) - untested**

[GITHUB Installation instructions](https://github.com/DougieLawson/backlight_dimmer)

**Note:** Not working on RPi4?