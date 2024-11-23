import socket
import time
import signal
import sys
import threading,time,random
from CSVDatabase import CSVDatabase
from cache import Cache
from HTTPHandler import HTTPHandler
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
THREAD_LIMIT = 10
class MultiThreadedRawServer:
    def __init__(self):
        self.threads:list[threading.Thread] = []
        self.thread_limit = threading.Semaphore(THREAD_LIMIT)
        self.terminate_event = threading.Event()
        self.connection_lock = threading.Lock()
        self.active_connections = 0

        self.db = CSVDatabase("db.csv")

        # Set up signal handler to ensure cleanup when exiting
        signal.signal(signal.SIGINT, self.exit_handler)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, self.exit_handler)  # Handle termination signal

    def exit_handler(self,sig, frame):
        print("\nExiting... Cleaning up!")
        self.terminate_event.set()
        print("semaphore ",self.thread_limit._value)
        for thread in self.threads:
            thread.join()
        sys.exit(0)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # Set socket option SO_REUSEADDR to allow rebinding quickly after exit
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                s.bind((HOST, PORT))
                s.listen()
                print(f"Server started at http://{HOST}:{PORT}")
                print(f"Concurrent Client Limit {self.thread_limit._value}")
                # accept call will wait for 1.0 sec only
                # s.settimeout(1.0)
                while not self.terminate_event.is_set():
                    conn, addr = s.accept()
                    thread = threading.Thread(target=self.connect_accept_client,args=(conn,addr),daemon=True)
                    self.threads.append(thread)
                    thread.start()

            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("Server shutting down...")
                s.close()

    def connect_accept_client(self,conn:socket.socket,addr):
        # client will wait for 10 s only
        conn.settimeout(10.0)
        # semaphore accquired
        with self.thread_limit:
            with conn:
                while not self.terminate_event.is_set():
                    print("semaphore ",self.thread_limit._value)
                    print(f"Connection from {addr}")
                    req_stream = conn.makefile("rb")
                    res_stream = conn.makefile("wb")
                    HTTPHandler(req_stream,res_stream)
                    # time.sleep(random.randint(1,4))
                    break # so that we 
            # semaphore released


server = MultiThreadedRawServer()
server.run()
