"""
Abstract base class for all states.
Every state has its own way to handle input events. The button handler never triggers a
specific function, but uses the StateMachine's current state to resolve the desired action via
polymorphism.

Author: Maximilian Schiedermeier
"""

from abc import ABC, abstractmethod


class State(ABC):

    # def transition_execute(self, func, target_state: State) -> None:
    #     """
    #     Most state will not override this method. This is only intended for intermediate states
    #     that perform a function and then transition to next state, e.g. to ignore all imput
    #     events until a function is fully executed (IDLE).
    #     """
    #     pass
    # I think this is not needed, for every called can just set to IDLE, then call the parameter
    # function and then transition themselves.

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
