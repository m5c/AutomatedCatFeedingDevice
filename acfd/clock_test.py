"""
Helper class to illustrate and test clock module.
"""

from time import sleep

from acfd.clock import Clock
from acfd.clock_subscriber import ClockSubscriber


class ClockTest:

    def __init__(self):
        # One and the same clock instance can be started and stopped multiple times.
        # Create the clock and provide a single listener to clock events. The clock is not yet
        # programmed or running.
        self.__clock: Clock = Clock([PrintingClockSubscriber()])
        # Start the countdown, will print message every second until aborted. The false flag
        # indicates that the clock should wait an initial second before decreasing.
        self.__clock.start_clock(5, False)
        sleep(2)
        # Abort the running countdown.
        self.__clock.stop_clock()
        sleep(2)
        # Reprogram the clock and recommence countdown from 5, this time with direct increment (
        # no delay before first decrement)
        self.__clock.start_clock(5, True)


class PrintingClockSubscriber(ClockSubscriber):
    """
    This is a dummy clock subscriber that does nothing but print all received clock events to
    console. Meant for testing of the Clock implementation.
    """

    def notify_clock_time_change(self, time_update: int) -> None:
        print(time_update)

    def notify_clock_started(self) -> None:
        print("Started!")

    def notify_clock_zero_reached(self) -> None:
        print("Zero Reached!")

    def notify_clock_stopped(self) -> None:
        print("Aborted!")


ClockTest()
