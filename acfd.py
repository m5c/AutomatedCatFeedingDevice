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

GPIO.setmode(GPIO.BCM)

# Waiting time between stepper motor steps.
step_time = 0.002

# 8 SEGMENT DISPLAY PINS
#     A  B    C  D   E   F   G
seg = [15, 24, 18, 22, 23, 17, 27]
gnd = [2, 3, 4, 14]

# indicates which segments must light up for digits 0-9
digits = [[15, 24, 18, 22, 23, 17], [24, 18], [15, 24, 22, 23, 27], [15, 24, 18, 22, 27], [24, 18, 17, 27],
          [15, 18, 22, 17, 27], [18, 22, 23, 17, 27], [15, 24, 18], [15, 24, 18, 22, 23, 17, 27], [15, 24, 18, 17, 27]]

# reset dot segment output
GPIO.setup(10, GPIO.OUT, initial=0)
# reset GPIO pins for all segments to 0. (off)
for s in range(len(seg)):
    GPIO.setup(seg[s], GPIO.OUT, initial=0)
# reset GPIO pins for all digits to 1. (not selected)
for s in range(len(gnd)):
    GPIO.setup(gnd[s], GPIO.OUT, initial=1)

# STEPPER MOTOR PINS (and modes)
# ULN2003 "-" goes to +5V pin, ULN2003 "+" goes to GND pin.
# ULN2003 mappings to GPIO pins:
IN1 = 21
IN2 = 26
IN3 = 20
IN4 = 19
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
# Initialize all pins with false, to prevent random movement at program start.
GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)

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
# Hours is set to false if coundown switches from HHMM to MMSS.
hours = True
# armed flag is set to true when the countdown begins
armed = False


# Define stepper motor sequential step functions
def step_1():
    GPIO.output(IN4, True)
    sleep(step_time)
    GPIO.output(IN4, False)


def step_2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep(step_time)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)


def step_3():
    GPIO.output(IN3, True)
    sleep(step_time)
    GPIO.output(IN3, False)


def step_4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep(step_time)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)


def step_5():
    GPIO.output(IN2, True)
    sleep(step_time)
    GPIO.output(IN2, False)


def step_6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep(step_time)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)


def step_7():
    GPIO.output(IN1, True)
    sleep(step_time)
    GPIO.output(IN1, False)


def step_8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep(step_time)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)


# Rotate counter-clockwise
def left(step):
    for i in range(step):
        step_1()
        step_2()
        step_3()
        step_4()
        step_5()
        step_6()
        step_7()
        step_8()


# Rotate clock-wise
def right(step):
    for i in range(step):
        step_8()
        step_7()
        step_6()
        step_5()
        step_4()
        step_3()
        step_2()
        step_1()


# custom function to open lid (perfect angle)
def open_lid():
    right(170)


# custom function to close lid (perfect angle)
def close_lid():
    left(170)

def decr_counter(counter):
    if counter == 0:
        return counter
    counter = counter-1
    first_two_digits = counter // 100
    last_two_digits = counter % 100
    if last_two_digits > 60:
      last_two_digits = 59
    return first_two_digits*100 + last_two_digits


# Continuous countdown thread. (Updates global remaining time variable via queue)
def thread_countdown():
    global armed
    global hours
    counter = q.queue[0]

    while counter > 0 and armed:
        
        # Current value remains displayed (by display function) and will stay on display until q is filled with updated value
        counter = q.queue[0]
        print(counter)

        # decrement second wise if in either on verge to seconds or in seconds mode.
        if (hours == True and counter == 100):
            # flip hours tag and manually override counter by 59:59
            sleep(1)
            counter = 5959
            hours = False
        elif hours == False:
            sleep(1)
            counter = decr_counter(counter)
        # decrement minute wise in every other case
        else:
            sleep(60)
            counter = decr_counter(counter)
            
        # when wait time is overi (and machine was not unarmed inbetween), update counter value on display and enter next iteration 
        if armed:
            q.get()
            q.put(counter)


    # Lid is perfectly balanced when open, we retract the whisker again right away, so the machine leaves in the same
    # state it left off.
    if armed:
        q.put(0)
        open_lid()
        close_lid()
        # Set armed to False, allow for next countdown iteration
        armed = False
        hours = True


# call to run countdown. provided counter value is interpreted as hhmm value.
def enable_display():
    # MAIN CONTROL
    print('CTRL-C to terminate')
    global armed
    try:
        while True:

            # update counter if changed
            if not q.empty():
                counter = q.queue[0]

            # i is the digit iterator
            for i in range(len(gnd)):

                # activate digit i
                GPIO.output(gnd[i], 0)

                # compute what to display on that digit
                digit = counter // pow(10, 3 - i) % 10

                # Light up all segments that correspond to number "i" 
                for segment in range(len(digits[digit])):
                    GPIO.output(digits[digit][segment], 1)

                # Light up dot separator if current digit is second position
                if i == 1:
                    GPIO.output(10, 1)

                # Light up dot separator if current digit is 4th position and ACFD is armed
                if i == 3 and armed:
                    GPIO.output(10, 1)

                # Keep the lights on long enough to be visible to the human eye
                time.sleep(0.005)

                # switch digit off again
                GPIO.output(gnd[i], 1)

                # Switch dot separator off again
                GPIO.output(10, 0)

                # reset all segments that were lit up
                for segment in range(len(digits[digit])):
                    GPIO.output(digits[digit][segment], 0)

    except KeyboardInterrupt:
        GPIO.cleanup()


# Helper function to start countdown in extra thread.
def countdown():
    global armed
    global hours
    counter = q.queue[0]

    # only start countdown if not yet running and a time was set
    if not armed and counter > 0:
        armed = True
        
        # Convert timer to minutes / seconds if HH is 0
        counter = q.get()
        if counter < 100:
            hours = False
            counter = counter * 100
        q.put(counter)

        # Start auto counter decrease in extra thread
        t = threading.Thread(target=thread_countdown)
        t.start()


# Def handler to be called on ctrl-C event
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


# Define handler for button press (channel is the GPIO that registered RISING signal)
def button_pressed_callback(channel):
    global armed
    # only allow timer changes if not armed
    if channel == button1:
        if not armed:
            counter = q.get()
            print("From " + str(counter))
            counter = ((counter + 100) % 2400)
            q.put(counter)
            print("To " + str(counter))
    if channel == button2:
        if not armed:
            counter = q.get()
            print("From " + str(counter))
            h = counter // 100 * 100
            m = counter % 100
            counter = (h + ((m + 15) % 60))
            q.put(counter)
            print("To " + str(counter))
    if channel == button3:
        if not armed:
            counter = q.get()
            print("From " + str(counter))
            h = counter // 100 * 100
            m = counter % 100
            counter = (h + ((m + 1) % 60))
            q.put(counter)
            print("To " + str(counter))
    if channel == button4:
        # if armed: reset. Otherwise start.
        if armed:
            print("Unarming")
            q.get()
            q.put(0)
            armed = False
            global hours
            hours = True
        else:
            countdown()


# Add keypad button handlers
GPIO.add_event_detect(button1, GPIO.RISING, callback=button_pressed_callback, bouncetime=300)
GPIO.add_event_detect(button2, GPIO.RISING, callback=button_pressed_callback, bouncetime=300)
GPIO.add_event_detect(button3, GPIO.RISING, callback=button_pressed_callback, bouncetime=300)
GPIO.add_event_detect(button4, GPIO.RISING, callback=button_pressed_callback, bouncetime=300)

# actual main thread starts here
# close_lid()
q.put(0)
enable_display()
