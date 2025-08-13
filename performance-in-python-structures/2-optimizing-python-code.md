# 2. Optimizing Python Code

## 2.1 For vs. List comprehensions

A typical Python application often processes collections of items in three steps:
1. **Prepare Input Data**: A collection of items (list, set, etc.) ready to process.
2. **Process Items**: Transform, filter, or compute on the collection.    
3. **Return Output**: Produce a new collection with the processed data.

There are two main approaches for this: **for loops** and **list comprehensions**.

|**Aspect**|**For Loop**|**List Comprehension**|
|---|---|---|
|_Flexibility_|High (can include complex logic, multiple statements)|Low (only used to create new collections)|
|_Conciseness_|Verbose, more lines|Very concise, fewer lines|
|_Performance_|Slower for simple transformations|Faster, optimized internally|
|_Use Cases_|Complex workflows, external API calls|Simple filtering and transformation|
|_Supported Collections_|Lists, but can also be adapted to sets and dicts|Lists, sets, and dictionary comprehensions|

```Python
orders = [120, 150, 50]

# for loop
fl = []
for o in orders:
	if o > 100:
		fl.append[o * 2]

# list comprehension

lc = [o * 2 for o in orders if o > 100]
```

### Technical comparison

```python
import random


def loop(orders):
    result = []
    for amount in orders:
        if amount > 50:
            result.append(2 * amount)
    return result


def comprehension(orders):
    return [2 * amount for amount in orders if amount > 50]


@profile
def main():
    orders = [random.randint(0, 100) for _ in range(100_000)]
    loop(orders)
    comprehension(orders)


main()
```


```bash
❯ kernprof -lv comprehension.py
Wrote profile results to comprehension.py.lprof
Timer unit: 1e-06 s

Total time: 0.151899 s
File: comprehension.py
Function: main at line 16

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    16                                           @profile
    17                                           def main():
    18    100001     133672.0      1.3     88.0      orders = [random.randint(0, 100) for _ in range(100_000)]
    19         1      10487.0  10487.0      6.9      loop(orders)
    20         1       7740.0   7740.0      5.1      comprehension(orders)
```

- **Conclusion**
	- Comprehension list is more concise and faster (`5.1`) than for loop (`6.9`).
## 2.2 Generator Expressions vs. List Comprehensions

- Generator expressions are a _lazy_ alternative to list comprehensions. Instead of creating all items up front, they produce items _one by one_ when requested.

|**Aspect**|**List Comprehensions**|**Generator Expressions**|
|---|---|---|
|_Syntax_|Use **square brackets** [ ]|Use **parentheses** ( )|
|_Evaluation_|Eager (creates all items immediately)|Lazy (produces items on demand)|
|_Iteration_|Can iterate multiple times|Can iterate only **once**|
|_Random Access_|Supports random access (list[5])|No random access (only next())|
|_Memory Consumption_|Higher (stores all items in memory)|Lower (items generated as needed)|
|_Performance (Creation)_|Slower (pre-computes all elements)|Faster (only prepares the generator)|
|_Performance (Iteration)_|Faster (items already computed)|Slower (must compute items during iteration)|
|_Use Cases_|When all items are needed and reused multiple times|When processing large datasets or streaming processing|
```python
orders = [10, 60, 150, 200]

# List comprehension
comprehension = [order * 2 for order in orders if order > 100]

# Generator expression
generator = (order * 2 for order in orders if order > 100)

# Consuming the generator
total_sum = sum(generator)
```

>[!INFO] After calling `sum(generator)`, the generator is exhausted and cannot be reused.

- **Creation Time**:
	- List comprehension takes more time because it immediately builds the list.   
    - Generator expression is faster as it only sets up the generator object.
- **Access Time**:
    - Summing the list comprehension is faster since the items already exist.
    - Summing the generator expression is slower since each item must be calculated during iteration.
- **Memory Usage**:
    - List comprehension uses significantly more memory.
    - Generator expression is much more memory-efficient.

- Use **generator expressions** when:
    - Working with large datasets.
    - You don’t need to access items multiple times.
    - You care about memory usage.
    
