"""
Implements a classic count-down clock that automatically notifies a subscriber on every update.
"""
import queue
from threading import Thread
from time import sleep
from acfd.clock_subscriber import ClockSubscriber


class Clock:

    def __init__(self, start_time_seconds: int, clock_subscriber: ClockSubscriber):
        """
        :param start_time_seconds: as default time to put on queue.
        :param clock_subscriber: as observer for value changes.
        """

        # We use a queue of size one for thread safe access to current time.
        self.__time_queue: queue.Queue[int] = queue.Queue(1)
        self.__time_queue.put(start_time_seconds)
        self.__running = False
        self.__clock_observer = clock_subscriber

        # initial update to subscriber
        if clock_subscriber is not None:
            clock_subscriber.update_time(start_time_seconds)

    def start_clock(self):
        """
        Creates new thread that decreases time on queue by one every second.
        """
        if self.__running:
            raise Exception(
                "Countdown Thread cannot be stared - is already running. You have to cancel it "
                "first.")

        # Mark countdown as running and start thread
        self.__running = True
        count_down_thread = Thread(target=self.__count_down)
        count_down_thread.start()

    def reset_clock(self, start_time_seconds: int) -> None:
        """
        Ends count-down thread by placing new value on queue. Thread notices change and goes to
        sleep.
        """
        print("Clock Reset: "+str(start_time_seconds))
        self.__time_queue.put(start_time_seconds)
        self.__running = False

    def __count_down(self):
        """
        The actual clock logic that is started in new thread. Decrements value in queue by one
        every second and updates subscribers, if there are any.
        Stops thread if external modification of queue is noticed. There can at most be one thread.
        """
        print("Count Down")

        # continue decrementing until 0 or value changed externally.
        zero_reached: bool = False
        external_touch: bool = False
        while not zero_reached and not external_touch:

            # Decrease value by one, notify observer
            old_value: int = self.__time_queue.get()
            new_value: int = old_value - 1
            self.__time_queue.put(new_value)
            if self.__clock_observer is not None:
                self.__clock_observer.update_time(new_value)
            print("New value: " + str(new_value))

            # Wait a second
            sleep(1)

            # Update flags
            zero_reached = (self.__time_queue.queue[0] == 0)
            external_touch = self.__time_queue.queue[0] != new_value

        # Mark thread as closed, notify subscribers that end is reached / aborted
        self.__running = False
        if external_touch:
            self.__clock_observer.aborted()
        else:
            self.__clock_observer.zero_reached()

