"""
Implements the ACFDs internal state machine. This is literally just a pointer to the current
state. Incoming button events are handled by the current state using polymorphism. The states know
how to react to input events.

Author: Maximilian Schiedermeier
"""
from acfd.display_utils.display import Display
from acfd.lid_motor import LidMotor
from acfd.state_machine.state import State
from acfd.state_machine.state_idle import StateIdle
from acfd.state_machine.state_set_time import StateSetTime


class StateMachine:

    def __init__(self, motor: LidMotor, display: Display):
        """
        Constructor for the StateMachine. Initializes the current state to IDLE.
        """
        # State machine state can be changed by name. States are singletons (which are not
        # properly supported by python, therefore we manually create a single instance per
        # state manually and let the state machine maintain those).
        self.__states = {
            "IDLE": StateIdle(),
            "SET_TIME": StateSetTime(display)
        }
        self.__state: State = self.__states.get("IDLE")

    @property
    def state(self) -> State:
        """
        Getter for current state machine state.
        """
        return self.__state

    def change_state(self, target_state: str) -> None:
        """
        Replaces current state by singleton like one and only instance of desired target state.
        """
        self.__state = self.__states[target_state]
