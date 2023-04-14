"""
Helper module to test static 4-pack segment char display, that is to say on reception of a list
with four segments-chars those are statically displayed on the 4-digit seven segment display with
common cathode, until stopdisplay() is called or another list is provided.
@Author Maximilian Schiedermeier
"""
import queue
import time
from threading import Thread
from RPi import GPIO
from display.digit import digit_values
from display.display_content import DisplayContent
from display.segment import segment_values
from display.segment_char import SegmentChar


class Display:

    def __init__(self):
        # Set up common cathode pins and segment pins
        GPIO.setmode(GPIO.BCM)
        for segment in segment_values() + digit_values():
            GPIO.setup(segment, GPIO.OUT)

        # The display is threaded, therefore to safely communicate new content to the display we
        # use a
        # queue of length 1.
        # The display will detect when a new value has been placed, on next segment light-up
        # iteration
        # and update the content.
        self.__content_queue: queue.Queue[DisplayContent] = queue.Queue(1)

        # Set the time lights stay on, for each on digit iterations
        # to small a number: light is weak, too high a number: flickering.
        self.__light_on_time: float = 0.004

        # define what to display for test
        self.__content_queue.put(DisplayContent("____"))
        segment_light_up_thread = Thread(target=self.enable_display)
        segment_light_up_thread.start()

    def enable_display(self):

        """
        Turns on the display to light up statically whatever is placed in the queue.
        Display will continue to iterate until the queue stores a Null object. (or ctrl-C)
        """
        try:
            while True:
                # If there is a new value to display in the queue, retrieve it and display it.
                if not self.__content_queue.empty():
                    current_display_content: DisplayContent = self.__content_queue.get()
                    if current_display_content is None:
                        return

                # iterate over the GPIO pins for the individual digits
                for idx, digit in enumerate(digit_values()):
                    # activate digit i, by setting the corresponding cathode to grounded (all other
                    # remain on 1, so there is no current in the other digits)
                    GPIO.output(digit, 0)

                    # Light up only the segments in question (for current digit)
                    segment_char: SegmentChar = current_display_content.get_segment_char_by_index(
                        idx)
                    segment_char.switch_on()

                    # Keep the lights on long enough to be visible to the human eye
                    time.sleep(self.__light_on_time)

                    # Turn the light at the current position off again
                    # (turning off means, putting 1 on cathode)
                    GPIO.output(digit, 1)

                    # turn off again all the segments that were lit up
                    segment_char.switch_off()

        except KeyboardInterrupt:
            GPIO.cleanup()

    def set_content(self, display_content: DisplayContent):
        """
        Replaces the current display content. Will be adapted on next display iteration.
        :param display_content: as the content to display. Passing None turns off display.
        """
        self.__content_queue.put(display_content)
