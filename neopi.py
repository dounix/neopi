#!/usr/bin/python
import pygame
import os
import platform
from time import sleep
import serial
import re
import struct
import configparser


def getconf():
   try:
      config = configparser.ConfigParser()
      config.read('neopi.cfg')
      return config[platform.machine()]
   except:
      print("ERROR: missing config for this platform")
      raise


config=getconf()
version="0.1"

SCREENSIZE=(480,320)
SCREENCENTER=(SCREENSIZE[0]/2,SCREENSIZE[1]/2)


class Button(object):
   def __init__(self, screen, text, posx, posy, sizex, sizey, active_color, action, textsize=35, active=True, textcolor=(255,255,255), inactive_textcolor=(255,255,255),  inactive_color=(40,40,40) ):
      self.screen=screen
      self.text=text
      self.active=active
      self.textsize=textsize
      self.textcolor=textcolor
      self.inactive_textcolor=inactive_textcolor
      self.posx=posx
      self.posy=posy
      self.sizex=sizex
      self.sizey=sizey
      self.action=action
      self.active_color=active_color
      self.inactive_color=inactive_color
      self.refresh()

   def refresh(self):
      if self.active:
         buttoncolor=self.active_color
         textcolor=self.textcolor
      else:
         buttoncolor=self.inactive_color
         textcolor = self.inactive_textcolor
      pygame.draw.rect(self.screen, buttoncolor, (self.posx, self.posy, self.sizex, self.sizey) )
      font_big = pygame.font.Font("font/Bungee/Bungee-Regular.ttf", self.textsize)
      text_surface = font_big.render(self.text, True, textcolor)
      rect = text_surface.get_rect(center=(self.posx + (self.sizex / 2), self.posy + (self.sizey / 2)))
      self.screen.blit(text_surface, rect)
      pygame.display.update()

   def activate(self):
      self.active=True
      self.refresh()
#should I call the update here
   def deactivate(self):
      self.active=False
      self.refresh()

   def touchcheck(self,pos,portstatus):
      x,y=pos
      cts,dsr=portstatus
      if self.posx + self.sizex >= x >= self.posx and self.posy + self.sizey >= y >= self.posy:
         print("on button %s" % self.text)
         self.action()

pygame.init()
if config.getboolean("fullscreen"):
   pygame.display.set_mode(SCREENSIZE,pygame.FULLSCREEN) #xwindows full sized
pygame.mouse.set_visible(config.getboolean("mousevisible"))

lcd = pygame.display.set_mode(SCREENSIZE)
lcd.fill(pygame.color.Color("black"))
pygame.display.update()

class Message(object):
   def __init__(self, screen, text, posx, posy, size=25, font="font/Bungee/Bungee-Regular.ttf", active=True,inactive_color=(0,0,0), color=(255, 255, 255) ):
      self.screen = screen
      self.text = text
      self.size = size
      self.posx = posx
      self.posy = posy
      self.color = color
      self.inactive_color = inactive_color
      self.active = active
      self.font = font
      self.refresh()

   def activate(self):
      self.active = True
      self.refresh()
         # should I call the update here

   def deactivate(self):
      self.active = False
      self.refresh()

   def setmsg(self,text):
      self.erase()
      self.text=text
      self.refresh()

   def erase(self):
      #probably dumb to render again, but don't know how else to get the size
      font_big = pygame.font.Font(self.font, self.size)
      text_surface = font_big.render(self.text, True, self.color)
      rect = text_surface.get_rect(center=(self.posx, self.posy))
      self.screen.fill((0,0,0), rect)

   def refresh(self):
      if self.active:
         color=self.color
      else:
         color=self.inactive_color
      font_big = pygame.font.Font(self.font, self.size)
      text_surface = font_big.render(self.text, True, self.color)
      rect = text_surface.get_rect(center=(self.posx,self.posy))
      self.screen.blit(text_surface, rect)
      pygame.display.update()




