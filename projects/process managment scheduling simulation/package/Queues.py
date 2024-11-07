from collections import deque
from .Process import Process


class Queue:
    def __init__(self):
        self.processes = deque([])

    def enque(self, process: Process):
        self.processes.append(process)

    def dequeue(self)->Process:
        return self.processes.popleft()

class JobQueue(Queue):
    def __init__(self):
        super().__init__()
    # other methods if required


class ReadyQueue(Queue):
    def __init__(self):
        super().__init__()
    # other methods if required


class TerminateQueue(Queue):
    def __init__(self):
        super().__init__()
        # other methods if required
