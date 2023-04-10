"""
This module display the correct wiring of four pull down buttons.
See: https://raspberrypi.stackexchange.com/questions/141207/phantom-events-on-pull-down-button
"""
import time

from RPi import GPIO

# keyboard GPIO pins. (Requires additional GND connected wia resistor to GPIOs, and 3V3 that
# connects to GPIOs on button press.)
button_pins: list[int] = [10, 22, 24, 23]
GPIO.setmode(GPIO.BCM)

# All buttons react to 3.3 voltage on button click (interrupt on rising edge, from low to high).
# That also means they all should be defaulted to DOWN.
# API meaning: PUD (means nothing, just Pull Up or Down). DOWN means it is connected to GND via
# resistor and defaults therefore to down, allowing rising edge detection.
# See: https://forums.raspberrypi.com/viewtopic.php?t=87292
GPIO.setup(button_pins[0], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[1], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[2], GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button_pins[3], GPIO.IN, GPIO.PUD_DOWN)


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_1_pressed(channel):
    print("Button A")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_2_pressed(channel):
    print("Button B")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_3_pressed(channel):
    print("Button C")


# Define handlers for button press (channel is the GPIO that registered RISING signal)
def button_4_pressed(channel):
    print("Button D")


def test_buttons() -> None:
    """
    Call to test the keypad
    :return:
    """
    # Add keypad button handlers
    GPIO.add_event_detect(button_pins[0], GPIO.RISING, callback=button_1_pressed, bouncetime=150)
    GPIO.add_event_detect(button_pins[1], GPIO.RISING, callback=button_2_pressed, bouncetime=150)
    GPIO.add_event_detect(button_pins[2], GPIO.RISING, callback=button_3_pressed, bouncetime=150)
    GPIO.add_event_detect(button_pins[3], GPIO.RISING, callback=button_4_pressed, bouncetime=150)

    # Keep program alive for 10 seconds to test keypad.
    for _ in range(10):
        time.sleep(1)
        print("", end='')


test_buttons()
