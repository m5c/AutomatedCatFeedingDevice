"""
Implementation of the Running state. The ACFD Automatically updates display_utils content
periodically,
but still allows for program abortion. If zero reached state is set to IDLE and the lid opened,
followed by Set Time state.

Author: Maximilian Schiedermeier
"""
from acfd.display_utils.display import Display
from acfd.state_machine_utils.state import State
# from acfd.state_machine_utils.state_machine import StateMachine


class StateRunning(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, state_machine, display: Display):
        self.__state_machine = state_machine
        self.__display = display

    def handle_button_one(self) -> None:
        print("RUNNING 1")

    def handle_button_two(self) -> None:
        print("RUNNING 2")

    def handle_button_three(self) -> None:
        print("RUNNING 3")

    def handle_button_four(self) -> None:
        print("RUNNING 4")
