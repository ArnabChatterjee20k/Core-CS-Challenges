* A child process is created.
* The child runs for 2 seconds and exits.
* The parent waits for 5 seconds (during which the child becomes a zombie).
* The parent collects the child's exit status using wait().
* After wait() returns, the child's PID is removed from the process table.