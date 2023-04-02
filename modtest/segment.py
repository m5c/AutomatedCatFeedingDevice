"""
Helper module to map Segments of display on GPIO pins. These emulate 3V3 to selectively light up
one segment of the display.
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


def segment_values() -> list[int]:
    return [s.value for s in Segment]
