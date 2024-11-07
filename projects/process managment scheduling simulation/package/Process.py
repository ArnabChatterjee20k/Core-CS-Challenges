from enum import Enum

class State(Enum):
    IDLE = "idle"
    READY = "READY"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"
    WAITING = "WAITING" # will not be required here as we are not waiting for IO here

class Process:
    def __init__(self,pid,burst,arrival,priority):
        self.pid = pid
        self.burst_time = burst
        self.arrival_time = arrival
        self.priority = priority
        self.state = State.IDLE
        self.last_executed_time = 0
        self.completion_time = 0

    def change_state(self,state):
        self.state = state
        # other required functions

    def terminate(self):
        self.change_state(State.TERMINATED)
        self.completion_time = self.last_executed_time
        # TODO: handle completion time

    def __repr__(self) -> str:
        return str(self.pid)