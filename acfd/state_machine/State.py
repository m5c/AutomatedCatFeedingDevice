"""
Abstract base class for all states.
Every state has its own way to handle input events. The button handler never triggers a
specific function, but uses the StateMachine's current state to resolve the desired action via
polymorphism.

Author: Maximilian Schiedermeier
"""

from abc import ABC, abstractmethod


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
