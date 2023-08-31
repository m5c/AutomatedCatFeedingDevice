"""
This module tests the motor wiring and simulates a lid open with subsequent parking of motor arm.
Code is based on an open source decision maker, but was afterwards commented in english and
modified to conform to python pylint checkstyle conventions.
Author: Maximilian Schiedermeier
"""
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO
import copy


class LidMotor:

    def __init__(self):
        # Pins used for ULN2003A driver board / GPIO.
        # Controller chip "+" goes to +5V, "-" goes to GND
        self.__motor_pins: list[int] = [2, 3, 4, 14]
        GPIO.setmode(GPIO.BCM)
        for i in range(len(self.__motor_pins)):
            GPIO.setup(self.__motor_pins[i], GPIO.OUT)

        # Time adds short delay between motor steps, so mechanic can catch up with program pin
        # iterations. Can also be set to a higher value to artificially slow down the motor
        # rotation.
        # Should be at least 2ms (0.002).
        self.__mechanism_adapt_delay: float = 0.002

        # Set to true if you want to skip double coil steps (two neighboured coils activate as
        # intermediate steps). Is not reliable with 3V3, and I don't recommend 5V as it overhears
        # ULN2003
        # driver and motor.
        self.__mechanism_skip_intermediate_steps: bool = False

        # Motor steps iteration map for forward and backward ticks
        self.__tick_steps: list[list[bool]] = [[True, False, False, False],
                                               [True, True, False, False],
                                               [False, True, False, False],
                                               [False, True, True, False],
                                               [False, False, True, False],
                                               [False, False, True, True],
                                               [False, False, False, True],
                                               [True, False, False, True]]
        self.__backward_tick_steps: list[list[bool]] = copy.deepcopy(self.__tick_steps)
        self.__backward_tick_steps.reverse()

        # thread lock variable to prevent motor commands while already running.
        self.__running = False

    def power_off(self) -> None:
        """
        Resets all motor pins to turn off leds and prevent initial mini step.
        :return: None
        """
        for motor_pin in self.__motor_pins:
            GPIO.output(motor_pin, False)

    def __rotate(self, angle: int) -> None:
        """
        Turn motor
        :param angle: amount in degrees to rotate clockwise
        :return: None
        """

        # Due to motor physics we need twice as many iterations as desired rotation in degrees.
        ticks: int = abs(angle) * 2
        forward: bool = (angle > 0)

        # Run as many ticks as requestes (internal rotations), using requested direction and coil
        # smode.
        for _ in range(ticks):
            self.__tick(forward, self.__mechanism_skip_intermediate_steps)
        self.power_off()

    def __tick(self, forward: bool, skip_intermediate_steps: bool) -> None:
        """
        Runs one complete motor internal coil iteration
        :param: forward true to turn clockwise, false for counter-clockwise.
        :param: false to include all semi steps where two neighboured coils power up at once.
        of the four single coils only.
        Note that a tick is NOT a motor rotation, due to the internal motor gears.
        :return: None
        """
        # By default, every step in stepper iterations is considered.
        iterator_size = 1
        if skip_intermediate_steps:
            iterator_size *= 2

        # Either cycle forward or backward through predefined sequence
        steps: list[list[bool]] = self.__tick_steps
        if not forward:
            steps = self.__backward_tick_steps

        # Iterate through the predefined motor steps, iterate by requested amount between steps.
        iteration = 0
        while iteration < len(steps):
            # Configure pins to next desired iteration
            for idx, pin in enumerate(self.__motor_pins):
                GPIO.output(pin, steps[iteration][idx])

            # Give the motor mechanism a brief moment to adapt
            sleep(self.__mechanism_adapt_delay)

            # Increment iterator (will increment by two if skip enabled)
            iteration += iterator_size

    def open_acfd_blocking(self) -> None:
        """
        Opens the ACFD lid by turning the motor from parking position to 85degrees up.
        Then returns arm into parking position.
        The values for up and down are not identical, since we undervolt the motor, to prevent
        overheating and the gravity on the lid reduces torc.
        :return: None.
        """
        self.__running = True
        self.__rotate(-105)  # -100
        self.__rotate(81)  # 83
        self.__running = False

    def open_acfd(self) -> None:
        """
        Threaded version of above function. Cannot be called while motor is already running.
        """
        if self.__running:
            raise Exception("Cannot start motor. Is currently running.")

        count_down_thread = Thread(target=self.__open_acfd_blocking)
        count_down_thread.start()
