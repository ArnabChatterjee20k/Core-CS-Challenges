import threading,time,random

condition = threading.Condition()
shared_resource = ""

def producer():
    global shared_resource
    with condition:
        for _ in range(4):
            time.sleep(random.random())
            shared_resource = "item"
        # should be inside the condition context
        # notifying the consumer
        condition.notify()
    print("produced item")

def consumer():
    global shared_resource
    with condition:
        print("consumer is waiting")
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