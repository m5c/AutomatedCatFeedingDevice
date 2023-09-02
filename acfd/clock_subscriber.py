"""
This abstract class substitutes what any proper object oriented language would consider an
interface. Needed for class-independent update subscription (observer pattern) to clock updates.
Author: Maximilian Schiedermeier
"""
from abc import ABC, abstractmethod


class ClockSubscriber(ABC):

    @abstractmethod
    def notify_clock_time_change(self, time_update: int) -> None:
        """
        Class (interface) implementation must provide logic for this abstract method. Method is
        invoked when the clock has an update.
        """

    @abstractmethod
    def notify_clock_zero_reached(self) -> None:
        """
        Class (interface) implementation must provide logic for this abstract method. Method is
        invoked when the clock has reached zero.
        """

    @abstractmethod
    def notify_clock_stopped(self) -> None:
        """
        Class (interface) implementation must provide logic for this abstract method. Method is
        invoked when the clock was reset / aborted.
        """

    @abstractmethod
    def notify_clock_started(self) -> None:
        """
        Class (interface) implementation must provide logic for this abstract method. Method is
        invoked when the clock started.
        """