class Filelist(object):
   headersz=513
   def __init__(self, directory=config["stitchdir"]):
      self.headersz = 513
      self.directory = directory
      self.curpick = 0
      self.filelist = []
      self.updatefilelist()
      self.incancel = False
      self.info = {}
      self.parsefile()

   def stitchcount(self):
      filesize = os.path.getsize(self.fullpath())
      bytesleft = filesize - self.headersz
      return (bytesleft / 3)

   def fullpath(self):
      return os.path.join(self.directory, self.currentfile())

   def send(self):
      fullpath = os.path.join(self.directory, self.currentfile())
      filesize = os.path.getsize(fullpath)
      bytesleft = filesize - self.headersz
      io = open(fullpath, 'rb')
      io.seek(self.headersz) # this should get to the null after the header
      ser.write(io.read(bytesleft))
      msg["bot"].setmsg("sent")
      btn["cancel"].deactivate()
      self.updatefilelist()
      #btn["send"].deactivate() somehow this is activated without this

   def pending(self):
      msg["bot"].setmsg("send pending")
      btn["cancel"].activate()
      btn["send"].deactivate()
      while True:
         if (ser.getCTS(), ser.getDSR()) == (True,True):
            msg["bot"].setmsg("sending")
            self.send()
            break
         else:
            for event in pygame.event.get():
               if (event.type == pygame.MOUSEBUTTONDOWN):
                  btn["cancel"].touchcheck(pygame.mouse.get_pos(),portstatus)

         if self.incancel:
            self.incancel=False
            break
         sleep(.1)

   def currentfile(self):
      if len(self.filelist) > 0:
         return self.filelist[self.curpick]
      else:
         return False

   def parsefile(self):
      if len(self.filelist) > 0:
         with open(self.fullpath(), "rb") as bfile:
            bfile.seek(0)  # Go to beginning
            header = bfile.read(74)  # We only care about the common headers
            info = {}
            label, stitchct, colorct, px, nx, py, ny=struct.unpack('<3x16sx3x7sx3x3sx3x5sx3x5sx3x5sx3x5sx', header)
            info["label"] = label.decode().strip()
            info["stitchct"] = stitchct.decode().strip()
            info["colorct"] = int(colorct.decode().strip())+1
            info["px"] = px.decode().strip()
            info["nx"] = nx.decode().strip()
            info["py"] = py.decode().strip()
            info["ny"] = ny.decode().strip()
            info["x"] = (int(info["px"]) + int(info["nx"]))/10
            info["y"] = (int(info["py"]) + int(info["ny"]))/10
            self.info = info
      else:
         return False



   def up(self):
      print("doing file incr")
      if self.curpick < (len(self.filelist)-1):
         self.curpick += 1
         self.parsefile()
         print(self.curpick)

   def down(self):
      print("doing file decr")
      if self.curpick > 0:
         self.curpick -= 1
         self.parsefile()
         print(self.curpick)

   def cancel(self):
      print("Cancel returning true")
      msg["bot"].setmsg("canceled")
      self.incancel=True
      self.updatefilelist()
      btn["cancel"].deactivate()
      btn["send"].activate()

   def updatefilelist(self):
      self.filelist=[f for f in os.listdir(self.directory) if re.match(r".*\.(dst|DST)$", f)]
      print(self.filelist)

def donothing():
   print("doing nothing")


files = Filelist()

btn={}
btn["left"] = Button(lcd,"<", 0,80,70,150, pygame.color.Color("DarkOrange"),files.down )
btn["right"] = Button(lcd,">", 410,80,70,150, pygame.color.Color("DarkOrange"),files.up )
#single send button
#btn["send"] = Button(lcd,"SEND", 120,250,200,60, pygame.color.Color("ForestGreen"),files.pending )
btn["send"] = Button(lcd,"SEND", 0,250,200,60, pygame.color.Color("ForestGreen"),files.pending )
btn["cancel"] = Button(lcd,"CANCEL", 280,250,200,60, pygame.color.Color("red"),files.cancel, active=False )
btn["online"] = Button(lcd,"ONLINE", 0,0,160,40, (0,0,200), donothing, inactive_textcolor=(20,20,20),inactive_color=(0,0,14) , active=False, textsize=20)
btn["rxready"] = Button(lcd,"RECV READY", 300 ,0,180,40, (0,0,200), donothing, inactive_textcolor=(20,20,20),inactive_color=(0,0,14) , active=False, textsize=20)

msg={}
msg["top"] = Message(lcd, "NeoPi "+version,SCREENSIZE[0]/2,(SCREENSIZE[1]/2)-70, size=30 )
msg["mid1"] = Message(lcd, "                ",SCREENSIZE[0]/2,(SCREENSIZE[1]/2)-30, size=26 )
msg["mid2"] = Message(lcd, "                ",SCREENSIZE[0]/2,(SCREENSIZE[1]/2)+5, size=26 )
msg["bot"] = Message(lcd, "data: "+files.directory ,SCREENSIZE[0]/2,(SCREENSIZE[1]/2)+45, size=26 )
sleep(.1)


priorcurpick=10 #something that isn't zero
while True:
   #Scan touchscreen events
   #need to be in this loop almost all the time...unless we're waiting on an error..maybe even then..
   for event in pygame.event.get():
      if(event.type == pygame.MOUSEBUTTONDOWN):
          #have each active button object check itself the pos
          for k in btn:
             if btn[k].active:
                btn[k].touchcheck(pygame.mouse.get_pos(),portstatus)

   if priorcurpick != files.curpick and len(files.filelist) > 0:
      msg["top"].setmsg(files.currentfile())
      mid1msg=str(files.info["x"])+"mm x "+str(files.info["y"])+"mm"
      msg["mid1"].setmsg(mid1msg)
      if files.info["colorct"] > 1:
         suffix=" Colors"
      else:
         suffix=" Color"
      mid2msg = str(files.info["colorct"]) + suffix
      msg["mid2"].setmsg(mid2msg)
      msg["bot"].setmsg(files.info["stitchct"]+" Stitches")
      priorcurpick = files.curpick
   elif priorcurpick != files.curpick and len(files.filelist) == 0:
      msg["top"].setmsg("no files")

   #see if ser already exists, if not open it
   try:
      ser
   except NameError:
      try:
         print("opening ",config["serialport"])
         ser = serial.Serial(config["serialport"],38400)
         # msg["bot"].setmsg("Port Opened")
         priorportstatus=(False,False)
      except IOError:
         msg["bot"].setmsg("Port Error")
   portstatus=(ser.getCTS(),ser.getDSR())
   #only blit things to the screen if they have changed.
   if portstatus != priorportstatus:
      print("port status changed")
      btn["online"].active=ser.getCTS()
      btn["online"].refresh()
      btn["rxready"].active = ser.getDSR()
      btn["rxready"].refresh()
      priorportstatus=portstatus
      if portstatus[0] == True:
         btn["send"].activate()
         print("activating send button")
      else:
         btn["send"].deactivate()
         print("deactivating send button")

   sleep(0.1)
