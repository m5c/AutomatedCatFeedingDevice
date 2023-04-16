"""
Main acfd logic. Interprets input events from keypad and sets content for display, and controls
motor.
Author: Maximilian Schiedermeier
"""
from time import sleep

import lid_motor
from buttons_registrator import register_button_callbacks
from clock_subscriber import ClockSubscriber
from display.display import Display
from display.display_content_formatter import to_zero_padded_number
from lid_motor import LidMotor

class Acfd(ClockSubscriber):

    def __init__(self):
        """
        Boot up the ACFD. Set welcome message on display, create clock, register button handlers.
        Note: program is alive until display is switched on. Calling a turn off to display will
        likewise end program.
        """
        print("ACFD")

        # Obtain and reset motor, to prevent overheating from default GPIO values
        self.__lid_motor: LidMotor = LidMotor()
        self.__lid_motor.power_off()

        # Initialize display with welcome message
        self.__display: Display = Display("A.C.F.D.")
        #
        # Wait a moment, print ready function
        sleep(2)
        self.__display.update_content("----")

        # Register button handlers
        register_button_callbacks(self.instant_open, self.test_message)

    def update_time(self, time_update: int) -> None:
        """
        Callback function, invoked by clock on countdown.
        """
        print("Received time update: " + str(time_update))
        self.__display.update_content(to_zero_padded_number(time_update, 4))

    def zero_reached(self) -> None:
        """
        Turn off display
        """
        self.__display.update_content("OPEN")
        # this one is blocking
        self.__lid_motor.open_acfd()
        self.__display.turn_off()

    def aborted(self) -> None:
        """
        For now: Turn off display
        """
        print("ABORT called!")
        self.__display.turn_off()

    def instant_open(self, whatever_python_enforced_nonsense):
        self.__lid_motor.open_acfd()


    def test_message(self, whatever_python_enforced_nonsense):
        if not self.__display.running:
            self.__display.turn_on("OK")
        else:
            self.__display.update_content("OK")
        sleep(3)
        self.__display.turn_off()


Acfd()
