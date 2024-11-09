"""
Using time.sleep is necessary to simulate a time buffer
Here the order should be-> 

produced item
shared_resource = "item"
consumed item
shared_resource = "item-consumed"

But due to concurrent execution of threads the order sometimes not getting maintained
"""
import threading,time,random

shared_resource = ""

def producer():
    global shared_resource
    for _ in range(4):
        time.sleep(random.random())
        shared_resource = "item"
    print("produced item")

def consumer():
    global shared_resource
    for _ in range(4):
        time.sleep(random.random())
        shared_resource = "item-consumed"
    print("consumed item")


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print(shared_resource)