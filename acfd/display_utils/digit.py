"""
Helper module to map Digits of display_utils on GPIO pins. These selectively emulate GND to light up a
specific digit, by enabling a specific common cathode, one at a time.
Author: Maximilian Schiedermeier
"""
from enum import Enum


class Digit(Enum):
    # Zero
    D1 = 15
    D2 = 18
    D3 = 17
    D4 = 27
    # Pico
    # D1 = 1
    # D2 = 2
    # D3 = 3
    # D4 = 4

def digit_values() -> list[int]:
    return [d.value for d in Digit]
