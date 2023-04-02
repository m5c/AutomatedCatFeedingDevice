"""
Helper module to define segments to light up for a given character (or number).
Author: Maximilian Schiedermeier"""
from enum import Enum


class SegmentChar(Enum):
    """
    Defines the segments to light up on a 7-segment display with decimal dot to display a desired
    character or number.
    Prefix indicated if "N"ot dotted, or "D"otted.
    """

    N1 =
