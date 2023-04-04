"""
Helper module to map Digits of display on GPIO pins. These selectively emulate GND to light up a
specific digit.
"""
from enum import Enum


class Digit(Enum):
    D1 = 2
    D2 = 3
    D3 = 4
    D4 = 14


def digit_values() -> list[int]:
    return [d.value for d in Digit]
