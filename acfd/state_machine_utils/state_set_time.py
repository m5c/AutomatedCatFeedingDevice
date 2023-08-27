"""
Implementation of the SetTime state. The ACFD displays the time intended for countdown,
but the automatic decrement is not yet triggered. Buttons can be used to change programmed time
or to transition to countdown state.

Author: Maximilian Schiedermeier
"""
from acfd.display_utils.display import Display
from acfd.state_machine_utils.state import State


class StateSetTime(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, display: Display):
        self.__display = display

    def handle_button_one(self) -> None:
        print("SET TIME 1")
        self.__display.update_content("0001")

    def handle_button_two(self) -> None:
        print("SET TIME 2")
        self.__display.update_content("0002")

    def handle_button_three(self) -> None:
        print("SET TIME 3")
        self.__display.update_content("0003")

    def handle_button_four(self) -> None:
        print("SET TIME 4")
        self.__display.turn_off()
