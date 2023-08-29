"""
Implementation of the Running state. The ACFD Automatically updates display_utils content
periodically,
but still allows for program abortion. If zero reached state is set to IDLE and the lid opened,
followed by Set Time state.

Author: Maximilian Schiedermeier
"""
from time import sleep

from acfd.clock import Clock
from acfd.display_utils.display import Display
from acfd.state_machine_utils.state import State


class StateRunning(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, state_machine: 'StateMachine', display: Display, clock: Clock):
        self.__state_machine = state_machine
        self.__display = display

    def handle_button_one(self) -> None:
        print("RUNNING 1")
        # Ignore, manual time changes are not allowed while running

    def handle_button_two(self) -> None:
        print("RUNNING 2")
        # Ignore, manual time changes are not allowed while running

    def handle_button_three(self) -> None:
        print("RUNNING 3")
        # Ignore, manual time changes are not allowed while running

    def handle_button_four(self) -> None:
        print("RUNNING 4")
        # Cancel program, turn off.
        self.__display.turn_off()
