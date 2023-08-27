"""
Helper module to map Segments of display_utils on GPIO pins. These emulate 3V3 to selectively light up
one segment of the display_utils.
"""
from enum import Enum


class Segment(Enum):
    # Zero
    A = 9
    B = 16
    C = 20
    D = 8
    E = 25
    F = 11
    G = 26
    DP = 19
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
