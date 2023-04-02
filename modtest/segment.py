"""
Helper module to map Segments of display on GPIO pins.
"""
from enum import Enum


class Segment(Enum):
    A = 15
    B = 24
    C = 18
    D = 22
    E = 23
    F = 17
    G = 27
    DP = 10