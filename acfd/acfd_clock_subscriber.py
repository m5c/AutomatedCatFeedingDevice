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

    def notify_clock_started(self) -> None:
        pass

    def notify_clock_time_change(self, time_update: int) -> None:
        """
        Called whenever the clock has an update (remaining seconds). Must update display content.
        """
        # If time still contains hours (is 3600s or more), forget about seconds. The 4 digits
        # just show hours and minutes.
        # If below one hour, switch to minutes and seconds.
        if time_update >= 3600:
            # chop off seconds: display hours and minutes
            first_two_padded: str = to_zero_padded_number(time_update // 3600, 2)
            last_two_padded: str = to_zero_padded_number(time_update % 3600 // 60, 2)
        else:
            # time is below an hour: display minutes and seconds
            first_two_padded: str = to_zero_padded_number(time_update // 60, 2)
            last_two_padded: str = to_zero_padded_number(time_update % 60, 2)
        self.__display.update_content(first_two_padded + "." + last_two_padded + ".")

    def notify_clock_zero_reached(self) -> None:
        """
        Called by clock when 0 reached. Must transition to IDLE, perform lid open and then
        transition to SET_TIME.
        """
        # Ignore all inputs, open bay
        self.__state_machine.change_state("IDLE")
        self.__display.update_content("Food")
        self.__motor.open_acfd_blocking()

        ## Revolver machine does not turn off motor power, so current angle is locked and feline
        # cannot use paws to self-forward.
        # self.__motor.power_off()

        # Wait another 55 seconds, so the machine does not time-drift.
        sleep(55)

        # Transition to set time
        # self.__display.update_content("AUTO")
        # self.__clock.start_clock(5, True)
        # self.__state_machine.change_state("RUNNING")
        self.__state_machine.change_state("AUTO_CONTINUE")

    def notify_clock_stopped(self) -> None:
        """
        Invoked when clock is aborted. This can be safely ignored, as the button press four
        causes the clock abort.
        """
        self.__display.update_content("0000")
        self.__state_machine.change_state("SET_TIME")
