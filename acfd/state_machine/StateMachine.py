"""
Implements the ACFDs internal state machine. This is literally just a pointer to the current
state. Incoming button events are handled by the current state using polymorphism. The states know
how to react to input events.

Author: Maximilian Schiedermeier
"""

from acfd.state_machine.State import State


class StateMachine:

    def __init__(self):
        """
        Constructor for the StateMachine. Initializes the current state to IDLE.
        """
        self.state: State = Idle()
