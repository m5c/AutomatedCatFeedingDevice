"""
Main acfd logic. Interprets input events from keypad and sets content for display_utils,
and controls
motor.
Author: Maximilian Schiedermeier
"""
from time import sleep

from acfd.buttons_registrator import register_button_callbacks
from acfd.display_utils.display import Display
from acfd.lid_motor import LidMotor
from acfd.state_machine_utils.state_machine import StateMachine


class AutomatedCatFeedingDevice:

    def __init__(self):
        """
        Boot up the ACFD. Set welcome message on display_utils, create clock, register button
        handlers.
        Note: program is alive until display_utils is switched on. Calling a turn off to
        display_utils will
        likewise end program.
        """

        # Obtain and reset motor, to prevent overheating from default GPIO values
        self.__lid_motor: LidMotor = LidMotor()
        self.__lid_motor.power_off()

        # Button registration should happen before display_utils initialization, as it overloads the
        # system and causes a display_utils glitch.
        # We therefore do a little trick and initialize the display_utils empty. So we have an
        # instance, but don't cause the glitch.
        self.__display: Display = Display("    ")

        # Initialize state machine in IDLE state, so button events have no effect until power up
        # complete.
        self.__state_machine = StateMachine(self.__lid_motor, self.__display)

        # Registering callbacks briefly overloads system, leading to display_utils glitch.
        # Buttons must
        # be registered before display_utils powers up:
        # NOTE: State machine should cause button presses to be without effect until boot
        # procedure completed.
        register_button_callbacks(self.__state_machine)

        # Initialize display_utils with welcome message
        # wait a moment, then turn display_utils to "dashed" to indicate that system is ready.
        self.__display.update_content("A.C.F.D.")
        sleep(2)
        self.__display.update_content("0000")

        # First manual transit from IDLE to set time. Just by changing this, the buttons become
        # active.
        self.__state_machine.change_state("SET_TIME")

        # There is no need for permanent loop here, the program remains active until the
        # display_utils is
        # turned off.
        # sleep(2)
        # self.__display.turn_off()

    # def update_time(self, time_update: int) -> None:
    #     """
    #     Callback function, invoked by clock on countdown.
    #     """
    #     print("Received time update: " + str(time_update))
    #     self.__display.update_content(to_zero_padded_number(time_update, 4))
    #
    # def zero_reached(self) -> None:
    #     """
    #     Turn off display_utils
    #     """
    #     self.__display.update_content("OPEN")
    #     # this one is blocking
    #     self.__lid_motor.open_acfd()
    #     self.__display.turn_off()
    #
    # def aborted(self) -> None:
    #     """
    #     For now: Turn off display_utils
    #     """
    #     print("ABORT called!")
    #     self.__display.turn_off()
    #
    # def instant_open(self, whatever_python_enforced_nonsense):
    #     self.__lid_motor.open_acfd()
    #
    # def test_message(self, whatever_python_enforced_nonsense):
    #     if not self.__display.running:
    #         self.__display.turn_on("OK")
    #     else:
    #         self.__display.update_content("OK")
    #     sleep(3)
    #     self.__display.turn_off()


AutomatedCatFeedingDevice()
