"""
Implements a classic count-down clock that automatically notifies a subscriber on every update.
Author: Maximilian Schiedermeier
"""
import queue
from threading import Thread
from time import sleep
from acfd.clock_subscriber import ClockSubscriber


class Clock:

    def __init__(self, clock_subscribers: list[ClockSubscriber]):
        """
        :param start_time_seconds: as default time to put on queue.
        :param clock_subscriber: as observer for value changes.
        """

        # We use a queue of size one for thread safe access to current time.
        # The queue is initialized with a dummy value (-1)
        self.__time_queue: queue.Queue[int] = queue.Queue(1)
        self.__time_queue.put(-1)
        self.__running = False
        self.__clock_subscribers: list[ClockSubscriber] = clock_subscribers

    def start_clock(self, initial_time_seconds: int, direct_decrement: bool) -> None:
        """
        Creates new thread that decreases time on queue by one every second.
        :param: initial_time_seconds as the clock time in seconds
        :direct_decrement: as flag to indicate whether the clock decrements without initial delay
        :return: None
        """
        if self.__running:
            raise Exception(
                "Countdown cannot be started - is already running. You have to cancel it first")

        if initial_time_seconds < 2:
            raise Exception("Initial time must be at least 2 seconds.")

        # Initialize queue, notify observers
        self.__time_queue: queue.Queue[int] = queue.Queue(1)
        initial_delay: int = 0 if direct_decrement else 1
        self.__time_queue.put(initial_time_seconds + initial_delay)

        # Mark clock as running, start automatic countdown (extra thread)
        self.__running = True
        count_down_thread = Thread(target=self.__count_down)
        count_down_thread.start()

    def stop_clock(self) -> None:
        """
        Ends count-down thread by placing new value on queue. Thread notices change and goes to
        sleep. Clock cannot be reused.
        """
        # By placing the dummy value on the queue, the count-down thread is notified to stop.
        # Note that the thread itself sets running flag to false when going to sleep. Having the
        # flag updated by the thread is a design choice, to avoid raise conditions.
        self.__time_queue.get()
        self.__time_queue.put(-1)

        # Notify observers that clock is stopped
        for subscriber in self.__clock_subscribers:
            subscriber.notify_clock_stopped()

    def __count_down(self):
        """
        This function must be started as background threat. It accesses this classes queue and in
        a loop decrements until zero reached or the dummy value (-1) was manually placed on
        queue, to signal interrupt.
        """

        # Initialize end criteria flags.
        zero_reached = False
        stop_requested = False

        # Keep going until value in queue is different from last placed value, or 0 reached.
        while not zero_reached and not stop_requested:

            # Pop from queue, decrease, put again.
            old_value = self.__time_queue.get()
            new_value: int = old_value - 1
            self.__time_queue.put(new_value)

            # Notify all observers about time change
            for observer in self.__clock_subscribers:
                observer.notify_clock_time_change(new_value)

            # First sleep, then update flags (to avoid missing interactions during sleep)
            # Placing negative values manually on queue is interpreted as external stop.
            sleep(1)
            zero_reached = (self.__time_queue.queue[0] == 1)
            stop_requested = (self.__time_queue.queue[0] < 0)

        # Mark thread as closed and notify observers
        self.__running = False
        if zero_reached:
            for observer in self.__clock_subscribers:
                observer.notify_clock_zero_reached()
        # No need to notify about abort, this is immediately handled by clock class in stop method.
