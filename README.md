# neopi - Raspberry Pi/touch screen interface for sending designs to a Tajima Neo Embroidery machine

![Screenshot](https://i.imgur.com/pqBmuBV.gif) [more](https://imgur.com/a/9JRE5)

## This sends commands to a piece of machinery capable of causing injury, this works for me.  It's up to you to determine if it works for you.

Tajima NEO(TEJT-C1501c) embroidery machines are made for production environments, with reasonable mainteance, they are nearly bulletproof for home/hobby use.
Mechanically rugged, but the original interface shows it's age(wasn't cutting edge when new)
   * Floppy via undocumented pinout/connector(mini centronics)
      * you can get floppy/USB interfaces(mostly GoTek based) with this odd cable(and custom FW?) for about $140(shipped)    
      These require virtual floppy images on your USB, etc, still Sneakernet
   *  RS232 - 9 pin serial(at 9600, or 38400)  
      This interface is supported by commercial applications/design spoolers, but the protocol is undocumented

# What you need

* Tajima NEO(TEJT-1501C) or equivalent(I believe Toyota ESP9000 is the same machine)
* Raspberry Pi 3b with raspbian installed
* Touch screen that works with pygame(X), tested with Kuman/Waveshare
* Linux supported USB to (DB9) serial with support for hardware flow control + a null modem cable/adapter, tested with a prolific chipset
* Access to a lasercutter and a bit of hardware if you want a case around it

Erratic issues with the touchscreen when using tslib/SDL/pygame led me to use this in Xwindows(with no window manager)
Tslib calibration worked perfectly, but pygame mouse positioning events left a lot to be desired

License: GNU GPLv2 
Portions derived or inspired by https://code.google.com/archive/p/pyembroidery/ (mirrored on https://github.com/OSUblake/pyembroidery?)



## Files
neopi_case.dxf - CAD file suitable for laser cutting a case from 1/8 plywood
neopi.py - awfully written pygame interface for neo
neopi.cfg - config file for changing serial ports, file locations, displays, etc
samplefiles - simple samples to "test" the app





# Future goals
## Send designs to machine without control panel interaction.
If you ignore serial flow control, you can get the machine to move(in a unexpected and potentially harmful way!)
There are commercial programs that can do this, not sure what it takes.   
DIP switch setting realted to 2 way communication(DSW2#8) may be the key
