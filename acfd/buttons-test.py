"""
This module modules the correct wiring of four pull down buttons.
See: https://raspberrypi.stackexchange.com/questions/141207/phantom-events-on-pull-down-button
"""
import time

from RPi import GPIO

# KEYPAD PINS
# PIN layout
button_pins: list[int] = [11, 8, 25, 9]
GPIO.setmode(GPIO.BCM)

# All buttons react to 3.3 voltage on button click (interrupt on rising edge, from low to high).
# That also means they all should be defaulted to DOWN.
# See: https://forums.raspberrypi.com/viewtopic.php?t=87292
GPIO.setup(button_pins[0], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[1], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[2], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[3], GPIO.IN, GPIO.PUD_DOWN)


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_one_pressed(channel):
    print("Button A")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_two_pressed(channel):
    print("Button B")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_three_pressed(channel):
    print("Button C")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_four_pressed(channel):
    print("Button D")


# Add keypad button handlers
GPIO.add_event_detect(button_pins[0], GPIO.RISING, callback=button_one_pressed, bouncetime=150)
GPIO.add_event_detect(button_pins[1], GPIO.RISING, callback=button_two_pressed, bouncetime=150)
GPIO.add_event_detect(button_pins[2], GPIO.RISING, callback=button_three_pressed, bouncetime=150)
GPIO.add_event_detect(button_pins[3], GPIO.RISING, callback=button_four_pressed, bouncetime=150)

# Keep program alive to wait for key events.
while True:
    time.sleep(1)
    print("", end='')
