"""
Implementation of the SetTime state. The ACFD displays the time intended for countdown,
but the automatic decrement is not yet triggered. Buttons can be used to change programmed time
or to transition to countdown state.

Author: Maximilian Schiedermeier
"""
from acfd.display_utils.display import Display
from acfd.display_utils.display_content_formatter import to_zero_padded_number
from acfd.state_machine_utils.state import State


class StateSetTime(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, display: Display):
        self.__time_hours: int = 0
        self.__time_minutes: int = 0
        self.__display = display

    def time_to_padded_string(self) -> str:
        """
        Consumes the current hours and minutes information and converts it to a padded string
        ready for display on 4 digit 7 segment component.
        """
        return to_zero_padded_number(self.__time_hours, 2) + to_zero_padded_number(
            self.__time_minutes, 2)

    def handle_button_one(self) -> None:
        print("SET TIME 1")
        self.__time_hours = (self.__time_hours + 1) % 24
        self.__display.update_content(self.time_to_padded_string())

    def handle_button_two(self) -> None:
        print("SET TIME 2")
        self.__time_minutes = (self.__time_minutes + 15) % 60
        self.__display.update_content(self.time_to_padded_string())

    def handle_button_three(self) -> None:
        print("SET TIME 3")
        self.__time_minutes = (self.__time_minutes + 1) % 60
        self.__display.update_content(self.time_to_padded_string())

    def handle_button_four(self) -> None:
        print("SET TIME 4")
        # TODO: transition to state running.
        self.__display.turn_off()
