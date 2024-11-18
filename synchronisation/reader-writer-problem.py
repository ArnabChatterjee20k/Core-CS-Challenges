"""
You will se multiple readers reading together(almost at same time printing in the terminal)
But writers doing it one by one
And after readers only writer are getting started
"""
import threading,time

read_count = 0
reader_lock = threading.Semaphore(1)
reader_writer_lock = threading.Semaphore(1) # we can increase

# Concurrency -> single writer , multiple readers

def reader(reader_id):
    global read_count
    # simulating continuos infinite flow
    while True:
        # enter
        with reader_lock:
            read_count+=1
            # acquire rw_lock only time when the first reader enters
            if read_count == 1:
                reader_writer_lock.acquire()
        
        # critical section reading
        print(f"Reader {reader_id} is reading")
        time.sleep(2) # reading simulation
    
        # exit
        with reader_lock:
            read_count-=1
            if read_count == 0:
                # Last reader unlocks the resource
                reader_writer_lock.release()
                    
        # periodic simulation
        time.sleep(1)

def writer(writer_id):
    while True:
        with reader_writer_lock:
            # critical section writing
            print(f"Writer {writer_id} is writing")
            time.sleep(3)
        # periodic simulation
        time.sleep(2)

reader_threads = [threading.Thread(target=reader, args=(i,),daemon=True) for i in range(3)]

writer_threads = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

for t in reader_threads + writer_threads:
    t.start()

# Wait for all threads to complete (infinite loop here for demo)
for t in reader_threads + writer_threads:
    t.join()