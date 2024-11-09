import threading

class Counter:
    counter = 0
    mutex = threading.Lock()

    @classmethod
    def increment(cls):
        # here since we are getting the mutex lock before running our range, all will increase the value uniformly
        # a bit slow as we are iterating a particular before releasing the mutex
        # if we want here non uniformity along with mutex then we can acquire mutex while incrementing and not the range
        with cls.mutex:
            for _ in range(10000000):
                cls.counter+=1
        print("Incremented, current counter:", cls.counter)

    @classmethod
    def increment_without_mutex(cls):
        # here the value will increase non-uniformly by a thread
        for _ in range(10000000):
            cls.counter+=1
        print("Incremented without mutex, current counter:", cls.counter)

threads = []
for _ in range(5):
    thread = threading.Thread(target=Counter.increment_without_mutex)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


threads = []
for _ in range(5):
    thread = threading.Thread(target=Counter.increment)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Final counter value:", Counter.counter)
