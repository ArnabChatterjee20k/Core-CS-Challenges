"""
Making writing prior means
"""
import threading,csv,os,time
from typing import Literal
class CSVDatabase:
    def __init__(self,path:str,priority:Literal["WRITE","READ"]="READ"):
        self.path = path
        self.priority = priority
        self.reader_writer_lock = threading.Semaphore(1)
        self.reader_lock = threading.Semaphore(1)
        self.reader_count = 0
        self._create()
    def get(self,key:str):
        with self.reader_lock:
            if self.reader_count == 0:
                self.reader_writer_lock.acquire()
            self.reader_count+=1

        # critical section
        # acquired the data
        item = None
        with open(self.path,"r") as f:
            print("reading")
            reader = csv.reader(f)
            for row in reader:
                if row[0] == key:
                    item = row[1]

        with self.reader_lock:
            self.reader_count-=1
            if self.reader_count == 0:
                self.reader_writer_lock.release()
        # I made a silly made mistake by returning the item before hand
        # lock was not getting released and system got in the deadlock
        return item
    def write(self,key:str,value:str):
        with self.reader_writer_lock:
            print("writing")
            time.sleep(4)
            with open(self.path,"a") as f:
                writer = csv.writer(f)
                writer.writerow([key,value])

    def _create(self):
        if os.path.exists(self.path):
            return True
        with open(self.path,"w"):
            return True

if __name__ == "__main__":
    db = CSVDatabase("db.csv")
    reader = [threading.Thread(target=db.get,args=('hello',),daemon=True) for _ in range(5)]
    writer = [threading.Thread(target=db.write,args=("db","database"),daemon=True) for _ in range(5)]

    for thread in reader+writer:
        thread.start()
    for thread in reader+writer:
        thread.join()