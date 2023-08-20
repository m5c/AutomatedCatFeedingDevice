"""
Implementation of the SetTime state. The ACFD displays the time intended for countdown,
but the automatic decrement is not yet triggered. Buttons can be used to change programmed time
or to transition to countdown state.

Author: Maximilian Schiedermeier
"""

from acfd.state_machine.State import State


class StateSetTime(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

# TODO: Implement...
# def handle_button_one(self) -> None:
#     pass
#
#
# def handle_button_two(self) -> None:
#     pass
#
#
# def handle_button_three(self) -> None:
#     pass
#
#
# def handle_button_four(self) -> None:
#     pass
