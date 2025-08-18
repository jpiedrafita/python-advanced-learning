# Python Learning

This repository contains complete, self-contained Python courses, each organized in its own directory.  
All materials are in Markdown format and include code examples, diagrams, and conceptual explanations.

---

1. [Design Patterns in Python 3](./design-patterns-in-python3/design-patterns-in-python3.md)
2. [Python Collections](./pyhton-collections/python-collections.md)
3. [Python Requests Playbook](./python-requests-playbook/python-requests-playbook.md)
4. [Working with Databases in Python](./working-with-databases-in-python/working-with-databases-in-python.md)

---
# Courses

## 1. Design Patterns in Python 3

This course contains a complete and structured walkthrough of **design patterns implemented in Python 3**, based on modern practices and educational resources.

The goal is to not only understand the *theoretical structure* of each pattern, but also explore **realistic Python implementations** with code examples, diagrams, and reflections.

### Structure

The course is divided into three main sections:

1. **Creational Patterns**  
   Focused on object creation and instantiation control.

2. **Structural Patterns**  
   Concerned with object composition and interface simplification.

3. **Behavioral Patterns**  
   Related to object interaction, responsibility, and control flow.

Each pattern is developed in a **dedicated note**, including:

- A short conceptual overview  
- A diagram of its structure (Mermaid or code-based)  
- A Python implementation (following best practices)  
- Notes on applicability and pros/cons

 🔗 [Go to course](./design-patterns-in-python3/design-patterns-in-python3)

---
## 2. Python Collections

This course covers Python's `collections` module and advanced data structures for efficient programming.

**Course Structure:**
- **Module 1**: Utilizing Built-in Containers - `defaultdict`
- **Module 2**: Improving Efficiency with Advanced Dictionaries - `ChainMap`
- **Module 3**: Using Specialized Collection Classes - `deque`, `namedtuple`, `Counter`
- **Module 4**: Customizing Built-in Data Types - `UserString`, `UserList`, `UserDict`

**Key Topics:**
- Performance optimization with specialized containers
- Advanced dictionary patterns and multi-level configurations
- Memory-efficient data structures and algorithms
- Custom data type implementations and inheritance patterns

## 3. Python Requests Playbook

This course provides a complete and practical guide to using the **`requests`** library in Python, covering both foundational concepts and advanced techniques for working with HTTP.

The aim is to not only master the basic usage of the library, but also to understand **how to integrate it effectively into real-world applications**, with examples, best practices, and troubleshooting tips.
### Structure

The course is organized into six focused sections:

1. **Analyzing GET Requests and the Response Object**  
   Understanding how to send GET requests, inspect responses, and work with status codes and content.

2. **Sending Data to the Server**  
   Using POST and other HTTP methods to send form data, JSON payloads, and files.

3. **Providing and Receiving Additional Data with Headers**  
   Customizing requests and interpreting server responses via HTTP headers.

4. **Persisting Connections with Cookies and Sessions**  
   Managing stateful communication, reusing connections, and handling cookies.

5. **Working with Redirection and Timeouts**  
   Controlling redirects, preventing infinite loops, and setting appropriate timeouts.

6. **Authenticating Requests for Secure APIs** 
   Implementing basic, digest, token-based, and OAuth authentication.

🔗  [Go to course](./python-requests-playbook/python-requests-playbook)

---

## 4. Working with Databases in Python

This course covers how to work with both **relational** and **NoSQL** databases in Python, moving from local lightweight solutions to production-grade setups, and including ORM and ODM usage.

The goal is to understand the different approaches to storing, retrieving, and managing data from Python, with practical examples using popular libraries and tools.

### Structure

The course is organized into six sections:

1. **Using a Local Relational Database – SQLite**  
   Introduction to SQLite databases, reviewing starter code, using the `sqlite3` module, and working with row factories.

2. **Using a Relational Database – PostgreSQL and psycopg2** 
   Installing `psycopg2`, inserting and retrieving data from PostgreSQL.

3. **Using an ORM – SQLAlchemy**  
   Overview of Object-Relational Mapping concepts, working with SQLAlchemy, and defining relationships.

4. **Using a Local NoSQL Database – Mongita**  
   Introduction to NoSQL databases and working with Mongita.

5. **Using a NoSQL Database – MongoDB and PyMongo**  
   Connecting to MongoDB, migrating from Mongita to PyMongo, filtering data, and handling embedded documents.

6. **Using an ODM – MongoEngine**  

   Understanding the differences between ODM and ORM, data modeling with MongoEngine, and managing embedded documents.

🔗 [Go to course](./working-with-databases-in-python/working-with-databases-in-python)

---

# Purpose

- This repository is part of a broader learning project aimed at building strong Python skills through structured, topic-focused courses.  

- Each course is designed to be **self-contained**, but all follow a consistent organization and style.

- This repository was created for **deep learning and internalization** of design patterns from a Pythonic perspective. It complements a broader personal knowledge base and note system built with Obsidian.

> You are welcome to clone, fork or adapt the structure for your own study or teaching needs.
