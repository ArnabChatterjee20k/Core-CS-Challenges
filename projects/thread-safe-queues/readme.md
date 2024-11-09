> The same thing is present in the official Queue of python
### dequeue

1. **Attempt to Acquire Mutex (`self.not_empty`)**
   - The current thread attempts to acquire the `self.mutex` lock, ensuring exclusive access to the queue.
   - If another thread currently holds the lock, this thread will wait until the lock is released.

2. **Check if Queue is Not Empty**
   - Once the thread holds `self.mutex`, it checks whether the queue contains items.
   - At this point, no other threads can modify the queue (either by getting or putting items) since they would also need to hold `self.mutex` to do so.

3. **Handle Empty Queue (Wait State)**
   - If the queue is empty, the thread pauses at `self.not_empty.wait()`, releasing the `self.mutex` lock temporarily.
   - By releasing the lock, other threads are now able to acquire `self.mutex` and potentially add new elements to the queue.

4. **Adding New Element (`self.not_empty.notify()`)**
   - When a new item is added to the queue, another thread calls `self.not_empty.notify()`.
   - This notification awakens any threads waiting for items to be added to the queue.

5. **Reacquire Mutex and Proceed**
   - A waiting thread wakes up, reacquires `self.mutex`, and now proceeds since it has exclusive access and knows the queue is no longer empty.
   - The thread can now safely pop an item from the queue.

6. **Pop Item from Queue**
   - The thread removes an item from the queue while holding `self.mutex`, ensuring no other threads can access or modify the queue simultaneously.

7. **Notify Queue Availability and Release Mutex**
   - After retrieving an item, the consumer thread notifies any waiting threads that the queue has space (it is no longer full).
   - Finally, the thread returns the item and releases the `self.mutex` lock, allowing other threads to access the queue.

### enqueue