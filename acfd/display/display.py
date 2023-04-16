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

    def __init__(self, initial_string: str):
        # Set up common cathode pins and segment pins
        GPIO.setmode(GPIO.BCM)
        for segment in segment_values() + digit_values():
            GPIO.setup(segment, GPIO.OUT)

        # Set the time lights stay on, for each on digit iterations
        # to small a number: light is weak, too high a number: flickering.
        self.__light_on_time: float = 0.004

        # Initialize queue and turn on display light thread
        self.__content_queue: queue.Queue[DisplayContent] = queue.Queue(1)
        self.turn_on(initial_string)

    def __enable_display_thread(self):

        """
        Method for thread that turns on the display to light up statically whatever is placed in
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

    def turn_off(self):
        """
        Clears content queue, to indicate segment thread that it should stop.
        """
        if self.__content_queue.empty():
            raise Exception("Display cannot be turned off. Is not on.")

        # Clear queue
        self.__content_queue.get()

    def turn_on(self, content_str: str):
        """
        Turns on display (in extra thread). Can only be called if queue is empty (display off)
        """
        if not self.__content_queue.empty():
            raise Exception("Cannot turn on display. Is already lit up.")

        # restart segment iteration thread
        self.__content_queue.put(DisplayContent(content_str))
        segment_light_up_thread = Thread(target=self.__enable_display_thread)
        segment_light_up_thread.start()

    def update_content(self, content_str: str):
        """
        Replaces the current display content. Will be adapted on next display iteration.
        :param content_str: as the content to display as string. Passing None turns off display.
        """
        # if the queue is currently empty, request display start up first.
        if self.__content_queue.empty():
            raise Exception("Cannot update content. Display is turned off.")

        # if there is content on the queue, remove it:
        self.__content_queue.get_nowait()
        self.__content_queue.put_nowait(DisplayContent(content_str))
