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
    N_A = [Segment.A, Segment.B, Segment.C, Segment.E, Segment.F, Segment.G]
    N_B = [Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    N_C = [Segment.A, Segment.D, Segment.E, Segment.F]
    N_D = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.G]
    N_E = [Segment.A, Segment.D, Segment.E, Segment.F, Segment.G]
    N_F = [Segment.A, Segment.E, Segment.F, Segment.G]
    N_G = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G]
    N_H = [Segment.B, Segment.C, Segment.E, Segment.F, Segment.G]
    N_I = [Segment.B, Segment.C]
    N_J = [Segment.B, Segment.C, Segment.D]
    N_K = [Segment.D, Segment.E, Segment.F, Segment.G]
    N_L = [Segment.D, Segment.E, Segment.F]
    N_M = [Segment.C, Segment.E, Segment.G]
    N_N = [Segment.C, Segment.E, Segment.G]
    N_O = [Segment.C, Segment.D, Segment.E, Segment.G]
    N_P = [Segment.A, Segment.B, Segment.E, Segment.F, Segment.G]
    N_Q = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G]
    N_R = [Segment.E, Segment.G]
    N_S = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G]
    N_T = [Segment.A, Segment.B, Segment.C]
    N_U = [Segment.C, Segment.D, Segment.E]
    N_V = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.F]
    N_W = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    N_X = [Segment.A, Segment.D, Segment.G]
    N_Y = [Segment.B, Segment.C, Segment.F, Segment.G]
    N_Z = [Segment.A, Segment.B, Segment.D, Segment.E]
    D_A = [Segment.A, Segment.B, Segment.C, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_B = [Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_C = [Segment.A, Segment.D, Segment.E, Segment.F, Segment.DP]
    D_D = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.G, Segment.DP]
    D_E = [Segment.A, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_F = [Segment.A, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_G = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]
    D_H = [Segment.B, Segment.C, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_I = [Segment.B, Segment.C, Segment.DP]
    D_J = [Segment.B, Segment.C, Segment.D, Segment.DP]
    D_K = [Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_L = [Segment.D, Segment.E, Segment.F, Segment.DP]
    D_M = [Segment.C, Segment.E, Segment.G, Segment.DP]
    D_N = [Segment.C, Segment.E, Segment.G, Segment.DP]
    D_O = [Segment.C, Segment.D, Segment.E, Segment.G, Segment.DP]
    D_P = [Segment.A, Segment.B, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_Q = [Segment.A, Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]
    D_R = [Segment.E, Segment.G, Segment.DP]
    D_S = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G, Segment.DP]
    D_T = [Segment.A, Segment.B, Segment.C, Segment.DP]
    D_U = [Segment.C, Segment.D, Segment.E, Segment.DP]
    D_V = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.DP]
    D_W = [Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    D_X = [Segment.A, Segment.D, Segment.G, Segment.DP]
    D_Y = [Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]
    D_Z = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.DP]
    BLANK = []
    DASH = [Segment.G]
    DOT = [Segment.DP]
    COMMA = [Segment.E]
    N_UNKNOWN = [Segment.D]
    D_UNKNOWN = [Segment.D, Segment.DP]
    N_0 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F]
    D_0 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.DP]
    N_1 = [Segment.B, Segment.C]
    D_1 = [Segment.B, Segment.C, Segment.DP]
    N_2 = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G]
    D_2 = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G, Segment.DP]
    N_3 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.G]
    D_3 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.G, Segment.DP]
    N_4 = [Segment.B, Segment.C, Segment.F, Segment.G]
    D_4 = [Segment.B, Segment.C, Segment.F, Segment.G, Segment.DP]
    N_5 = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G]
    D_5 = [Segment.A, Segment.C, Segment.D, Segment.F, Segment.G, Segment.DP]
    N_6 = [Segment.A, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    D_6 = [Segment.A, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    N_7 = [Segment.A, Segment.B, Segment.C]
    D_7 = [Segment.A, Segment.B, Segment.C, Segment.DP]
    N_8 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G]
    D_8 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.E, Segment.F, Segment.G, Segment.DP]
    N_9 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.F, Segment.G]
    D_9 = [Segment.A, Segment.B, Segment.C, Segment.D, Segment.F, Segment.G, Segment.DP]
    QUESTION = [Segment.A, Segment.B, Segment.D, Segment.E, Segment.G, Segment.DP]
    EXCLAMATION = [Segment.B, Segment.C, Segment.DP]

    def set_power(self, power: bool) -> None:
        """
        Puts current on or off for all segments of a given segment char
        """
        for segment in self.value:
            GPIO.output(segment.value, power)

    def switch_on(self) -> None:
        """
        Turns on all lights associated to a segment char.
        """
        self.set_power(True)

    def switch_off(self) -> None:
        """
        Turns on all lights associated to a segment char.
        """
        self.set_power(False)

def get_alphabet() -> str:
    return "acbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-?!,. "