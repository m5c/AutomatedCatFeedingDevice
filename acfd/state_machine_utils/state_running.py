"""
Implementation of the Running state. The ACFD Automatically updates display_utils content periodically,
but still allows for program abortion. If zero reached state is set to IDLE and the lid opened,
followed by Set Time state.

Author: Maximilian Schiedermeier
"""

from acfd.state_machine_utils.state import State


class StateRunning(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def handle_button_one(self) -> None:
        pass

    def handle_button_two(self) -> None:
        pass

    def handle_button_three(self) -> None:
        pass

    def handle_button_four(self) -> None:
        pass
