# Joystickppm
Convert input signal of 2 USB Logitech Attack 3 Joysticks to a PPM signal output

First of all, some credits to Howchoo for the Powerbutton Python programming!
Disclaimer: use, edit and build of this setup is at
your own risk!

Hardware:
Raspberry Pi 3 B+ + Powersupply (Optional with powerbank for offgrid
functioning)
8GB Sandisk SD
2x Joystick Logitech Attack 3 USB
Radiomaster TX16S

Installation steps:

Write Raspberry Buster Image to SD. 

Write wpa_supplicant.conf and an empty SSH file to /boot/ 

Write PPM.py and joystickclass.py to /home/pi 

Login and write in the commandline:

sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoclean -y && sudo apt-get autoremove -y

sudo apt-get install python3-evdev 

sudo apt-get install python3-pigpio 

sudo apt-get install pigpiod 

sudo systemctl enable pigpiod 

sudo apt-get install python3-pip 

sudo pip3 install evdev 

#if the evdev version isn’t one of the latest: 

sudo pip3 install "evdev == 1.5.0"

#Insert to /etc/rc.local BEFORE THE LINE exit 0:

#pigpiod #only if “sudo systemctl enable pigpiod” doesn’t work
cd ~pi/

sudo python3 joystickclass.py &

cd -

Wiring:
5V → Raspberry Pi

Raspberry PPM output GPIO 18 + Ground (pin 12+14) → headphone jack → transmitter

trainer port DSC

Pi powerbutton (Optional)

sudo apt-get install git

git clone https://github.com/Howchoo/pi-power-button.git

./pi-power-button/script/install

Uninstall powerbutton

./pi-power-button/script/uninstall

Wiring:
GPIO 3 + Ground (pin 5+6)
use "normally open momentary push button"
