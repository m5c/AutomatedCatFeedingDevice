"""
Abstract base class for all states.
States are the polymorphic way to handle button input events. The hardware button handler never
triggers a specific function, but uses the StateMachine's current state as proxy to resolve the
desired action via polymorphism.

Author: Maximilian Schiedermeier
"""

from abc import ABC, abstractmethod

from acfd.clock import Clock
from acfd.display_utils.display import Display


class State(ABC):

    @abstractmethod
    def handle_button_one(self) -> None:
        pass

    @abstractmethod
    def handle_button_two(self) -> None:
        pass

    @abstractmethod
    def handle_button_three(self) -> None:
        pass

    @abstractmethod
    def handle_button_four(self) -> None:
        pass
