"""
This abstract class substitutes what any proper object oriented language would consider an
interface. Needed for class-independent update subscription (observer pattern) to clock updates.
Author: Maximilian Schiedermeier
"""
from abc import ABC, abstractmethod


class ClockSubscriber(ABC):

    @abstractmethod
    def update_time(self, time_update: int) -> None:
        """
        Class (interface) implementation must provide logic for this abstract method.
        """
        pass

