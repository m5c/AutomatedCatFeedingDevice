"""
Helper module to map Segments of display_utils on GPIO pins. These emulate 3V3 to selectively light up
one segment of the display_utils.
"""
from enum import Enum


class Segment(Enum):
    # Zero
    A = 13
    B = 21
    C = 7
    D = 11
    E = 5
    F = 19
    G = 25
    DP = 8
    # # Zero
    # A = 8
    # B = 9
    # C = 11
    # D = 25
    # E = 16
    # F = 19
    # G = 20
    # DP = 26
    # Pico
    # A = 13
    # B = 16
    # C = 17
    # D = 18
    # E = 19
    # F = 20
    # G = 21
    # DP = 22


def segment_values() -> list[int]:
    return [s.value for s in Segment]
