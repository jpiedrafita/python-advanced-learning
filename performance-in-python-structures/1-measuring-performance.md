# 1. Measuring Performance

## 1.1 Lists and Arrays

| **Feature**                | **Lists**                   | **Built-in Arrays**             | **NumPy Arrays**                     |
| -------------------------- | --------------------------- | ------------------------------- | ------------------------------------ |
| *Mutability*               | Mutable                     | Mutable                         | Mutable                              |
| *Type of Items*            | Mixed types allowed         | Only specific types (e.g., int) | Mostly numeric (but supports dtypes) |
| *Memory Efficiency*        | Medium                      | Very high                       | High                                 |
| *Performance for Math Ops* | Slow                        | Medium                          | Very fast                            |
| *Popularity*               | Very popular                | Less popular                    | Very popular                         |
| *Use Case*                 | General-purpose collections | Compact storage                 | Numeric computations                 |
| *Memory Allocation*        | Preallocated extra room     | No preallocation                | Optimized under the hood             |
| *Flexibility*              | Very flexible               | Low flexibility                 | High flexibility for numeric data    |
| *Example Operation Speed*  | O(1) get/set/append         | O(1) get/set                    | Vectorized (bulk) operations O(n)    |

### Technical comparison

```python
import numpy as np


def double_list(size):
    initial_list = list(range(size))
    return [2 * i for i in initial_list]


def double_array(size):
    initial_array = np.arange(size)
    return initial_array * 2


double_array(1_000_000)
double_list(1_000_000)

```

```bash
❯ python -m cProfile -o list_array.prof list_array.py
❯ snakeviz list_array.prof
```

The ```numpy```list is much faster than the normal list.

| ncalls | tottime      | percall      | cumtime      | percall      | filename:lineno(function)         |
| ------ | ------------ | ------------ | ------------ | ------------ | --------------------------------- |
| 1      | 0.02827      | 0.02827      | 0.02827      | 0.02827      | list_array.py:4(double_list)      |
| 1      | **0.001303** | **0.001303** | **0.002048** | **0.002048** | **list_array.py:9(double_array)** |

## 1.2 Sets and Tuples

| **Feature**                | **Sets**                              | **Tuples**                  |
| -------------------------- | ------------------------------------- | --------------------------- |
| *Mutability*               | Mutable                               | Immutable                   |
| *Order*                    | Unordered                             | Ordered                     |
| *Duplicates Allowed*       | No                                    | Yes                         |
| *Memory Usage*             | Medium                                | Very low                    |
| *Membership Checking*      | Very fast (O(1))                      | Slow (O(n))                 |
| *Use Case*                 | Fast lookup, ensuring unique elements | Fixed collections of values |
| *Indexing*                 | Not supported                         | Supported                   |
| *Typical Operations*       | Union, intersection, difference       | Slicing, unpacking          |
| *Performance on Iteration* | Fast                                  | Fast                        |

### Technical comparison

```python
import random


def search(items, collection):
    count = 0
    for i in items:
        if i in collection:
            count += 1
    return count

@profile
def main():
    SIZE = 1_000_000

    big_list = list(range(SIZE))
    big_set = set(big_list)
    big_tuple = tuple(big_list)

    items_to_find = [random.randint(0, SIZE) for _ in range(1000)]

    search(items_to_find, big_list)
    search(items_to_find, big_set)
    search(items_to_find, big_tuple)


main()
```


```bash
❯ python -m memory_profiler set_tuple.py
Filename: set_tuple.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    12   22.234 MiB   22.234 MiB           1   @profile
    13                                         def main():
    14   22.234 MiB    0.000 MiB           1       SIZE = 1_000_000
    15                                         
    16   60.500 MiB   38.266 MiB           1       big_list = list(range(SIZE))
    17  123.062 MiB   62.562 MiB           1       big_set = set(big_list)
    18  130.703 MiB    7.641 MiB           1       big_tuple = tuple(big_list)
    19                                         
    20  130.734 MiB    0.031 MiB        1001       items_to_find = [random.randint(0, SIZE) for _ in range(1000)]
    21                                         
    22  130.734 MiB    0.000 MiB           1       search(items_to_find, big_list)
    23  130.734 MiB    0.000 MiB           1       search(items_to_find, big_set)
    24  130.734 MiB    0.000 MiB           1       search(items_to_find, big_tuple)
```

- List takes more memory followed by Set.
- Touples are incredibly memory efficient in comparison.

