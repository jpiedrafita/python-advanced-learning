09-07-2025 10:52

Labels:  [[Dominio Técnico]] [[programación]] #Python 

---
# Index

- [Big O Notation](#big-o-notation)
- [Summary](#summary)
- [1. Measuring Performance](1-measuring-performance.md)
	- [1.1 Lists and Arrays](1-measuring-performance.md#11-lists-and-arrays)
	- [1.2 Sets and Tuples](1-measuring-performance.md#12-sets-and-tuples)
	- [1.3 Queues and Deques](1-measuring-performance.md#13-queues-and-deques)
	- [1.4 Dictionaries](1-measuring-performance.md#14-dictionaries)
	- [1.5 Dictionaries, Dataclasses, and NamedTuples](1-measuring-performance.md#15-dictionaries-dataclasses-and-namedtuples)
- [2. Optimizing Python Code](2-optimizing-python-code.md)
	- [2.1 For vs. List comprehensions](2-optimizing-python-code.md#21-for-vs-list-comprehensions)
	- [2.2 Generator Expressions vs. List Comprehensions](2-optimizing-python-code.md#22-generator-expressions-vs-list-comprehensions)
	- [2.3 Fast Concatenation of Strings](2-optimizing-python-code.md#23-fast-concatenation-of-strings)
	- [2.4 Permission or Forgiveness](2-optimizing-python-code.md#24-permission-or-forgiveness)
	- [2.5 Python Functions](2-optimizing-python-code.md#25-python-functions)
	- [2.6 Optimizing Numerical Calculations](2-optimizing-python-code.md#26-optmizing-numerical-calculations)
	- [2.7 Interpreter-based Optimizations](2-optimizing-python-code.md#27-interpreter-based-optimizations)
	- [2.8 Risky Optimizations](2-optimizing-python-code.md#28-risky-optimizations)
- [3. Using More Threads](3-using-more-threads.md)
	- [3.1 What Are Threads?](3-using-more-threads.md#31-what-are-threads)
	- [3.2 Challenges of Working with Threads](3-using-more-threads.md#32-challenges-of-working-with-threads)
	- [3.3 When to Use Multithreading](3-using-more-threads.md#33-when-to-use-multithreading)
- [4. Using Asynchronous Code](4-using-asynchronous-code.md)
	- [4.1 Asynchronous Code](4-using-asynchronous-code.md#41-asynchronous-code)
	- [4.2 Challenges of Working With asyncio](4-using-asynchronous-code.md#42-challenges-of-working-with-asycio)
	- [4.3 When to Use asyncio](4-using-asynchronous-code.md#43-when-to-use-asyncio)
- [5. Using More Processes](5-using-more-processes.md)
	- [5.1 Process-based Parallelism](5-using-more-processes.md#51-process-based-parallelism)
	- [5.2 Processes Communication](5-using-more-processes.md#52-processes-communication)
	- [5.3 When to Use More Processes](5-using-more-processes.md#53-when-to-use-more-processes)
	- [5.4 Scaling From One to More Machines](5-using-more-processes.md#54-scaling-fron-one-to-more-machines)


# Big O Notation

[Big_O_Notation](https://en.wikipedia.org/wiki/Big_O_notation)

**Big O notation** is a mathematical way to describe how the runtime or memory requirements of an algorithm grow relative to the size of the input data. It expresses the _upper bound_ of complexity, helping you understand the worst-case performance as inputs get large.


```mermaid
flowchart LR
    A["O(n²)"] --> B["O(n log n)"] --> C["O(n)"] --> D["O(log n)"]

    VerySlow([Very slow])
    VeryFast([Very fast])

    VerySlow -.-> A
    D -.-> VeryFast

    classDef slow fill:#fcd34d,stroke:#000,stroke-width:1px
    classDef fast fill:#a78bfa,stroke:#000,stroke-width:1px

    class A,B,C slow
    class D fast
```

- **O(1)**: Constant

```python
my_list = [3, 11, 25]
double_top = amoutns[0] * 2
```

- **O(n)**: Linear

```python
sum = 0
for amount in amounts:
	sum += amount
```

- **O(Log n)**: logarithmic
	- Binary search

- **O(N^2)**: Quadratic
	- Nested loops

```python
for i in my_list:
    for j in my_list:
        print(i, j)
```

# Summary

| **Estructura** | **Ordenada** | **Mutable** | **Únicos**    | **Claves/Valores** | **Complejidad Acceso** | **Complejidad Búsqueda** | **Memoria** | **Notas destacadas**                            |
| -------------- | ------------ | ----------- | ------------- | ------------------ | ---------------------- | ------------------------ | ----------- | ----------------------------------------------- |
| **List**       | Sí           | Sí          | No            | No                 | O(1)                   | O(n)                     | Alta        | Flexible, operaciones de append rápidas         |
| **Tuple**      | Sí           | No          | No            | No                 | O(1)                   | O(n)                     | Baja        | Inmutable, muy eficiente en memoria             |
| **Set**        | No           | Sí          | Sí            | No                 | –                      | O(1)                     | Media       | Miembros únicos, búsqueda ultra rápida          |
| **Dict**       | No           | Sí          | Claves únicas | Sí                 | O(1) (por clave)       | O(1) (por clave)         | Media       | Claves hashables, muy usado en Python           |
| **Deque**      | Sí           | Sí          | No            | No                 | O(1)                   | O(n)                     | Media       | Acceso rápido en ambos extremos                 |
| **NamedTuple** | Sí           | No          | No            | No                 | O(1)                   | O(n)                     | Muy baja    | Campos por nombre, inmutable                    |
| **DataClass**  | Sí           | Sí (*)      | No            | No                 | O(1)                   | O(n)                     | Media       | Campos con tipos, opcionalmente inmutable       |
| **Array**      | Sí           | Sí          | No            | No                 | O(1)                   | O(n)                     | Baja        | `array` módulo o NumPy, optimizado para números |

**Notes:**
- (\*) `DataClas` can be made immutable with `frozen=True`.
- Search complexity is O(n) except for special cases (for example, indices in NumPy).
- In `Set`, index access complexity does not apply because there is no order or index.
- `Array` refers both to the standard `array` module (very compact) and to `NumPy`







