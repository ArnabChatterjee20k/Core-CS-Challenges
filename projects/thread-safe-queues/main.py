"""
If using more than one consumer it is meant to stuck and not exit
As we are waiting for not_empty condition till the q_size is empty
We can solve this by timeout

The same thing happens in the Queue implementation of python
"""

from collections import deque
import threading,time
from queue import Queue
class ThreadSafeQueue:
    def __init__(self):
        self.queue = deque([])
        # using the same mutex/lock in both condition to synchronise
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
    def qsize(self):
        return len(self.queue)

    def dequeue(self):
        # not considering the timeout
        with self.not_empty:
            # if empty
            while not self.qsize():
                self.not_empty.wait()
            item = self._get()
            self.not_full.notify()
            return item

    def enqueue(self,item):
        with self.not_full:
            self._put(item)
            self.not_empty.notify()
    
    def _put(self,item):
        self.queue.append(item)

    def _get(self):
        return self.queue.popleft()

queue = ThreadSafeQueue()
def produce():
    print("getting item....")    
    time.sleep(2)
    queue.enqueue("hello")

def consume():
    print(queue.dequeue())

producer = threading.Thread(target=produce)
threads = [producer]

for _ in range(1):
    consumer = threading.Thread(target=consume)
    threads.append(consumer)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()