"""
Represents a valid display content, that is to say something that can be statically displayed on
a 7 segment display with decimal dot, four digits.
Author: Maximilian Schiedermeier
"""
from display.segment_char import SegmentChar


class DisplayContent:

    def __init__(self, segment_chars: list[SegmentChar]) -> None:
        """
        Constructor to create a display content entity. This entity should be placed on the queue
        for communication between display and acfd main logic.
        """
        self.__segment_chars = segment_chars

    # TODO: Add smarter constructor that accepts strings (and internally converts them to
    #  SegmentChar List as good as possible, e.g. using underscore for everything undefined.)

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
