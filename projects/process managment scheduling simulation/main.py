from package.Process import Process
from package.Scheduler import ShortTermScheduler,LongTermScheduler

def simulate():
    process_list_1 = [
    Process(pid=1, burst=6, arrival=0, priority=1),
    Process(pid=2, burst=4, arrival=2, priority=2),
    Process(pid=3, burst=3, arrival=4, priority=3),
    Process(pid=4, burst=5, arrival=6, priority=4)
]
    short_term_scheduler = ShortTermScheduler(3)
    long_term_scheduler = LongTermScheduler(processes=process_list_1,shortTermScheduler=short_term_scheduler)

    print(short_term_scheduler.round_robin())

simulate()