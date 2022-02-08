#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import queue
import random
import signal
import sys
import threading
import time
from time import sleep
from display import *
from motor import open_lid, close_lid

GPIO.setmode(GPIO.BCM)


# KEYPAD PINS
# PIN layout
keypadPowerPin = 7
button1 = 11
button2 = 8
button3 = 25
button4 = 9
GPIO.setup(keypadPowerPin, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button3, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button4, GPIO.IN, GPIO.PUD_DOWN)
# Power up 3.3V input pin
GPIO.output(keypadPowerPin, 1)

# global variables for inter-thread communication
# current counter value - stored in a queue, so it can be conveniently accessed from threads
# Only one value is stored in here at a time.
q = queue.Queue()
# Hours is set to false if countdown switches from HHMM to MMSS.
hours = False
armed = False


# Continuous countdown thread. (Updates global remaining time variable via queue)
def thread_countdown():
    counter = q.queue[0]
    print("Thread started.")
    while counter >= 0:
        print(counter)
        q.get()
        q.put(counter)

        # in hour mode, hour counter
        global hours
        if hours:
            # second counter only goes up to 59.
            # leave minutes, apply mod 60 on seconds
            counter = counter - 1
            hour = counter // 100
            minute = (counter % 100)
            if minute > 60:
                minute = 59
            counter = hour * 100 + minute
            time.sleep(60)
            if counter == 100:
                q.put(counter)
                time.sleep(1)
                counter = 5959
                hours = False
        else:
            # second counter only goes up to 59.
            # leave minutes, apply mod 60 on seconds
            counter = counter - 1
            minute = counter // 100
            second = (counter % 100)
            if second > 60:
                second = 59
            counter = minute * 100 + second
            time.sleep(1)

    print("Thread finished.")
    open_lid()


# Helper function to start countdown in extra thread.
def countdown():
    global armed
    if not armed:
        armed = True
        # COUNT DOWN THREAD (MUST NOT BLOCK)
        # starts with 1h 1 minute
        t = threading.Thread(target=thread_countdown)
        t.start()


# Def handler to be called on ctrl-C event
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


# Define handler for button press (channel is the GPIO that registered RISING signal)
def button_pressed_callback(channel):
    if channel == button1:
        q.put(q.get() + 100)
    if channel == button2:
        q.put(q.get() + 15)
    if channel == button3:
        print("3")
    if channel == button4:
        print("4")
        countdown()


# Add keypad button handlers
GPIO.add_event_detect(button1, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(button2, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(button3, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(button4, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)

# actual main thread starts here
# close_lid()
q.put(0)
enable_display(q)
