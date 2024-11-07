from .Process import Process, State
from .Queues import ReadyQueue, TerminateQueue, Queue

class ShortTermScheduler:
    def __init__(self, time_quantum=2):
        self.time_quantum = time_quantum
        self.ready_queue = ReadyQueue()
        self.terminate_queue = TerminateQueue()
        self.gnatt_chart = []
        self.current_time = 0

    def push_to_ready_queue(self, process: Process):
        process.change_state(state=State.READY)
        self.ready_queue.enque(process)

    def handle_termination(self, process: Process):
        process.terminate()
        self.terminate_queue.enque(process)

    def round_robin(self):
        while self.ready_queue.processes:
            process = self.ready_queue.dequeue()

            # If the process's arrival time is greater than the current time, enqueue it back and move current time
            if process.arrival_time > self.current_time:
                self.ready_queue.enque(process)
                self.current_time = process.arrival_time
                continue

            process.change_state(State.RUNNING)
            self.gnatt_chart.append(process.pid)

            
            time_slice = self.time_quantum

            while time_slice:
                if process.burst_time <= 0:
                    self.handle_termination(process)
                    break
                process.burst_time -= 1
                process.last_executed_time += 1
                self.current_time += 1
                time_slice -= 1
                if process.burst_time == 0:
                    self.handle_termination(process)
                    break

            if process.state != State.TERMINATED:
                self.ready_queue.enque(process)

            process.change_state(State.READY)

        return {"totalTime":self.current_time,"gant":self.gnatt_chart,"termination":self.terminate_queue.processes}


class LongTermScheduler:
    def __init__(self, shortTermScheduler: ShortTermScheduler, processes: list[Process]):
        processes.sort(key=lambda p: p.arrival_time)

        for process in processes:
            shortTermScheduler.push_to_ready_queue(process)