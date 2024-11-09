from threading import Semaphore,Thread
import time

# at a time only two threads will work
semaphore = Semaphore(2)

def access_resource(id):
    semaphore.acquire()
    print(f"thread-{id} making api call")
    time.sleep(1)
    semaphore.release()

threads = []
for i in range(5):
    thread = Thread(target=access_resource,args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()