- Use **list comprehensions** when:
    - You need random access to the items.
    - You will iterate multiple times over the results.
    - The dataset fits comfortably in memory.

### Technical comparison

```python
import random


@profile
def main():
    orders = [random.randint(0, 100) for _ in range(100_000)]

    comprehension = [2 * amount for amount in orders if amount > 50]
    generator = (2 * amount for amount in orders if amount > 50)

    sum(comprehension)
    sum(generator)

main()
```

```bash
❯ kernprof -lv generator.py
Wrote profile results to generator.py.lprof
Timer unit: 1e-06 s

Total time: 0.16067 s
File: generator.py
Function: main at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           @profile
     5                                           def main():
     6    100001     132101.0      1.3     82.2      orders = [random.randint(0, 100) for _ in range(100_000)]
     7                                           
     8    100001      16062.0      0.2     10.0      comprehension = [2 * amount for amount in orders if amount > 50]
     9         1          1.0      1.0      0.0      generator = (2 * amount for amount in orders if amount > 50)
    10                                           
    11         1        112.0    112.0      0.1      sum(comprehension)
    12         1      12394.0  12394.0      7.7      sum(generator)
```

```bash
❯ python -m memory_profiler generator.py
Filename: generator.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     4   22.422 MiB   22.422 MiB           1   @profile
     5                                         def main():
     6   23.156 MiB    0.734 MiB      100001       orders = [random.randint(0, 100) for _ in range(100_000)]
     7                                         
     8   23.359 MiB    0.203 MiB      100001       comprehension = [2 * amount for amount in orders if amount > 50]
     9   23.391 MiB    0.031 MiB      149708       generator = (2 * amount for amount in orders if amount > 50)
    10                                         
    11   23.359 MiB    0.000 MiB           1       sum(comprehension)
    12   23.391 MiB    0.000 MiB           1       sum(generator)
```


- **Conclusion**
	- Comprehension (`10.0`) is much slower than generator (`0.0`) because comprehension creates a full list and generator uses a lazy approach.
	- For the sum, the comprehension is faster (`0.1`) because the values are already in place, and for the generator (`6.8`), the calculations were delayed.
	- List comprehension clearly needed more memory than generator.

## 2.3 Fast Concatenation of Strings

Two Main Scenarios

1. **Small, fixed number of strings**:  Performance impact is usually negligible.
2. **Large, variable number of strings**: Performance impact is significant.

**Aproaches:**

|**Approach**|**Description**|**Performance**|**Scalability**|**Friendliness**|
|---|---|---|---|---|
|+ Operator|Intuitive and simple. Adds strings together by recreating new strings each time.|Slow|Scales poorly with many strings|Very friendly|
|f-Strings|Good for formatting a few known variables.|Fast|Not scalable (must know all pieces)|Friendly|
|join() Method|Concatenates many strings efficiently using a separator.|Very fast|Highly scalable|Less friendly / verbose|
**Trade-offs:**

|**Aspect**|**+ Operator**|**f-Strings**|**join()**|
|---|---|---|---|
|_Performance_|Slow for many strings|Fast for few strings|Very fast for many strings|
|_Memory Efficiency_|Poor (creates many intermediates)|Good|Excellent|
|_Ease of Use_|Easiest to read|Easy|Less intuitive|
|_Scalability_|Bad with many items|Bad with many items|Excellent|
```python
items = ['hello ', 'world']

items[0] + items[1]
f'{items[0]}{items[1]}'
''.join(items)
```

### Technical comparison

```python
import random


@profile
def main():
    orders = [str(random.randint(0, 100)) for _ in range(50_000)]

    report = ""
    for o in orders:
        report += o

    "".join(orders)
```

