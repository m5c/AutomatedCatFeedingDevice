"""
Implementation of the SetTime state. The ACFD displays the time intended for countdown,
but the automatic decrement is not yet triggered. Buttons can be used to change programmed time
or to transition to countdown state.

Author: Maximilian Schiedermeier
"""
from acfd.clock import Clock
from acfd.display_utils.display import Display
from acfd.display_utils.display_content_formatter import to_zero_padded_number
from acfd.state_machine_utils.state import State


class StateSetTime(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, state_machine: 'StateMachine', display: Display, clock: Clock):
        self.__state_machine = state_machine
        self.__display = display
        self.__clock = clock
        self.__time_hours: int = 0
        self.__time_minutes: int = 0

    def time_to_padded_string(self) -> str:
        """
        Consumes the current hours and minutes information and converts it to a padded string
        ready for display on 4 digit 7 segment component.
        """
        return to_zero_padded_number(self.__time_hours, 2) + "." + to_zero_padded_number(
            self.__time_minutes, 2)

    def time_in_seconds(self) -> int:
        """
        Converts amount of hours and minuted into the equivalent in seconds.
        """
        return 60 * 60 * self.__time_hours + 60 * self.__time_minutes

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
        # If time is 0 => shut down (this is not desired in PROD. Users will simply pull the plug
        # if they don't need the machine any more and there is no way to restart once killed.)
        # Otherwise: start clock
        if self.time_in_seconds() == 0:
            # Turning off display kills last background thread and ends program.
            # self.__display.turn_off() # IGNORE IN PROD
            pass
        else:
            self.__state_machine.change_state("RUNNING")
            self.__clock.start_clock(self.time_in_seconds(), True)
            # update own time, to start clean on next state iteration
            self.__time_hours = 0
            self.__time_minutes = 0
