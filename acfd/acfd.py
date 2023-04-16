"""
Main acfd logic. Interprets input events from keypad and sets content for display, and controls
motor.
Author: Maximilian Schiedermeier
"""
from time import sleep

import lid_motor
from clock import Clock
from clock_subscriber import ClockSubscriber
from display.display import Display
from display.display_content_formatter import to_zero_padded_number


class Acfd(ClockSubscriber):

    def __init__(self):
        """
        Boot up the ACFD. Set welcome message on display, create clock, register button handlers.
        """
        # Reset motor power, to prevent overheating from default GPIO values
        lid_motor.power_off()

        # Initialize display with welcome message
        self.__display: Display = Display()
        self.__display.set_content("A.C.F.D.")

        # Wait a moment, print ready function
        sleep(2)
        self.__display.set_content("----")

        sleep(5)
        self.__display.turn_off()

        # Register button handlers

        # Set up clock
        # Set up test timer, subscribe to events and pass to display
        # self.__clock: Clock = Clock(10, self)
        # self.__clock.start_clock()

    def update_time(self, time_update: int) -> None:
        """
        Callback function, invoked by clock on countdown.
        """
        print("Received time update: " + str(time_update))
        self.__display.set_content(to_zero_padded_number(time_update, 4))

    def zero_reached(self) -> None:
        """
        Turn off display
        """
        self.__display.set_content("OPEN")
        # this one is blocking
        lid_motor.open_acfd_lid()
        self.__display.turn_off()


    def aborted(self) -> None:
        """
        For now: Turn off display
        """
        print("ABORT called!")
        self.__display.turn_off()


Acfd()
