# 5. Using More Processes

## 5.1 Process-based Parallelism

- Key concepts:
	- **Processes**: Run in separate memory spaces and utilize multiple CPU cores.
	- **No GIL**: Not limited by the Global Interpreter Lock like threads.
	- **Stability**: A crash in one process doesn’t affect others.
	- **Best for**: **CPU-bound** tasks like heavy data processing.

| **Pros**                                       | **❌ Cons**                                                             |
| ---------------------------------------------- | ---------------------------------------------------------------------- |
| Utilizes **all available CPU** cores.          | **Higher memory** usage than threads.                                  |
| Isolated: more **stable** than multithreading. | **More complex** to share data between processes.                      |
| **No GIL**: true parallel execution.           | **Must balance** number of processes with physical cores.              |
| Ideal for **heavy, parallel workloads**.       | **Requires redesign** if there’s a lot of inter-process communication. |
```python
from multiprocessing import Process

class OrderProcessing(Process): # Create a subclass of Process
	def run(self):
		print("Processing")

process = OrderProcessing() # Create a new instance
process.start() # Start new process

def process_order(): # Python function
	print("Processing...")

p = Process(targer=process_order) # Cereate a new process
p.start() # Start the process
```

### Technical comparison

- CPU-Intensive task with 1 order and 1 process

```python
from multiprocessing import Process


def clean_order():
    for _ in range(500_000_000):
        pass
    print("Finished cleaning")


if __name__ == "__main__":
    p1 = Process(target=clean_order)
    p1.start()
    p1.join()
```


```bash
❯ time python more_processes.py
Finished cleaning
python3 more_processes.py  6,22s user 0,04s system 98% cpu 6,341 total
```

CPU-Intensive task with 2 order and 2 processes

```python
if __name__ == "__main__":
    p1 = Process(target=clean_order)
    p2 = Process(target=clean_order)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

```

```bash
❯ time python more_processes.py
Finished cleaning
Finished cleaning
python3 more_processes.py  12,53s user 0,09s system 194% cpu 6,492 total
```

- **Conclusion**: 
	- The processing time is almost the same in both cases `6.341` vs. `6.492`.
	- The process takes advantage of the extra CPU `98%` vs. `194%`.

## 5.2 Processes Communication

- Challenges
	- **Error handling**: Communication errors can block or crash the app.
	- **Synchronization**: Use locks/semaphores to avoid conflicts over shared resources.
	- **Completion coordination**: Use .join() to wait for all processes to finish.
	- **Workload balancing**: Avoid overloading some processes while others stay idle.

- Approaches for processes communication:
	- **Pipe**: Lightweight, fast; only two endpoints (one sender, one receiver).
	- **Queue**: Supports multiple producers/consumers; better for larger or shared data.

```python
import multiprocessing
from multiprocessing import Process
from random import randint

# Producer function
def producer(queue): 
	for i in range(10):
		queue.put(randint(1, 100))
	queue.put(None)

# Consumer function
def consumer(queue): 
	while True:
		item = queue.get()
		if item:
			print(f"Processed {item}")
		else:
			break
# Start several processes
if __name__ == '__main__':
	# Dedicated queue
	queue = multiprocessing.Queue() 
	# Create consumer/producer process, queue as argument
	consumer_process = Process(target=consumer, args=(queue,))
	producer_process = Process(targer=producer, args=(queue,))
	# Start processes
	consumer_process.start()
	producer_process.start
	# Wait processes to finish
	producer_process.join()
	consumer_process.join()
```

## 5.3 When to Use More Processes

| **Aspect**              | **Multiprocessing**                                      | **Threading**                             | **Asyncio**                                            |
| ----------------------- | -------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------ |
| **CPU usage**           | Uses **multiple CPU cores**                              | Only **1 core** (due to GIL)              | Only **1 core**, single-threaded                       |
| **Best for**            | **CPU-intensive** tasks                                  | **I/O-bound** tasks with some parallelism | **I/O-bound** tasks with many small, fast operations   |
| **Isolation**           | High (each process has its own memory)                   | Low (shared memory)                       | Low (shared state in single thread)                    |
| **Sync complexity**     | Low risk of bugs; better isolation                       | High risk due to shared state             | Lower risk, but complex flow                           |
| **Performance benefit** | High for CPU-intensive workloads                         | High only if waiting on I/O               | High when doing many concurrent I/O tasks              |
| **Drawbacks**           | More memory usage, harder inter-process communication    | GIL bottleneck, tricky sync bugs          | Learning curve, not all libraries are async-compatible |
| **Example use cases**   | - Parallel order processing- Producer/consumer pipelines | - Web scraping- File/network I/O          | - High-concurrency apps- Async APIs / networking       |

- **Tips for Using Multiprocessing**
	- Use logging to trace state and bugs across processes.
	- Terminate processes cleanly with .join() to release resources.
	- Monitor **CPU** and **RAM** usage during execution.
	- Avoid shared file access from multiple processes at the same time.
    - Don’t overspawn: keep process count close to number of CPU cores.

### Technical comparison

```python
# Multiprocessing
from multiprocessing import Process


def clean_order(order_id):
    for _ in range(500_000_000):
        pass
    print(f"Finished cleaning order with id={order_id}")


if __name__ == "__main__":
    first = Process(target=clean_order, args=(10,))
    second = Process(target=clean_order, args=(20,))
    first.start()
    second.start()
    first.join()
    second.join()

# Threading
import threading


def clean_order(order_id):
    for _ in range(500_000_000):
        pass
    print(f"Finished cleaning order with id={order_id}")


if __name__ == "__main__":
    first = threading.Thread(target=clean_order, args=(10,))
    second = threading.Thread(target=clean_order, args=(20,))
    first.start()
    second.start()
    first.join()
    second.join()
```

```bash
❯ time python clean_threads.py
Finished cleaning order with id=10
Finished cleaning order with id=20
python3 clean_threads.py  11,68s user 0,07s system 98% cpu 11,885 total
❯ time python clean_processes.py
Finished cleaning order with id=10
Finished cleaning order with id=20
python3 clean_processes.py  12,86s user 0,04s system 197% cpu 6,526 total
```

- **Conclusion**:
	- Multiprocessing is much faster than threading `6.52` vs. `11.885`.
	- They share similar syntax.
## 5.4 Scaling Fron One to More Machines

- Even with multithreading, asyncio, and multiprocessing, a **single machine** limits:
	- CPU cores
    - Memory
	- Reliability
- We can use more machines to scale.

| **Tool**       | **Description**                                                     | **Use Case**                          | **Notes**                                      |
| -------------- | ------------------------------------------------------------------- | ------------------------------------- | ---------------------------------------------- |
| **Celery**     | Task queue system with worker machines                              | Offload heavy tasks from web backends | Requires message broker (e.g. Redis)           |
| **Dask**       | Parallel computing with native support for NumPy & Pandas           | Data science, large-scale computation | Easy to scale from laptop to cluster           |
| **Ray**        | General-purpose distributed framework, supports ML workloads        | ML, deep learning, autoscaling        | Offers ML-specific tools and autoscaler        |
| **Kubernetes** | Container orchestration system for scaling and managing deployments | Any containerized application         | Must containerize app; used often in the cloud |
