
#README:

####List to  install:

pip
Pillow 4.1.1
h5py
h5py-2.7.0.dist-info
keras
Keras-2.0.5.egg-info
numpy
numpy-1.13.0.dist-info
scikit_learn-0.18.1.dist-info
scipy
scipy-0.19.1.dist-info
sklearn
tensorflow
tensorflow-1.1.0.dist-info
theano
Theano-0.10.0.dev1.egg-info


##UNINSTALL

####COMPLETELY REMOVE PIL/PILLOW (2.7 & 3.5):

$ sudo -H pip uninstall pillow
-> Successfully uninstalled Pillow-3.1.2
$ sudo -H pip3 uninstall pillow
-> Cannot uninstall requirement pillow, not installed

Used to find extra files: 
$ find / -name "*PIL*"

$ cd /usr/lib/python2.7/dist-packages
$ sudo rm -rf PILcompat.pth PILcompat

$ cd /usr/lib/python3/dist-packages/
$ sudo rm -rf PIL Pillow-3.1.2.egg-info

$ cd /usr/local/lib/python3.5/dist-packages/
$ sudo rm -rf PIL Pillow-4.1.1.dist-info pip-9.0.1.dist-info

$ sudo rm -rf virtualenvwrapper-4.7.2.egg-info virtualenvwrapper-4.7.2-nspkg.pth virtualenv_support virtualenvwrapper virtualenv-15.1.0.dist-info virtualenv_clone-0.2.6.egg-info virtualenv.py

-----
####COMPLETELY REMOVE PIP & PIP3:

$ sudo apt-get purge  --auto-remove python-pip
$ sudo apt-get purge  --auto-remove python3-pip

$ pip -V
pip 9.0.1 from /home/antz/.local/lib/python2.7/site-packages (python 2.7)

$ which pip
/usr/local/bin/pip
$ cd /usr/local/bin/
$ sudo rm -rf pip pip2 pip2.7

$ pip3 -V
pip 9.0.1 from /home/antz/.local/lib/python2.7/site-packages (python 2.7)

$ which pip3
/usr/local/bin/pip3
$ cd /usr/local/bin/
$ sudo rm -rf pip3 pip3.5

$ cd /home/antz/.local/lib/python2.7/site-packages
$ sudo rm -rf PIL Pillow-4.1.1.dist-info pip pip-9.0.1.dist-info

$ cd /usr/local/lib/python2.7/dist-packages
$ sudo rm -rf pip pip-9.0.1dist-info

$ cd /usr/local/lib/python3.5/dist-packages
$ sudo rm -rf pip pip-9.0.1.dist-info PIL Pillow-4.1.1.dist-info 

-----
####Remove Egg (from easy_install):


-----
####COMPLETELY REMOVE SPYDER3:

$ sudo apt-get purge --auto-remove spyder3
-OR-
$ sudo apt-get remove --auto-remove spyder3

-----
##INSTALL

####INSTALL PIP & PIP3:

$ sudo apt-get install python-pip python-dev build-essential
$ sudo apt-get install python3-pip python3-dev
$ sudo pip install --upgrade pip
$ sudo pip3 install --upgrade pip

-OR-

$ sudo easy_install pip		<- Installs to different directory (egg)
$ sudo easy_install pip3		<- Installs to different directory (egg)

-----
####INSTALL VIRTUAL ENVIRONMENT:

- SEPERATE NOTES -

-----
####INSTALL PILLOW (2.7 & 3.5):

sudo -H pip3 install pillow
-> Installed Pillow-4.1.1-cp27-cp27mu-manylinux1_x86_64.whl
sudo -H pip install pillow
-> Requirement already satisfied

$ sudo easy_install Pillow
Searching for Pillow
Best match: Pillow 4.1.1
Adding Pillow 4.1.1 to easy-install.pth file

Using /usr/local/lib/python2.7/dist-packages
Processing dependencies for Pillow
Finished processing dependencies for Pillow

$ sudo pip3 install Pillow
Requirement already satisfied: Pillow in ./.local/lib/python2.7/site-packages

-----
###INSTALL SPYDER3:



####CHECK IF PIP & PIP3 ARE STILL AVAILABLE:

$ pip freeze
$ pip3 freeze

$ which pip
$ which pip3

$ type pip
$ type pip3

$ pip -V
$ pip3 -V

--------------------
$ which pip
/usr/local/bin/pip

$ which pip3
/usr/local/bin/pip3

$ type pip3
-> pip3 is hashed (/usr/local/bin/pip3)
$ hash -r					<- Clears the cache
$ type pip3
-> pip3 is /usr/local/bin/pip3

pip -V
-> pip 9.0.1 from /home/antz/.local/lib/python2.7/site-packages (python 2.7)
pip3 -V
-> pip 9.0.1 from /usr/local/lib/python3.5/dist-packages (python 3.5)

-----
$ sudo apt-get install python3-dev python3-setuptools
$ sudo apt-get install libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev k8.5-dev
$ sudo apt-get install python3-pip
$ sudo -H pip3 install Pillow
$ sudo apt-get install imagemagick

X--> $ sudo ln -s /usr/bin/display /usr/bin/xv

-----
###Works fine using: python3

> import PIL
> print(PIL.__version__)
4.1.1

> from PIL import Image
> im = Image.open("someimage.jpg")
> im.show()

-----
###2018 versions of all:

Python 2.7.12:
	- PIL 		4.1.1
	- theano 	none
	- keras 	none
	- tensorflow 	none

Python 3.5.2
	- Spyder (iConsole )
	- Pillow 		4.1.1
	- theano	0.9.0
	- keras		2.0.5
	- tensorflow	1.2.0
	- numpy		1.13.0
	- scipy		0.19.1
	- scikit-learn	0.18.2




