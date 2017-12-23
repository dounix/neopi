# neopi
Raspberry Pi/touch screen interface for sending designs to a Tajima Neo Embroidery machine

## This sends commands to a piece of machinery capable of causing injury, this works for me.  It's up to you to determine if it works for you.

Tajima NEO(TEJT-C1501c) embroidery machines are made for production environments, with reasonable mainteance, they are nearly bulletproof for home/hobby use.
Mechanically rugged, but the original interface shows it's age(wasn't cutting edge when new)
   * Floppy via undocumented pinout/connector(mini centronics)
      * you can get floppy/USB interfaces(mostly GoTek based) with this odd cable(and custom FW?) for about $140(shipped)    
      These require virtual floppy images on your USB, etc, still Sneakernet
   *  RS232 - 9 pin serial(at 9600, or 38400)  
      This interface is supported by commercial applications/design spoolers, but the protocol is undocumented

* Tajima NEO(TEJT-1501C) or equivalent(I believe Toyota ESP9000 is the same device)
* Raspberry Pi 3b with raspbian installed
* Touch screen that works with pygame(X), tested with Kuman/Waveshare

* Linux supported USB to (DB9) serial with support for hardware flow control + a null modem cable, tested with a prolific chipset

Erratic issues with the touchscreen when using tslib/SDL/pygame let me to use this in Xwindows(with no window manager)
Tslib calibration worked perfectly, but pygame mouse positioning events let a lot to be desired

