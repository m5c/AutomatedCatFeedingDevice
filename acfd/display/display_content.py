"""
Represents a valid display content, that is to say something that can be statically displayed on
a 7 segment display with decimal dot, four digits.
Author: Maximilian Schiedermeier
"""
from display.segment_char import SegmentChar, get_alphabet

# Represents the amount of digits physically available.
amount_digits: int = 4


class DisplayContent:

    def __init__(self, string_content: str) -> None:
        """
        Constructor to create a display content entity. Pass a string and the contructor tries to
        convert it to a display_content representation.
        This entity should be placed on the thread safe queue communicating with the display entity.
        """
        self.__segment_chars = convert_to_segments_chars(string_content)
        print(self.__segment_chars)

    @property
    def segment_chars(self) -> list[SegmentChar]:
        """
        Python pseudo getter to access the actual content
        """
        return self.__segment_chars

    def get_segment_char_by_index(self, index: int) -> SegmentChar:
        """
        Similar to previous method, but returns only segment char at specific index.
        """
        return self.__segment_chars[index]


def to_segment(char: str, dotted: bool):
    """
    Converts a single character to corresponding undotted or dotted segment_char
    """
    if not len(char) == 1:
        raise Exception("Cannot convert non char to segment char.")
    if not get_alphabet().__contains__(char):
        return SegmentChar.D_UNKNOWN if dotted else SegmentChar.N_UNKNOWN
    if char in ['a', 'A']:
        return SegmentChar.D_A if dotted else SegmentChar.N_A
    if char in ['b', 'B']:
        return SegmentChar.D_B if dotted else SegmentChar.N_B
    if char in ['c', 'C']:
        return SegmentChar.D_C if dotted else SegmentChar.N_C
    if char in ['d', 'D']:
        return SegmentChar.D_D if dotted else SegmentChar.N_D
    if char in ['e', 'E']:
        return SegmentChar.D_E if dotted else SegmentChar.N_E
    if char in ['f', 'F']:
        return SegmentChar.D_F if dotted else SegmentChar.N_F
    if char in ['g', 'G']:
        return SegmentChar.D_G if dotted else SegmentChar.N_G
    if char in ['h', 'H']:
        return SegmentChar.D_H if dotted else SegmentChar.N_H
    if char in ['i', 'I']:
        return SegmentChar.D_I if dotted else SegmentChar.N_I
    if char in ['j', 'J']:
        return SegmentChar.D_J if dotted else SegmentChar.N_J
    if char in ['k', 'K']:
        return SegmentChar.D_K if dotted else SegmentChar.N_K
    if char in ['l', 'L']:
        return SegmentChar.D_L if dotted else SegmentChar.N_L
    if char in ['m', 'M']:
        return SegmentChar.D_M if dotted else SegmentChar.N_M
    if char in ['n', 'N']:
        return SegmentChar.D_N if dotted else SegmentChar.N_N
    if char in ['o', 'O']:
        return SegmentChar.D_O if dotted else SegmentChar.N_O
    if char in ['p', 'P']:
        return SegmentChar.D_P if dotted else SegmentChar.N_P
    if char in ['q', 'Q']:
        return SegmentChar.D_Q if dotted else SegmentChar.N_Q
    if char in ['r', 'R']:
        return SegmentChar.D_R if dotted else SegmentChar.N_R
    if char in ['s', 'S']:
        return SegmentChar.D_S if dotted else SegmentChar.N_S
    if char in ['t', 'T']:
        return SegmentChar.D_T if dotted else SegmentChar.N_T
    if char in ['u', 'U']:
        return SegmentChar.D_U if dotted else SegmentChar.N_U
    if char in ['v', 'V']:
        return SegmentChar.D_V if dotted else SegmentChar.N_V
    if char in ['w', 'W']:
        return SegmentChar.D_W if dotted else SegmentChar.N_W
    if char in ['x', 'X']:
        return SegmentChar.D_X if dotted else SegmentChar.N_X
    if char in ['y', 'Y']:
        return SegmentChar.D_Y if dotted else SegmentChar.N_Y
    if char in ['z', 'Z']:
        return SegmentChar.D_Z if dotted else SegmentChar.N_Z
    if char == '0':
        return SegmentChar.D_0 if dotted else SegmentChar.N_0
    if char == '1':
        return SegmentChar.D_1 if dotted else SegmentChar.N_1
    if char == '2':
        return SegmentChar.D_2 if dotted else SegmentChar.N_2
    if char == '3':
        return SegmentChar.D_3 if dotted else SegmentChar.N_3
    if char == '4':
        return SegmentChar.D_4 if dotted else SegmentChar.N_4
    if char == '5':
        return SegmentChar.D_5 if dotted else SegmentChar.N_5
    if char == '6':
        return SegmentChar.D_6 if dotted else SegmentChar.N_6
    if char == '7':
        return SegmentChar.D_7 if dotted else SegmentChar.N_7
    if char == '8':
        return SegmentChar.D_8 if dotted else SegmentChar.N_8
    if char == '9':
        return SegmentChar.D_9 if dotted else SegmentChar.N_9
    if char == ' ':
        return SegmentChar.BLANK
    if char == '.':
        return SegmentChar.DOT
    if char == '.':
        return SegmentChar.COMMA
    if char == '!':
        return SegmentChar.EXCLAMATION
    if char == '?':
        return SegmentChar.QUESTION


def convert_to_segments_chars(content: str) -> list[SegmentChar]:
    """
    Attempts to convert content of string to display to actual segment chars.
    """
    # provided content might not be long enough. We pad with balnks to be an save side
    content += (' ' * amount_digits)

    # store extracted segment chars
    segment_chars: list[SegmentChar] = []

    # actually parse content
    for digit in range(amount_digits):
        # Dotted is only possible if string is a least length 2
        # Dotted not allowed if character itself is a dot
        dotted = len(content) >= 2 and content[1] == '.' and content[0] != '.'

        # if character is not in known alphabet, replace by unknown symbol
        segment_chars.append(to_segment(content[0], dotted))

        # remove the extracted amount of chars from provided string
        if dotted:
            content = content[2:]
        else:
            content = content[1:]

    # return outcome
    return segment_chars
