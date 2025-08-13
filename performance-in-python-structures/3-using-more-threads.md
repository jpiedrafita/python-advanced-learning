# 3. Using More Threads

## 3.1 What Are Threads?

- **Thread**: A separate flow of execution within a process.
- **Process**: An instance of a running program. May contain one or more threads.
- **Concurrency**:  The ability to run multiple tasks in overlapping time periods without necessarily executing them simultaneously.
- **GIL (Global Interpreter Lock)**: Only one thread can run Python code at a time in CPython.

| **Aspect**    | **Threads**                                       | **Processes**                          |
| ------------- | ------------------------------------------------- | -------------------------------------- |
| Creation cost | Lightweight, fast                                 | Heavier, more expensive                |
| Memory        | Shared (can access same variables)                | Isolated memory                        |
| Data exchange | Easy but risky (shared state)                     | Harder, requires IPC                   |
| Risk of bugs  | Higher (race conditions, shared state)            | Lower (isolated execution)             |
| GIL           | Yes (only one thread runs at a time)              | No GIL (true parallelism possible)     |
| Ideal for     | I/O-bound tasks (e.g., waiting on files, network) | CPU-bound tasks (parallel computation) |
- **Creating threads in Python**
	1. Subclassing `Thread`.
	2. Using `Thread(target=...)`.
	
```python
import threading

#1
class OrderProcessing(threading.Thread): # Create a subclass of Thread
	def run(self):
		print("Processing")

thread = OrderProcessing() # Instantiate the new class

thread.start() # Start the new thread

#2
def process(): # Python function
	print("Processing...")

t = threading.Thread(target=process) # Create the new thread

t.start() # Start the new thread
```

### Technical comparison

```python
import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order with id={order_id}")
    sleep(1)
    print(f"Finished processing order with id={order_id}")


first_thread = threading.Thread(target=process_order, args=(10,))
second_thread = threading.Thread(target=process_order, args=(20,))

first_thread.start()
second_thread.start()
```

```bash
❯ python more_threads.py
Processing order with id=10
Processing order with id=20
Finished processing order with id=10
Finished processing order with id=20
```

- **Conclusion**: 
	- The second order starts being processed before the first one finished. There si room for optimization.

## 3.2 Challenges of Working with Threads

- Main challenges

| **Challenge**                     | **Description**                                                   |
| --------------------------------- | ----------------------------------------------------------------- |
| **Synchronization**               | Coordinating threads that access shared resources safely.         |
| **Debugging & Troubleshooting**   | Bugs are hard to reproduce and diagnose, especially under load.   |
| **Global Interpreter Lock (GIL)** | Only one thread can execute Python bytecode at a time in CPython. |
- Common bugs

| **Bug Type**       | **Description**                                                                |
| ------------------ | ------------------------------------------------------------------------------ |
| **Race Condition** | Threads read/write the same variable concurrently, causing unexpected results. |
| **Deadlock**       | Threads wait on each other indefinitely for resources.                         |
| **Starvation**     | A thread never gets access to a resource due to other dominant threads.        |
| **Livelock**       | Threads keep changing state but make no progress (spinning behavior).          |

- Debugging Multithreaded Code
	- Bugs are **nondeterministic** and **hard to reproduce**.
	- Might appear only under **production loads**.
	- **Debugging tools** may change thread behavior.
	- Finding root causes is harder in **large, complex** codebases.

- The Global Interpreter Lock (GIL)
	- Limits parallel execution for **CPU-bonud** code. Limits the execution of 1 thread at a time. Even with that limitation there is margin for improvement.
		- `sleep()` releases the GIL.
	- Simplifies memory management and avoids race conditions on Python objects.
	- GIL has the most impact on CPU-intensive tasks.
		- Two CPU-intensive threads will not have a performance advantage from multithreading.
### Technical comparison

- Non-intensive workload

