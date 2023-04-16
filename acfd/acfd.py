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



class Acfd(ClockSubscriber):

    def __init__(self):
        """
        Boot up the ACFD. Set welcome message on display, create clock, register button handlers.
        """
        print("ACFD")
        # Reset motor power, to prevent overheating from default GPIO values
        lid_motor.power_off()

        # Initialize display with welcome message
        self.__display: Display = Display("A.C.F.D.")
        #
        # Wait a moment, print ready function
        sleep(2)
        self.__display.update_content("----")

        sleep(2)
        self.__display.turn_off()
        # lid_motor.open_acfd_lid()
        #
        # sleep(2)
        #
        # # Test to show something else again
        # self.__display.update_content("WXYZ")
        # self.__display.turn_on()
        # sleep(2)
        # self.__display.turn_off()



        # Register button handlers
        register_button_callbacks(self.instant_open, self.test_message)

        # Set up clock
        # Set up test timer, subscribe to events and pass to display
        # self.__clock: Clock = Clock(10, self)
        # self.__clock.start_clock()

        sleep(100)

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
        lid_motor.open_acfd_lid()
        self.__display.turn_off()


    def aborted(self) -> None:
        """
        For now: Turn off display
        """
        print("ABORT called!")
        self.__display.turn_off()


    def instant_open(self, whatever):
        print("Foo")
        lid_motor.open_acfd_lid()
        # self.__display.set_content("OK")
        # # self.__display.enable_display()
        # sleep(1)
        # self.__display.turn_off()

    def test_message(self, whatever):
        print("Foo")
        self.__display.update_content("OK")
        self.__display.__enable_display()
        sleep(1)
        self.__display.turn_off()

Acfd()
