"""
Helper module to map Digits of display on GPIO pins.
"""
from enum import Enum


class Segment(Enum):
    D1 = 1
    D2 = 2
    D3 = 3
    D4 = 4