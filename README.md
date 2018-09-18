# neopi - Raspberry Pi/touch screen interface for sending designs to a Tajima Neo Embroidery machine

### License: GNU GPLv2 
Portions derived or inspired by https://code.google.com/archive/p/pyembroidery/ (mirrored on https://github.com/OSUblake/pyembroidery?)

![Screenshot](https://i.imgur.com/pqBmuBV.gif)  
[more](https://imgur.com/a/9JRE5)

## This sends commands to a piece of machinery capable of causing injury, this works for me.  It's up to you to determine if it works for you.

Tajima NEO(TEJT-C1501c) embroidery machines are made for production environments, they are **nearly** bulletproof for home/hobby use.
Mechanically rugged, but the original interface shows it's age..
   * Floppy via undocumented pinout/connector(mini centronics)
      * want sneakernet, but USB, a tajima speciifc gotek virtual floppy drive is $140(shipped)    
      These require virtual floppy images on your USB, etc, still Sneakernet
   *  RS232 - 9 pin serial(at 9600, or 38400)  
      This interface is supported by commercial applications/design spoolers, but the protocol is undocumented

# What you need

* Tajima NEO(TEJT-1501C) or equivalent(I believe Toyota ESP9000 is the same machine)
* Raspberry Pi 3b with raspbian distro installed
* Touch screen that works with pygame(X windows), tested with 3.5"(480x320) Kuman/Waveshare, (https://www.amazon.com/gp/product/B01CNJVG8K/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)[amazon] 
* Linux supported USB to (DB9) serial with support for hardware flow control + a null modem cable/adapter, tested with a prolific chipset
* Access to a lasercutter and a bit of hardware(if you want a case around it)

Erratic issues with the touchscreen when using tslib/SDL/pygame led me to use this in Xwindows(with no window manager)
Tslib calibration worked perfectly, but pygame mouse positioning events left a lot to be desired


## Files
neopi_case.dxf - CAD file suitable for laser cutting a case from 1/8 plywood
neopi.py - awfully written pygame interface for neo
neopi.cfg - config file for changing serial ports, file locations, displays, etc
samplefiles - simple samples to "test" the app


## Setup
### Install software
```
apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev  xinput-calibrator build-deb python-pygame
```

### Copy configs from this repo to X directories
```
cp 40-libinput.conf /usr/share/X11/xorg.conf.d/.
cp 99-calibration.conf  /etc/X11/xorg.conf.d/.
```

### Install LCD overlay
```
echo "installing LCD config tool from https://github.com/goodtft/LCD-show"
git clone https://github.com/goodtft/LCD-show
cd LCD-show
chmod 755 LCD35-show ; ./LCD35-show
```

#edit the /boot/config update the overlay to rotate the display
dtoverlay=tft35a,rotate=270 

### Reboot

### calibrate the display
```
export TSLIB_TSDEVICE=/dev/input/event0
export TSLIB_FBDEVICE=/dev/fb1
ts_calibrate
```

### Follow calibration prompts, this will update /etc/pointercal, **your values will vary**
```
8478 111 -2023240 -40 -5537 22244074 65536
```

### clone/configure 
clone this repo  
edit neopi.cfg to suit, minimum change the directory where designs are stored  
copy/mount DST/dst files to the defined directory  
start neopi.py  
choose a file to send, it will show pending..  
select input from PC on NEO control panel, it will be sent to the serial port


# TODO
## Send designs to machine without control panel interaction.
If you ignore serial flow control, you can get the machine to move(in a unexpected and potentially harmful way!)
There are commercial programs that can do this, not sure what it takes.   
DIP switch setting realted to 2 way communication(DSW2#8) may be the key
## Scrap the whole idea and extend octoprint to support embroidery.


