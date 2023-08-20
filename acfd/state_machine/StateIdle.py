"""
Implementation of the IDLE state, where the ACFD is currently performing task and the next state
transition is already programmed. However, no input events should be accepted before the current
action is completed (e.e.g opening the lid with motor, or displaying the boot message)

Author: Maximilian Schiedermeier
"""

from acfd.state_machine.State import State


class StateIdle(State):
    """
    IDLE State is selected when an action is proces sbut needs time to finish. While this state
    is active, all incoming events should be simply discarded.
    """


def handle_button_one(self) -> None:
    pass


def handle_button_two(self) -> None:
    pass


def handle_button_three(self) -> None:
    pass


def handle_button_four(self) -> None:
    pass
