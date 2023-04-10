"""
Represents a valid display content, that is to say something that can be statically displayed on
a 7 segment display with decimal dot, four digits.
Author: Maximilian Schiedermeier
"""
from display.segment_char import SegmentChar


class DisplayContent:

    # Represents the amount of digits physically available.
    amount_digits: int = 4

    def __init__(self, string_content: str) -> None:
        """
        Constructor to create a display content entity. Pass a string and the contructor tries to
        convert it to a display_content representation.
        This entity should be placed on the thread safe queue communicating with the display entity.
        """
        self.__segment_chars = convert_to_segments_chars(string_content)

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

def convert_to_segments_chars(content: str) -> list[SegmentChar]:
    """
    Attempts to convert content of string to display to actual segment chars.
    """
    # Make as manu iterations from the start as there are
    return [SegmentChar.N_UNKNOWN, SegmentChar.N_UNKNOWN, SegmentChar.N_UNKNOWN,
                                SegmentChar.N_UNKNOWN]