```bash
❯ kernprof -lv concatenation.py
Wrote profile results to concatenation.py.lprof
Timer unit: 1e-06 s

Total time: 0.080244 s
File: concatenation.py
Function: main at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           @profile
     5                                           def main():
     6     50001      67539.0      1.4     84.2      orders = [str(random.randint(0, 100)) for _ in range(50_000)]
     7                                           
     8         1          0.0      0.0      0.0      report = ""
     9     50001       5975.0      0.1      7.4      for o in orders:
    10     50000       6433.0      0.1      8.0          report += o
    11                                           
    12         1        297.0    297.0      0.4      "".join(orders)                                           "".join(orders)

❯ python -m memory_profiler concatenation.py
Filename: concatenation.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     4   21.969 MiB   21.969 MiB           1   @profile
     5                                         def main():
     6   24.781 MiB    2.812 MiB       50001       orders = [str(random.randint(0, 100)) for _ in range(50_000)]
     7                                         
     8   24.781 MiB    0.000 MiB           1       report = ""
     9   24.812 MiB    0.000 MiB       50001       for o in orders:
    10   24.812 MiB    0.031 MiB       50000           report += o
    11                                         
    12   24.812 MiB    0.000 MiB           1       "".join(orders)

```

- **Conclusion**: 
	- join (`0.4`) is much faster than + (`8.0`).
	- join is more memory efficient

## 2.4 Permission or Forgiveness

- In real-world applications, problems are inevitable.
	- A file is missing.
	- A class field is absent.
	- An integer is replaced by a string.

- **Permission**: Also called _Look Before You Leap_. Check if everything is valid _before_ doing the action.
- **Forgiveness**: Also called _Easier to Ask Forgiveness_. Try the operation and handle exceptions if needed.

| **Aspect**                    | **Permission**                                                        | **Forgiveness**                                                                    |
| ----------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Description**               | Use if statements to check all conditions in advance.                 | Use try/except to catch errors as they happen.                                     |
| **Example**                   | if os.path.exists(filepath): ...                                      | try: ... except FileNotFoundError: ...                                             |
| **Pros**                      | - Clear intention- Avoids exceptions                                  | - Concise- Avoids race conditions- Popular in Python                               |
| **Cons**                      | - Verbose- Potential race conditions (e.g., file deleted after check) | - Slower if exceptions occur often                                                 |
| **Performance (Few Errors)**  | Slower (many checks even when data is valid)                          | Faster (rare exceptions)                                                           |
| **Performance (Many Errors)** | Faster (avoids many exceptions)                                       | Slower (many exceptions trigger costly handling)                                   |
| **Recommendations**           | Use when:- Errors are common- You expect lots of invalid data         | Use when:- Errors are rare- You want clean and concise code- Avoid race conditions |
```python
class Order:
	order_id = 5

new_order = Order()

# Permission
if hasatrr(new_order, 'order_id'):
	print(new_order.order_id)

# Forgiveness
try:
	print(new_order.order_id)
except AttributeError as attribue:
	print(attribute)
```

### Technical comparison

```python
import random


def permission(orders):
    result = []
    for amount in orders:
        if type(amount) == int:
            if amount > 50:
                result.append(2 * amount)
    return result


def forgiveness(orders):
    result = []
    for amount in orders:
        try:
            if amount > 50:
                result.append(2 * amount)
        except TypeError:
            pass
    return result


@profile
def main():
    orders = [random.randint(0, 100) for _ in range(100_000)]

    for i in range(10):
        orders[i] = "bad data"

    permission(orders)
    forgiveness(orders)

    for i in range(90_000):
        orders[i] = "bad data"

    permission(orders)
    forgiveness(orders)


main()
```

```bash
❯ kernprof -lv permission.py
Wrote profile results to permission.py.lprof
Timer unit: 1e-06 s

Total time: 0.233434 s
File: permission.py
Function: main at line 24

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def main():
    26    100001     131159.0      1.3     56.2      orders = [random.randint(0, 100) for _ in range(100_000)]
    27                                           
    28        11          4.0      0.4      0.0      for i in range(10):
    29        10          2.0      0.2      0.0          orders[i] = "bad data"
    30                                           
    31         1      15905.0  15905.0      6.8      permission(orders)
    32         1      13245.0  13245.0      5.7      forgiveness(orders)
    33                                           
    34     90001      12076.0      0.1      5.2      for i in range(90_000):
    35     90000       9388.0      0.1      4.0          orders[i] = "bad data"
    36                                           
    37         1      10430.0  10430.0      4.5      permission(orders)
    38         1      41225.0  41225.0     17.7      forgiveness(orders)
```

