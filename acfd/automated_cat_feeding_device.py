"""
Main ACFD module.
Start with: python3 -m acfd.automated_cat_feeding_device
Author: Maximilian Schiedermeier
"""
from time import sleep

from acfd.buttons_registrator import register_button_callbacks
from acfd.display_utils.display import Display
from acfd.lid_motor import LidMotor
from acfd.state_machine_utils.state_machine import StateMachine


class AutomatedCatFeedingDevice:
    """
    Main ACFD class.
    """

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
        self.__display.update_content("A   ")
        sleep(0.2)
        self.__display.update_content("A.   ")
        sleep(0.2)
        self.__display.update_content("A.C  ")
        sleep(0.2)
        self.__display.update_content("A.C.  ")
        sleep(0.2)
        self.__display.update_content("A.C.F ")
        sleep(0.2)
        self.__display.update_content("A.C.F. ")
        sleep(0.2)
        self.__display.update_content("A.C.F.D")
        sleep(0.2)
        self.__display.update_content("A.C.F.D.")
        sleep(0.5)
        self.__display.update_content("0000")

        # First manual transit from IDLE to set time. Just by changing this, the buttons become
        # active.
        self.__state_machine.change_state("SET_TIME")

        # There is no need for permanent loop here, the program remains active until the display
        # is turned off.


AutomatedCatFeedingDevice()
