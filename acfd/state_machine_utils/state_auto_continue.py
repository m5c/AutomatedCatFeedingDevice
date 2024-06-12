"""
Implementation of the Auto continue state. The ACFD ignores all button presses and right forwards
to countdown / running state.

Author: Maximilian Schiedermeier
"""
from acfd.acfd_clock_subscriber import AcfdClockSubscriber
from acfd.clock import Clock
from acfd.display_utils.display import Display
from acfd.display_utils.display_content_formatter import to_zero_padded_number
from acfd.state_machine_utils.state import State


class StateAutoContinue(State):
    """
    Buttons 1/2/3 trigger change of currently displayed time. Button for triggers transition to
    count-down state.
    """

    def __init__(self, state_machine: 'StateMachine', display: Display, clock: Clock):
        self.__state_machine = state_machine
        self.__display = display
        self.__clock = clock
        self.__time_hours: int = 23
        self.__time_minutes: int = 59

    def land(self) -> None:
        # Triggered once this state turns active. It just resets the clock and forwards to running.
        self.__state_machine.change_state("RUNNING")
        self.__clock.start_clock(60 * 60 * self.__time_hours + 60 * self.__time_minutes, True)

    def time_in_seconds(self) -> int:
        return

    def handle_button_one(self) -> None:
        pass

    def handle_button_two(self) -> None:
        pass

    def handle_button_three(self) -> None:
        pass

    def handle_button_four(self) -> None:
        pass