- **Conclusion**: 
	- With few errors, forgiveness (`5.7`) is faster than permission (`6.8`).
	- With a lot of errors, permission (`4.5`) is faster than forgiveness (`17.7`).

## 2.5 Python Functions

- **Regular functions**: Defined with def, have names, reusable in many places.
- **Lambda functions**: Anonymous one-liners, defined with lambda.

|**Aspect**|**Self-sufficient Approach**|**Calling Other Functions**|
|---|---|---|
|**Performance**|Fastest (no call overhead)|Slightly slower (function call overhead)|
|**Code Reuse**|Low (logic may be duplicated)|High (logic is reusable)|
|**Maintainability**|Lower (bigger functions harder to test and understand)|Higher (cleaner separation)|
|**Readability**|Lower (all logic in one place)|Higher (split into smaller pieces)|
|**Performance Impact**|Significant only if the function is called _many times_ in hot loops.|Negligible for occasional calls.|

```python
import random

# Self-sufficient approach
orders = [random.randint(0, 100) for _ in range(100_000)]

# Using an external function
def get_random_integer():
    return random.randint(0, 100)

orders = [get_random_integer() for _ in range(100_000)]

# Using a lambda function
get_random_lambda = lambda: random.randint(0, 100)
orders = [get_random_lambda() for _ in range(100_000)]
```

### Technical comparison


```python
import random


def get_random_integer():
    return random.randint(0, 100)


@profile
def main():
    [random.randint(0, 100) for _ in range(100_000)]
    [get_random_integer() for _ in range(100_000)]
    [(lambda: random.randint(0, 100))() for _ in range(100_000)]


main()
```

```bash
❯ kernprof -lv functions.py
Wrote profile results to functions.py.lprof
Timer unit: 1e-06 s

Total time: 0.442127 s
File: functions.py
Function: main at line 8

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           @profile
     9                                           def main():
    10    100001     135064.0      1.4     30.5      [random.randint(0, 100) for _ in range(100_000)]
    11    100001     152158.0      1.5     34.4      [get_random_integer() for _ in range(100_000)]
    12    100001     154905.0      1.5     35.0      [(lambda: random.randint(0, 100))() for _ in range(100_000)]
```

- **Conclusion**:
	- A self-sufficient approach is the fastest, but only slightly faster.
	- The ordinary function has almost the same performance as the lambda.

## 2.6 Optmizing Numerical Calculations

- Numerical calculations are a **critical part of many Python applications**, including:
	- Basic arithmetic (addition, multiplication)
	- Vector operations and matrix
    - Statistical calculations (mean, standard deviation)
    - Machine learning workflows (data cleaning, model updates)

Popular tools:
- **NumPy**: 
	- The unofficial standard for scientific computing.
	- High-performance arrays.
	- Many C-optimized functions.
	- Efficient contiguous memory.
	- Used in data science, ML, visualization
	- Prerequisite for tools like Matplotlib.
- **Pandas**:
	- Built on top of NumPy.
	- Excellent for tabular data manipulation.
	- Handles messy real-world data.
	- Reads/writes CSV, Excel, databases.
	- High-performance due to NumPy internals.

### Technical comparison

```python
import random
import numpy as np


def loop_approach(orders):
    result = 0
    for o in orders:
        result += o * o
    return result


def numpy_approach(orders):
    numpy_orders = np.array(orders)
    return np.sum(numpy_orders * numpy_orders)


@profile
def main():
    orders = [random.randint(0, 100) for _ in range(100_000)]
    loop_approach(orders)
    numpy_approach(orders)


main()
```

