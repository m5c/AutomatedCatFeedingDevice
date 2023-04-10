"""
Helper module to define segments to light up for a given character (or number).
Author: Maximilian Schiedermeier"""
from enum import Enum

from RPi import GPIO

from display.segment import Segment


class SegmentChar(Enum):
    """
    Defines the segments to light up on a 7-segment display with decimal dot to display a desired
    character or number.
    Prefix indicated if "N"ot dotted, or "D"otted.
    """
    N1 = [Segment.B, Segment.C]
    D1 = [Segment.B, Segment.C, Segment.DP]
    N2 = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G]
    D2 = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G, Segment.DP]
    N3 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.G]
    D3 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.G, Segment.DP]
    N4 = [Segment.B, Segment.C, Segment.F, Segment.G]
    D4 = [Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]
    N5 = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G]
    D5 = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G, Segment.DP]
    N6 = [Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    D6 = [Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    N7 = [Segment.A, Segment.B, Segment.C]
    D7 = [Segment.A, Segment.B, Segment.C, Segment.DP]
    N8 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    D8 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    N9 = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G]
    D9 = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]

    def set_power(self, power: bool) -> None:
        """
        Puts current on or off for all segments of a given segment char
        """
        print("yay")
        for segment in self.value:
            GPIO.output(segment.value, power)

    def switch_on(self) -> None:
        """
        Turns on all lights associated to a segment char.
        """
        self.set_power(True)

    def switch_on(self) -> None:
        """
        Turns on all lights associated to a segment char.
        """
        self.set_power(False)


