"""
Helper module to test static 4-pack segment char display, that is to say on reception of a list
with four segments-chars those are statically displayed on the 4-digit seven segment display with
common cathode, until stopdisplay() is called or another list is provided.
@Author Maximilian Schiedermeier
"""
import queue
import time

from RPi import GPIO

from display.digit import digit_values
from display.display_content import DisplayContent
from display.segment_char import SegmentChar

# The display is threaded, therefore to safely communicate new content to the display we use a
# queue of length 1.
# The display will detect when a new value has been placed, on next segment light-up iteration
# and update the content.
q: queue.Queue[DisplayContent] = queue.Queue(1)

# Set the time lights stay on, for each on digit iterations
# to small a number: light is weak, too high a number: flickering.
light_on_time: float = 0.005


def enable_display():
    """
    Turns on the display to light up statically whatever is placed in the queue.
    """

    # MAIN CONTROL
    # TODO: terminate on specific value placed in queue.
    print('CTRL-C to terminate')
    try:
        while True:

            print("Ready for next display iteration.")

            # TODO: change queue type to be anything displayable, not just a number, so strings
            #  are supported.
            # If there is a new value to display in the queue, retrieve it and display it.
            if not q.empty():
                current_display_content: DisplayContent = q.queue[0]

            # iterate over the GPIO pins for the individual digits
            for idx, digit in enumerate(digit_values):

                # activate digit i, by setting the corresponding cathode to grounded (all other
                # remain on 1, so there is no current in the other digits)
                GPIO.output(digit, 0)

                # Light up only the segments in question (for current digit)
                current_display_content.get_segment_char_by_index(idx).switch_on()

                # Keep the lights on long enough to be visible to the human eye
                time.sleep(light_on_time)

                # Turn the light at the current position off again
                # (turning off means, putting 1 on cathode)
                GPIO.output(digit, 1)

                # turn off again all the segments that were lit up
                current_display_content.get_segment_char_by_index(idx).switch_off()

    except KeyboardInterrupt:
        GPIO.cleanup()


# define what to display for test
test_numbers: DisplayContent = DisplayContent(
    [SegmentChar.N1, SegmentChar.N2, SegmentChar.N3, SegmentChar.N4])
q.put(DisplayContent(test_numbers))