```bash
❯ kernprof -lv numerical.py
Wrote profile results to numerical.py.lprof
Timer unit: 1e-06 s

Total time: 0.143984 s
File: numerical.py
Function: main at line 17

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    17                                           @profile
    18                                           def main():
    19    100001     131054.0      1.3     91.0      orders = [random.randint(0, 100) for _ in range(100_000)]
    20         1       9997.0   9997.0      6.9      loop_approach(orders)
    21         1       2933.0   2933.0      2.0      numpy_approach(orders)

```

- **Conclusion**:
	- **numpy** approach is faster than loop approach, but requires more lines of code.
	- Great performance for big amount of data.

## 2.7 Interpreter-based Optimizations

- A **Python interpreter** transforms your Python code into instructions that hardware can execute.

- **CPython**:
	- The default and most popular interpreter.
	- Written in C.
	- Reference implementation.
	- Highly portable.

Alternative interpreters:

- **PyPy**:
	- Uses a Just-In-Time (JIT) compiler to convert Python to machine code at runtime.
	- Often significantly faster.
	- Highly compatible with CPython.
- **Cython**:
	- Compiles Python code to efficient C code.
	- Adds extensions (C types, C function calls).
	- Requires extra steps; code won’t run unchanged on CPython.
- **Jython**: 
	- Implemented in Java.
	- Integrates with Java code.
	- Lags behind CPython in features.
- **Pyston**:
	- Fast and increasingly compatible.
	- Aims to be a drop-in CPython replacement with better performance.
### Technical comparison

```bash
brew install pypy3 #mac
sudo apt install pypy3 #ubuntu
```

```bash
❯ python3 sum_loop.py
Duration:  2.83 seconds

❯ pypy3 sum_loop.py
Duration:  0.06 seconds
```

- **Conclusion**:
	- **PyPy** is significantly more efficient.

## 2.8 Risky Optimizations

|**Risk**|**Description**|**How to Mitigate**|
|---|---|---|
|**Reduced Readability**|Code becomes harder to read, understand, and maintain.|Use comments, clear variable names, and documentation.|
|**New Bugs Introduced**|Refactoring or optimization introduces regressions.|Use regression tests to catch issues early.|
|**Small Performance Gains vs. Effort**|A lot of work may result in negligible speed improvements.|Use profilers and measure before optimizing.|
Examples of Risky Optimizations:

1. **Large Self-Sufficient Functions**
    - Avoid function calls to gain slight speed improvements.
    - _Drawback:_ Big, monolithic functions are hard to test and maintain.    
2. **Alternative Python Interpreters**
    - PyPy or other interpreters can be faster.
    - _Drawback:_ Compatibility issues with some libraries.
3. **Multiple Assignments**
    - Concise syntax for assigning multiple variables in one line.
    - _Drawback:_ Less clear, harder to read for beginners.

### Technical comparison


```python
import random
import numpy as np


def multiple_assignments(order):
    order_subtotal, order_tax, order_shipping = order

def individual_assignments(order):
    order_subtotal = order[0]
    order_tax = order[1]
    order_shipping = order[2]

@profile
def main():
    orders = [(random.randint(0, 100),
               random.randint(0, 100),
               random.randint(0, 100)) for _ in range(100_000)]
    
    for o in orders:
        multiple_assignments(o)
        individual_assignments(o)


main()
```


```bash
❯ kernprof -lv assignments.py
Wrote profile results to assignments.py.lprof
Timer unit: 1e-06 s

Total time: 0.468941 s
File: assignments.py
Function: main at line 15

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    15                                           @profile
    16                                           def main():
    17    100001      13021.0      0.1      2.8      orders = [
    18    100000     378853.0      3.8     80.8          (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    19    100001      10184.0      0.1      2.2          for _ in range(100_000)
    20                                               ]
    21                                           
    22    100001      13238.0      0.1      2.8      for o in orders:
    23    100000      21975.0      0.2      4.7          multiple_assignments(o)
    24    100000      31670.0      0.3      6.8          individual_assignments(o)
```

- **Conclusion**:
	- **multiple_assinments** (`4.7`) is slightly faster than **individual_assignments** (`6.8`)
	- The performance gain is minimal and the code is harder to read, so this is a **risky optimization**.