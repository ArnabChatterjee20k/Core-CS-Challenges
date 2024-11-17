### Sockets
Python sockets -> https://realpython.com/python-sockets/
### terminating threads in python
https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread


### Non-daemon threads (default, daemon=False):

Program waits for these threads to complete before exiting
Main program won't exit until all non-daemon threads finish


### Daemon threads (daemon=True):

Program will exit without waiting for these threads
These threads will be abruptly terminated when main program exits
No cleanup, no proper socket closing, no context manager __exit__

### Events
On interruption we can make sure that no more connection is accepted or new thread spawns