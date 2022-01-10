#!/usr/bin/python
# TODO: implement using hardware interrupts
import RPi.GPIO as GPIO
import time, datetime


# PIN layout
keypadPower=7
taster1=9
taster2=25
taster3=8
taster4=11

# Set PIN IO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(keypadPower, GPIO.OUT)
GPIO.setup(taster1, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster3, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster4, GPIO.IN, GPIO.PUD_DOWN)

# Power up 3.3V input oin
GPIO.output(keypadPower, 1)

noTouch=True

while True:
  if GPIO.input(taster1):
      if noTouch:
        print('1')
        noTouch=False
  elif GPIO.input(taster2):
      if noTouch:
        print('2')
        noTouch=False
  elif GPIO.input(taster3):
      if noTouch:
        print('3')
        noTouch=False
  elif GPIO.input(taster4):
      if noTouch:
        print('4')
        noTouch=False
  else:
    noTouch=True

GPIO.cleanup()