```bash
❯ kernprof -lv set_tuple.py
Wrote profile results to set_tuple.py.lprof
Timer unit: 1e-06 s

Total time: 5.36034 s
File: set_tuple.py
Function: main at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           @profile
    13                                           def main():
    14         1          0.0      0.0      0.0      SIZE = 1_000_000
    15                                           
    16         1       9488.0   9488.0      0.2      big_list = list(range(SIZE))
    17         1      14646.0  14646.0      0.3      big_set = set(big_list)
    18         1       1844.0   1844.0      0.0      big_tuple = tuple(big_list)
    19                                           
    20      1001       1473.0      1.5      0.0      items_to_find = [random.randint(0, SIZE) for _ in range(1000)]
    21                                           
    22         1    2819156.0    3e+06     52.6      search(items_to_find, big_list)
    23         1        376.0    376.0      0.0      search(items_to_find, big_set)
    24         1    2513361.0    3e+06     46.9      search(items_to_find, big_tuple)
```

- Searching lists and tuples takes more time.
- Searching sets is insanely fast, near 0.

- **Conclusion**
	- Sets are the fastest.
	- Tuples consume the least memory.
	- Lists offer the most flexibility.

## 1.3 Queues and Deques

| **Feature**          | **Queues**                     | **Deques**                                                 |
| -------------------- | ------------------------------ | ---------------------------------------------------------- |
| *Module*               | `queue`                        | `collections`                                              |
| *Type*                 | Simple queue                   | Double-ended queue                                         |
| *Access Pattern*       | FIFO (First-In, First-Out)     | FIFO (First-In, First-Out) <br/> LIFO (Last-In, First-Out) |
| *Multithreading*       | Specialized for multithreading | Multithreading support                                     |
| *Supported Operations* | Few operations                 | Many operations                                            |
| *Index Access*         | Slow (O(n))                    | Fast (O(1))                                                |
| *Append/Pop End*       | Fast                           | Fast                                                       |
| *Append/Pop Start*     | Fast                           | Fast                                                       |
| *Special Capabilities* | -                              | Efficient operations at both ends                          |

### Technical comparison

```python
from collections import deque


@profile
def main():
    SIZE = 100_000

    big_list = list(range(SIZE))
    big_queue = deque(big_list)

    while big_list:
        big_list.pop()
    while big_queue:
        big_queue.pop()

    big_list = list(range(SIZE))
    big_queue = deque(big_list)

    while big_list:
        big_list.pop(0)
    while big_queue:
        big_queue.popleft()


main()
```

```bash
❯ kernprof -lv deque.py
Wrote profile results to deque.py.lprof
Timer unit: 1e-06 s

Total time: 0.900465 s
File: deque.py
Function: main at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           @profile
     5                                           def main():
     6         1          0.0      0.0      0.0      SIZE = 100_000
     7                                           
     8         1       1022.0   1022.0      0.1      big_list = list(range(SIZE))
     9         1        408.0    408.0      0.0      big_queue = deque(big_list)
    10                                           
    11    100001      12445.0      0.1      1.4      while big_list:
    12    100000      10154.0      0.1      1.1          big_list.pop()
    13    100001      12638.0      0.1      1.4      while big_queue:
    14    100000      11141.0      0.1      1.2          big_queue.pop()
    15                                           
    16         1        953.0    953.0      0.1      big_list = list(range(SIZE))
    17         1        401.0    401.0      0.0      big_queue = deque(big_list)
    18                                           
    19    100001      13389.0      0.1      1.5      while big_list:
    20    100000     813161.0      8.1     90.3          big_list.pop(0)
    21    100001      14310.0      0.1      1.6      while big_queue:
    22    100000      10443.0      0.1      1.2          big_queue.popleft()
```

- **Conclusion**
	- Removing items from the left of the list creates a bottleneck.
		- ```90.3          big_list.pop(0)```
	- Avoid pop-append operations at the start of lists.

## 1.4 Dictionaries

| **Aspect**               | **Dictionaries**                                  |
| ------------------------ | ------------------------------------------------- |
| *What they store*        | Key-value pairs                                   |
| *Mutability*             | Mutable (you can add, remove, update pairs)       |
| *Keys*                   | Must be unique and hashable                       |
| *Value types*            | Any type                                          |
| *Access pattern*         | Via keys (like a lookup table)                    |
| *Performance*            | Very fast O(1) for get/set/delete in most cases   |
| *Worst-case performance* | Rarely O(n)                                       |
| *Comparison to lists*    | Faster membership checks, but less flexible types |
| *Memory usage*           | Higher than lists (stores hashes and pairs)       |
| *Common use cases*       | Fast lookups, mappings, indexing by unique keys   |

### Technical comparison

1.  **Appending items**

```python
@profile
def main():
    SIZE = 100_000

    big_list = []
    big_dict = {}

    for i in range(SIZE):
        big_list.append([i, i * 2, i * i])
        big_dict[i] = [i, i * 2, i * i]

main()
```

