"""
Implements lister for clock events. Has access to state machine to alter state, e.g. when zero
reached.
"""
from time import sleep

from acfd.clock_subscriber import ClockSubscriber
from acfd.display_utils.display import Display
from acfd.display_utils.display_content_formatter import to_zero_padded_number
from acfd.lid_motor import LidMotor


class AcfdClockSubscriber(ClockSubscriber):
    """
    Lister for clock updates, e.g. time changes or zero reached.
    """

    def __init__(self, state_machine: 'StateMachine', display: Display, motor: LidMotor):
        """
        Constructor.
        """
        self.__display: Display = display
        self.__state_machine: 'StateMachine' = state_machine
        self.__motor: LidMotor = motor

    def notify_clock_time_change(self, time_update: int) -> None:
        """
        Called whenever the clock has an update (remaining seconds). Must update display content.
        """
        print("Request to update display time "+str(time_update))
        self.__display.update_content(to_zero_padded_number(time_update, 4))

    def notify_clock_zero_reached(self) -> None:
        """
        Called by clock when 0 reached. Must transition to IDLE, perform lid open and then
        transition to SET_TIME.
        """
        self.__display.update_content("OPEN")
        sleep(2)
        self.__display.turn_off()
        # TODO: transition to IDLE, open bay, transition to SET TIME

    def notify_clock_stopped(self) -> None:
        """
        Invoked when clock is aborted. This can be safely ignored, as the button press four
        causes the clock abort.
        """
        pass
