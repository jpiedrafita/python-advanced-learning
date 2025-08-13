# 4. Using Asynchronous Code

## 4.1 Asynchronous Code

- Key concepts:
	- **Coroutine**: A special function defined with async def. Executes asynchronously.
	- **Event loop**: Manages and schedules coroutines. Runs all async code.
	- **await**: Pauses execution until an awaited coroutine completes.
	- **asyncio.run()**: Entry point that starts the event loop and calls the main coroutine.

| **Aspect**            | **Async (asyncio)**                                        | **Threads (threading)**                       |
| --------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| **Overhead**          | Low (no thread switching)                                  | Higher (context switching, memory)            |
| **Bugs**              | Fewer (no shared state)                                    | More (shared state, race conditions)          |
| **Learning Curve**    | High (new syntax and async patterns)                       | Low (familiar syntax)                         |
| **Compatibility**     | Limited (depends on async-compatible libraries)            | High (most existing libraries work)           |
| **Best for**          | Many small I/O-bound tasks (e.g., HTTP requests, file I/O) | Few threads with simple logic or blocking I/O |
| **Parallelism (CPU)** | No (single-threaded execution)                             | No (limited by the GIL)                       |

| **Aspect**               | **Benefit**                                                            | **Trade-off**                                                       |
| ------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Bug avoidance**        | Fewer synchronization issues (no shared state, no race conditions)     | Requires understanding coroutine behavior and async execution flow  |
| **Performance overhead** | Lower overhead (no thread switching)                                   | Doesn’t leverage multiple CPU cores (single-threaded)               |
| **Concurrency**          | Efficient for many small I/O-bound tasks                               | Poor performance for CPU-bound tasks                                |
| **Resource usage**       | Better core utilization when dealing with many wait states (e.g., I/O) | Misuse can result in sequential execution if not scheduled properly |
| **Code maintainability** | Cleaner for concurrent I/O-heavy workflows                             | Increased complexity due to new syntax (async, await, etc.)         |
| **Compatibility**        | Great with async-native libraries (e.g., aiohttp, aiomysql)            | Limited compatibility with traditional sync libraries               |

```python
import asyncio

async def process_order(): # Define new corutine
	await asyncio.sleep(1) # Wait with await
	print("Order complete")

async def main(): # Define another coroutine
	await process_order() # Call and await for coroutine
	print("Finished processing")

asyncio.run(main()) # Start event loop
```

### Technical comparison

```python
import asyncio


async def process_order():
    await asyncio.sleep(1)
    print("Order complete")


async def main():
    await process_order()
    await process_order()
    print("Finished processing")


asyncio.run(main())
```

```bash
❯ time python orders_asincio.py
Order complete
Order complete
Finished processing
python3 orders_asincio.py  0,04s user 0,02s system 2% cpu 2,091 total
```

- **Conclusion**:
	- It takes 2s because the 2nd order waits the first one to complete.

## 4.2 Challenges of Working With asycio

- **Curva de aprendizaje**
	- New syntax (async, await)
	- New concepts (coroutines, event loop)
	- New libraries (aiohttp, aiomysql, etc.)
- **Dificultad para depurar**
	- Not Obvious execution order
	- Shared state among concurrent tasks
	- Event loop puede can hide subtle errors
- **Compatibilidad**
	- Many libraries are not prepared for async
	- The  _blocking_ code (like time.sleep) blocks the entire event loop
### Technical comparison

- Testing `asyncio` execution (non-blocking)
	- Correct usage of `asyncio.sleep`
	- Task executed in parallel

```python
import asyncio


async def process_order():
    await asyncio.sleep(1)
    print("Order complete")


async def main():
    await asyncio.gather(process_order(), process_order())
    print("Finished processing")


asyncio.run(main())
```

```bash
❯ time python challenges_asyncio.py
Order complete
Order complete
Finished processing
python3 challenges_asyncio.py  0,04s user 0,02s system 5% cpu 1,083 total
```

- Testing with blocking code 
	- Incorrect use
	- Mixes `asyncio` with `time.sleep`, blocking the event loop

```python
import time


async def process_order():
    await asyncio.sleep(1)
    time.sleep(3)  
    print("Order complete")
```

```bash
❯ time python challenges_asyncio.py
Order complete
Order complete
Finished processing
python3 challenges_asyncio.py  0,05s user 0,02s system 0% cpu 7,103 total
```

- Testing asyncop with CPU-Bound task.
	- Intensive CPU code without concurrency benefit.
	- Locks event loop.

```python
import asyncio
import time


async def process_order():
    # await asyncio.sleep(1)
    # time.sleep(3)
    for _ in range(100_000_000):
        pass
    print("Order complete")


# 1 order
async def main():
    await process_order()
    # await asyncio.gather(process_order(), process_order())
    print("Finished processing")

# 2 concurrent orders
async def main():
    # await process_order()
    await asyncio.gather(process_order(), process_order())
    print("Finished processing")

asyncio.run(main())
```

```bash
# 1 order
❯ time python challenges_asyncio.py
Order complete
Finished processing
python3 challenges_asyncio.py  1,28s user 0,02s system 97% cpu 1,336 total
# 2 concurrent orders
❯ time python challenges_asyncio.py
Order complete
Order complete
Finished processing
python3 challenges_asyncio.py  2,40s user 0,02s system 99% cpu 2,448 total
```

- **Conclusion**:
	- **non-blocking**: Both orders were processed concurrently in ~1s because `await asyncio.sleep(1)` did not blocked the thread.
	- **Blocking**: Since `time.sleep(3)` is blocking is keeping the main thread blocked for 3s for each call, so total execution time ~2x3+1s instead 4s.
	- **CPU-intensive**: 2 concurrent orders takes twice as 1 order.

## 4.3 When to Use asyncio

| **Use asyncio when…**                                                                                    | **Avoid asyncio when…**                                                      |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Your application performs many **I/O operations** (network, disk, etc.)                                  | Your application performs **CPU-intensive tasks**.                           |
| You have **many small** tasks that can run concurrently                                                  | There is **blocking code** (like time.sleep or subprocess.run)               |
| You want to **avoid** the complexity and risks of **thread synchronization**                             | You use **dependencies/libraries** that don’t have async versions            |
| You’re building a **network application** or scraper that needs to scale. **Data processing pipelines**. | The code is simple, linear, or doesn’t justify the added complexity of async |
| Your core dependencies have asynchronous versions (aiohttp, aiomysql, etc.)                              | You’re not familiar with the syntax or execution model of asyncio            |

### Technical comparison

```python
import asyncio
from urllib import request

import aiohttp


def download():
    return request.urlopen("http://google.com").read()


def synchronous():
    for _ in range(5):
        download()


async def async_download(session, url):
    async with session.get(url) as response:
        return await response.text()


async def asynchronous():
    async with aiohttp.ClientSession() as session:
        coroutines = [async_download(session, "https://google.com") for _ in range(5)]
        await asyncio.gather(*coroutines)


@profile
def main():
    synchronous()
    asyncio.run(asynchronous())


main()
```


```bash
❯ kernprof -lv download_asyncio.py
Wrote profile results to download_asyncio.py.lprof
Timer unit: 1e-06 s

Total time: 2.35864 s
File: download_asyncio.py
Function: main at line 27

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    27                                           @profile
    28                                           def main():
    29         1    1743511.0    2e+06     73.9      synchronous()
    30         1     615133.0 615133.0     26.1      asyncio.run(asynchronous())
```

- **Conclusion**: 
	- `asyncio` gives a significant performance improvement from the synchronous code, `26.1` vs. `73.9`