"""
This module display the correct wiring of four pull down buttons.
See: https://raspberrypi.stackexchange.com/questions/141207/phantom-events-on-pull-down-button
"""
from RPi import GPIO


def register_button_callbacks(hour_button_callback, action_button_callback) -> None:
    # Keyboard GPIO pins. (Requires additional GND connected wia resistor to GPIOs, and 3V3 that
    # connects to GPIOs on button press.)
    button_pins: list[int] = [10, 22, 24, 23]
    GPIO.setmode(GPIO.BCM)

    # All buttons react to 3.3 voltage on button click (interrupt on rising edge, from low to
    # high).
    # That also means they all should be defaulted to DOWN.
    # API meaning: PUD (means nothing, just Pull Up or Down). DOWN means it is connected to
    # GND via
    # resistor and defaults therefore to down, allowing rising edge detection.
    # See: https://forums.raspberrypi.com/viewtopic.php?t=87292
    GPIO.setup(button_pins[0], GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(button_pins[1], GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(button_pins[2], GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(button_pins[3], GPIO.IN, GPIO.PUD_DOWN)

    # Add keypad button handlers
    GPIO.add_event_detect(button_pins[0], GPIO.RISING, callback=hour_button_callback,
                          bouncetime=150)
    # # GPIO.add_event_detect(button_pins[1], GPIO.RISING, callback=self.button_2_pressed,
    # # bouncetime=150)
    # # GPIO.add_event_detect(button_pins[2], GPIO.RISING, callback=self.button_3_pressed,
    # # bouncetime=150)
    GPIO.add_event_detect(button_pins[3], GPIO.RISING, callback=action_button_callback,
                          bouncetime=150)

# def button_1_pressed(self, channel):
#     """
#     Define handlers for button press (channel is the GPIO that registered RISING signal)
#     """
#     self.__hour_button_callback()
