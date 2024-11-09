"""
so basically it is needed when two threads spawned producer and consumer
producer did something and notify
consumer did something and cant proceed untill notified
"""
import threading,time

# Shared resource
shared_resource = []

# Condition variable
condition = threading.Condition()

# Consumer thread
def consumer():
    with condition:
        print("api call done by consumer")
        while not shared_resource:
            print("Consumer is waiting...")
            condition.wait()
        item = shared_resource.pop(0)
        print("Consumer consumed item:", item)

# Producer thread
def producer():
    with condition:
        item = "New item"
        shared_resource.append(item)
        time.sleep(2)
        print("Producer produced item:", item)
        condition.notify()

# Create and start the threads
consumer_thread = threading.Thread(target=consumer)
producer_thread = threading.Thread(target=producer)
consumer_thread.start()
producer_thread.start()