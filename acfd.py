#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading, queue
import signal
import sys
from time import sleep
import os
import random

GPIO.setmode(GPIO.BCM)

## STEPPER MOTOR PINS
# Verwendete Pins des ULN2003A auf die Pins des Rapberry Pi
# zugeordnet 
IN1=21 # IN1
IN2=26 # IN2
IN3=20 # IN3
IN4=19 # IN4
# - goes to +5V, + goes to GND

# Wartezeit regelt die Geschwindigkeit wie schnell sich der Motor
# dreht.
steptime = 0.002

# Pins aus Ausgänge definieren
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
# Alle Pins werden initial auf False gesetzt. So dreht sich der 
# Stepper-Motor nicht sofort irgendwie.
GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)
GPIO.setmode(GPIO.BCM)

## KEYPAD
# PIN layout
keypadPower=7
taster4=9
taster3=25
taster2=8
taster1=11

# Set PIN IO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(keypadPower, GPIO.OUT)
GPIO.setup(taster1, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster2, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster3, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(taster4, GPIO.IN, GPIO.PUD_DOWN)

# Power up 3.3V input oin
GPIO.output(keypadPower, 1)

## global variables
# current counter value - stored in a queue, so it can be conveniently accessed from threads
# Only one value is stored in here at a time.
q = queue.Queue()
# Hours is set to false if coundown switches from HHMM to MMSS.
hours = False
#hours = True
armed = False

# Der Schrittmotoren 28BYJ-48 ist so aufgebaut, das der Motor im
# Inneren 8 Schritte für eine Umdrehung benötigt. Durch die Betriebe
# benätigt es aber 512 x 8 Schritte damit die Achse sich einmal um
# sich selbt also 360° dreht.

# Definition der Schritte 1 - 8 über die Pins IN1 bis IN4
# Zwischen jeder Bewegung des Motors wird kurz gewartet damit der
# Motoranker seine Position erreicht.
def Step1():
    GPIO.output(IN4, True)
    sleep (steptime)
    GPIO.output(IN4, False)

def Step2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep (steptime)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)

def Step3():
    GPIO.output(IN3, True)
    sleep (steptime)
    GPIO.output(IN3, False)

def Step4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep (steptime)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)

def Step5():
    GPIO.output(IN2, True)
    sleep (steptime)
    GPIO.output(IN2, False)

def Step6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep (steptime)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)

def Step7():
    GPIO.output(IN1, True)
    sleep (steptime)
    GPIO.output(IN1, False)

def Step8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep (steptime)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)

# Umdrehung links herum  
def left(step):	
	for i in range (step):   
		#os.system('clear') # verlangsamt die Bewegung des Motors zu sehr. 
		Step1()
		Step2()
		Step3()
		Step4()
		Step5()
		Step6()
		Step7()
		Step8()  
		print("Step left: ",i)

# Umdrehung rechts herum		
def right(step):
	for i in range (step):
		#os.system('clear') # verlangsamt die Bewegung des Motors zu sehr.  
		Step8()
		Step7()
		Step6()
		Step5()
		Step4()
		Step3()
		Step2()
		Step1()  
		print("Step right: ",i)

def openlid():
    right(170)

def closelid():
    left(170)

## HELPER THREAD FUNCTION FOR COUNTDOWN
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
    openlid()

#     A  B    C  D   E   F   G
seg=[15, 24, 18, 22, 23, 17, 27]
gnd=[2, 3, 4, 14]

# indicates which segments must light up for digits 0-9
digits=[[15, 24, 18, 22, 23, 17], [24, 18], [15, 24, 22, 23, 27], [15, 24, 18, 22, 27], [24, 18, 17, 27], [15, 18, 22, 17, 27], [18, 22, 23, 17, 27], [15, 24, 18], [15, 24, 18, 22, 23, 17, 27], [15, 24, 18, 17, 27]]

## INIT
# reset dot segement output
GPIO.setup(10, GPIO.OUT, initial=0)

# reset GPIO pins for all segments to 0. (off)
for s in range(len(seg)):
    GPIO.setup(seg[s], GPIO.OUT, initial=0)

# reset GPIO pins for all digits to 1. (not selected)
for s in range(len(gnd)):
    GPIO.setup(gnd[s], GPIO.OUT, initial=1)
    
# call to run countdown. provided counter value is interpreted as hhmm value.
def displaytime():

    ## MAIN CONTROL
    print('CTRL-C to terminate')
    try:
        while (True):

            # update counter if changed
            if not q.empty():
                counter = q.queue[0]

            # i is the digit iterator
            for i in range(len(gnd)):

                # activate digit i
                GPIO.output(gnd[i], 0)

                # compute what to display on that digit
                digit = counter // pow(10, 3-i) % 10

                # Light up all segments that correspond to number "i" 
                for seg in range(len(digits[digit])):
                    GPIO.output(digits[digit][seg], 1)

                # Light up dot separator if curret digit is second position
                if i == 1:
                    GPIO.output(10, 1)
                    
                time.sleep(0.005)
                
                # switch digit off again
                GPIO.output(gnd[i], 1)

                # Switch dot separator off again
                GPIO.output(10, 0)

                # reset all segments that were lit up
                for seg in range(len(digits[digit])):
                    GPIO.output(digits[digit][seg], 0)

    except KeyboardInterrupt:
        GPIO.cleanup()

# Helper function to start countdown in extra thread.
def countdown():
    global armed
    if not armed:
        armed = True
        ## COUNT DOWN THREAD (MUST NOT BLOCK)
        # starts with 1h 1 minute
        t = threading.Thread(target=thread_countdown)
        t.start()

# Def handler to be called on ctrl-C event
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

# Define handler for button press (channel is the GPIO that registered RISING signal)
def button_pressed_callback(channel):
    if channel==taster1:
        q.put(q.get()+100)
    if channel==taster2:
        q.put(q.get()+15)
    if channel==taster3:
        print("3")
    if channel==taster4:
        print("4")
        countdown()

# Add keypad button handlers
GPIO.add_event_detect(taster1, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(taster2, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(taster3, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)
GPIO.add_event_detect(taster4, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)

closelid()
q.put(0)
displaytime()


