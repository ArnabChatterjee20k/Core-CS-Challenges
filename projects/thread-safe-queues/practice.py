from collections import deque
import threading
MAX = 2
class ThreadSafeQueue:
    def __init__(self):
        self.mutex = threading.Lock()
        self.not_full = threading.Condition(self.mutex)
        self.not_empty = threading.Condition(self.mutex)
        self.q = deque([])
    def pop(self):
        with self.not_empty:
            while not self.q:
                print("q is empty: waiting at pop")
                self.not_empty.wait()
            item = self.q.popleft()
            self.not_full.notify()
            return item
    
    def put(self,item):
        with self.not_full:
            while len(self.q)==MAX:
                print("q is full: waiting at put")
                self.not_full.wait()
            self.q.append(item)
            self.not_empty.notify()

import time
queue = ThreadSafeQueue()
def produce(item):
    print("putting item....")    
    time.sleep(2)
    queue.put(item)

def consume():
    import random
    time.sleep(random.randint(1,5))
    print(queue.pop())

producer1 = threading.Thread(target=produce,args=("p1",))
producer2 = threading.Thread(target=produce,args=("p2",))
producer3 = threading.Thread(target=produce,args=("p3",))
threads = [producer1,producer2,producer3]

for _ in range(3):
    consumer = threading.Thread(target=consume)
    threads.append(consumer)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()