```python
import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order with id={order_id}")
    sleep(1)
    print(f"Finished processing order with id={order_id}")


first_thread = threading.Thread(target=process_order, args=(10,))
second_thread = threading.Thread(target=process_order, args=(20,))

first_thread.start()
second_thread.start()
```


```bash
❯ time python challenges_threads.py #commenting second_thread.start()
Processing order with id=10
Finished processing order with id=10
python3 challenges_threads.py  0,02s user 0,01s system 2% cpu 1,044 total
❯ time python challenges_threads.py
Processing order with id=10
Processing order with id=20
Finished processing order with id=10
Finished processing order with id=20
python3 challenges_threads.py  0,02s user 0,01s system 2% cpu 1,033 total
```

- Intensive workload

```python
import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order with id={order_id}")
    # sleep(1)
    for _ in range(100_000_000):
        pass
    print(f"Finished processing order with id={order_id}")


first_thread = threading.Thread(target=process_order, args=(10,))
second_thread = threading.Thread(target=process_order, args=(20,))

first_thread.start()
second_thread.start()
```

```bash
❯ time python challenges_threads.py #commenting second_thread.start()
Processing order with id=10
Finished processing order with id=10
python3 challenges_threads.py  1,20s user 0,01s system 97% cpu 1,236 total
❯ time python challenges_threads.py
Processing order with id=10
Processing order with id=20
Finished processing order with id=20
Finished processing order with id=10
python3 challenges_threads.py  2,53s user 0,02s system 99% cpu 2,571 total
```

- **Conclusion**:
	- There isn't any advantage of using multithreading for intensive workloads.
	- The optimization for multithreading ranges from *nothing* to *excellent*.
	- For non non-intensive workload
		- Using 1 thread for 1 order takes ~1s.
		- Using 2 threads for 2 orders takes ~1s.
	- For an intensive workload
		- Using 1 thread for 1 order takes ~1.2s.
		- Using 2 threads for 2 orders takes ~2.5s.

## 3.3 When to Use Multithreading

- Main synchronization tools

| **ool**                 | **Description**                                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Lock**                | Only one thread can acquire it at a time. Prevents concurrent access to shared resources.                         |
| **Semaphore**           | Allows a limited number of threads to acquire it concurrently. Useful for limiting resources like DB connections. |
| **Condition variables** | Lets threads wait for a condition to be met. Another thread can notify them when the condition is satisfied.      |

| **✅ Use Threads When…**                                        | **❌ Avoid Threads When…**                                    |
| -------------------------------------------------------------- | ------------------------------------------------------------ |
| Tasks are **I/O-bound** (e.g., file, network, sleep)           | Tasks are **CPU-bound** (heavy computation)                  |
| The app **waits for external events** (e.g., user input)       | The app doesn’t involve waiting or blocking operations       |
| You want to **handle multiple I/O tasks concurrently**         | You need **true parallelism** (use multiprocessing)          |
| Logic is **simple** with **minimal synchronization**           | Logic involves **complex shared state or coordination**      |
| You want to **improve responsiveness** (e.g., GUI, web server) | Threads offer **no clear performance gain** in your scenario |

### Technical comparison

```python
import threading
from urllib import request


def download():
    return request.urlopen("http://google.com").read()


def single_thread():
    for _ in range(5):
        download()


def multiple_threads():
    threads = []
    for _ in range(5):
        threads.append(threading.Thread(target=download))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


@profile
def main():
    single_thread()
    multiple_threads()


main()
```

```bash
❯ kernprof -lv download_threads.py
Wrote profile results to download_threads.py.lprof
Timer unit: 1e-06 s

Total time: 4.52241 s
File: download_threads.py
Function: main at line 24

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def main():
    26         1    4091714.0    4e+06     90.5      single_thread()
    27         1     430700.0 430700.0      9.5      multiple_threads()
```

- **Conclusion**:
	- Multiple threads get a x10 performance improvement.