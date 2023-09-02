"""
Helper module to test static 4-pack segment char display_utils, that is to say on reception of a
list
with four segments-chars those are statically displayed on the 4-digit seven segment
display_utils with
common cathode, until stopdisplay() is called or another list is provided.
@Author Maximilian Schiedermeier
"""
import queue
import time
from threading import Thread
from RPi import GPIO
from acfd.display_utils.digit import digit_values
from acfd.display_utils.display_content import DisplayContent
from acfd.display_utils.segment import segment_values


class Display:

    def __init__(self, initial_string: str):
        # Set up common cathode pins and segment pins
        GPIO.setmode(GPIO.BCM)
        for segment in segment_values() + digit_values():
            GPIO.setup(segment, GPIO.OUT)

        # Set the time lights stay on, for each on digit iterations
        # to small a number: light is weak, too high a number: flickering.
        self.__light_on_time: float = 0.004

        # Initialize queue and turn on display_utils light thread
        self.__content_queue: queue.Queue[DisplayContent] = queue.Queue(1)
        self.turn_on(initial_string)

    def __enable_display_thread(self):

        """
        Method for thread that turns on the display_utils to light up statically whatever is
        placed in
        the queue.
        This thread never removes from the queue, only peeks.
        Display will continue to iterate until the queue stores a None object.
        """
        while not self.__content_queue.empty():
            # TODO: add lock here to prevent reading on non atomic update.
            current_display_content: DisplayContent = self.__content_queue.queue[0]

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
        print("Thread ended, no more content")

    @property
    def running(self) -> bool:
        """
        Pseudo python getter (proper OO PLs would call it a getter) to look up if display_utils
        is currently switched on.
        """
        return not self.__content_queue.empty()

    def turn_off(self):
        """
        Clears content queue, to indicate segment thread that it should stop.
        """
        if self.__content_queue.empty():
            raise Exception("Display cannot be turned off. Is not on.")

        # NOTE: there seems to be an issue here!
        self.__content_queue.get()

    def turn_on(self, content_str: str):
        """
        Turns on display_utils (in extra thread). Can only be called if queue is empty (
        display_utils off)
        """
        if not self.__content_queue.empty():
            raise Exception("Cannot turn on display_utils. Is already lit up.")

        # restart segment iteration thread
        self.__content_queue.put(DisplayContent(content_str))
        segment_light_up_thread = Thread(target=self.__enable_display_thread)
        segment_light_up_thread.start()

    def update_content(self, content_str: str):
        """
        Replaces the current display_utils content. Will be adapted on next display_utils iteration.
        :param content_str: as the content to display_utils as string. Passing None turns off
        display_utils.
        """
        # if the queue is currently empty, request display_utils start up first.
        if self.__content_queue.empty():
            raise Exception("Cannot update content. Display is turned off.")

        # if there is content on the queue, remove it:
        self.__content_queue.get_nowait()
        self.__content_queue.put_nowait(DisplayContent(content_str))
