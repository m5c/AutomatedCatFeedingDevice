"""
This tester module lights up all individual segments of the four digit segment display with
common cathode. Run it to test wiring and board integrity.
Author: Maximilian Schiedermeier.
"""
import time
from RPi import GPIO
from modules.digit import digit_values
from modules.segment import segment_values

# At program start we reset all outputs
GPIO.setmode(GPIO.BCM)


def segment_test() -> None:
    """
    Powers up all segments for a fraction of a segment, one at a time.
    :return: None
    """
    # Reset PINS
    # Segments default to 0, Digits (common cathode) default to 1
    for segment in segment_values():
        GPIO.setup(segment, GPIO.OUT, initial=0)
    for digit in digit_values():
        GPIO.setup(digit, GPIO.OUT, initial=1)

    # Run the actual segment test:
    # iterate over the four digits
    for digit in digit_values():

        # activate digit i
        GPIO.output(digit, 0)

        # iterate over all segment, including the "dot"
        # Light up all segments that correspond to number "i"
        for segment in segment_values():
            # light current segment on current digit up for 200ms, then continue
            GPIO.output(segment, 1)
            time.sleep(0.1)

            # then reset segment again
            GPIO.output(segment, 0)

        # When all segments of current digit are tested, proceed to next digit (disable current)
        GPIO.output(digit, 1)


# At program end, reset all pins
segment_test()
GPIO.cleanup()