```bash
❯ kernprof -lv dictionary.py
Wrote profile results to dictionary.py.lprof
Timer unit: 1e-06 s

Total time: 0.06543 s
File: dictionary.py
Function: main at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def main():
     3         1          0.0      0.0      0.0      SIZE = 100_000
     4                                           
     5         1          0.0      0.0      0.0      big_list = []
     6         1          0.0      0.0      0.0      big_dict = {}
     7                                           
     8    100001      13103.0      0.1     20.0      for i in range(SIZE):
     9    100000      15864.0      0.2     24.2          big_list.append([i, i * 2, i * i])
    10    100000      36463.0      0.4     55.7          big_dict[i] = [i, i * 2, i * i]
```

- Dictionary is clearly faster than the list (~ x2).

2. **Searching indexes**

```python
import random


def search_list(big_list, items):
    count = 0
    for item in items:
        if item in big_list:
            for order in big_list:
                if item == order[0]:
                    count += 1
    return count


def search_dict(big_dict, items):
    count = 0
    for item in items:
        if item in big_dict:
            count += 1
    return count


@profile
def main():
    SIZE = 100_000

    big_list = []
    big_dict = {}

    for i in range(SIZE):
        big_list.append([i, i * 2, i * i])
        big_dict[i] = [i, i * 2, i * i]

    orders_to_search = [random.randint(0, SIZE) for _ in range(1000)]
    search_list(big_list, orders_to_search)
    search_dict(big_dict, orders_to_search)


main()
```


```bash
❯ kernprof -lv dictionary.py
Wrote profile results to dictionary.py.lprof
Timer unit: 1e-06 s

Total time: 1.01097 s
File: dictionary.py
Function: main at line 22

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    22                                           @profile
    23                                           def main():
    24         1          1.0      1.0      0.0      SIZE = 100_000
    25                                           
    26         1          1.0      1.0      0.0      big_list = []
    27         1          0.0      0.0      0.0      big_dict = {}
    28                                           
    29    100001      13101.0      0.1      1.3      for i in range(SIZE):
    30    100000      16171.0      0.2      1.6          big_list.append([i, i * 2, i * i])
    31    100000      39132.0      0.4      3.9          big_dict[i] = [i, i * 2, i * i]
    32                                           
    33      1001       1459.0      1.5      0.1      orders_to_search = [random.randint(0, SIZE) for _ in range(1000)]
    34         1     940358.0 940358.0     93.0      search_list(big_list, orders_to_search)
    35         1        747.0    747.0      0.1      search_dict(big_dict, orders_to_search)

```

- **Conclusion**
	- Searching a dictionary is much faster.

## 1.5 Dictionaries, Dataclasses, and NamedTuples

| **Feature**             | **Named Tuples**                    | **Data Classes**                                              |
| ----------------------- | ----------------------------------- | ------------------------------------------------------------- |
| *Mutability*              | Immutable                           | Mutable by default (can be made immutable with `frozen=True`) |
| *Syntax*                  | `collections.namedtuple()`          | `@dataclass` decorator                                        |
| *Data Access Performance* | Very fast                           | Extremely fast                                                |
| *Memory Efficiency*       | More lightweight, memory-efficient  | Slightly heavier                                              |
| *Type Annotations*        | Limited                             | Full support                                                  |
| *Readability*             | Good readability with named fields  | Excellent readability with class-like syntax                  |
| *Class Features*          | Fewer features (not actual classes) | Full class features                                           |
| *Use Case*                | Read-only data, lightweight records | Rich data models with more flexibility                        |

### Technical comparison

- Measure creation time with `timeit`.

```bash
❯ python -m timeit '{"order_id": 1}'
10000000 loops, best of 5: 28.5 nsec per loop

# This should not happen before 3.10
❯ python -m timeit -s 'from collections import namedtuple; Order=namedtuple("Order", "order_id"); Order(1)'
100000000 loops, best of 5: 3.87 nsec per loop

❯ python -m timeit -s """
dquote> from dataclasses import dataclass
dquote> @dataclass
dquote> class Order:
dquote>     order_id: int
dquote> """ 'Order(1)'
2000000 loops, best of 5: 109 nsec per loop
```

- Measure the time to access order_id.

```bash
❯ python -m timeit -s 'order={"order_id": 1}' 'order["order_id"]'
20000000 loops, best of 5: 12.5 nsec per loop

❯ python -m timeit  'from collections import namedtuple; Order=namedtuple("Order", "order_id"); order=Order(1)' 'order.order_id'
20000 loops, best of 5: 18.9 usec per loop

❯ python -m timeit -s """
from dataclasses import dataclass
@dataclass
class Order:
    order_id: int
order=Order(1)""" 'order.order_id'
50000000 loops, best of 5: 6.06 nsec per loop
```

- **Conclusion**
	- Data classes are the fastest for data access, even than dictionaries.