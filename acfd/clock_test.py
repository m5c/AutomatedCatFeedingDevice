from time import sleep

from acfd.clock import Clock
from acfd.clock_subscriber import ClockSubscriber


class ClockTest:

    def __init__(self):
        print("Testing Clock")
        self.__clock: Clock = Clock([PrintingClockSubscriber()])
        self.__clock.start_clock(5, False)
        sleep(2)
        self.__clock.stop_clock()
        sleep(2)
        self.__clock.start_clock(5, True)


class PrintingClockSubscriber(ClockSubscriber):
    def notify_clock_time_change(self, time_update: int) -> None:
        print(time_update)

    def started(self) -> None:
        print("Started!")

    def notify_clock_zero_reached(self) -> None:
        print("Zero Reached!")

    def notify_clock_stopped(self) -> None:
        print("Aborted!")



ClockTest()