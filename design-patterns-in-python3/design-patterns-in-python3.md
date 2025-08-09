# Index

- [Introduction](#introduction)
	- [SOLID Principles](#solid-principles)
	- [Abstract Base Class (ABC)](#abstract-base-class-abc)

## 1 Creational Patterns

- [1.1 Factory](01_Creational_Patterns/1.1-Factory.md)
- [1.2 Abstract Factory](01_Creational_Patterns/1.2-Abstract-Factory.md)
- [1.3 Builder](01_Creational_Patterns/1.3-Builder.md)
- [1.4 Prototype](01_Creational_Patterns/1.4-Prototype.md)
- [1.5 Singleton](01_Creational_Patterns/1.5-Singleton.md)

## 2 Structural Patterns

- [2.1 Adapter](02_Structural_Patterns/2.1-Adapter.md)
- [2.2 Bridge](02_Structural_Patterns/2.2-Bridge.md)
- [2.3 Composite](02_Structural_Patterns/2.3-Composite.md)
- [2.4 Decorator](02_Structural_Patterns/2.4-Decorator.md)
- [2.5 Façade](02_Structural_Patterns/2.5-Facade.md)
- [2.6 Flyweight](02_Structural_Patterns/2.6-Flyweight.md)
- [2.7 Proxy](02_Structural_Patterns/2.7-Proxy.md)

## 3 Behavioral Patterns

- [3.1 Strategy](03_Behavioral_Patterns/3.1-Strategy.md)
- [3.2 Command](03_Behavioral_Patterns/3.2-Command.md)
- [3.3 State](03_Behavioral_Patterns/3.3-State.md)
- [3.4 Observer](03_Behavioral_Patterns/3.4-Observer.md)
- [3.5 Visitor](03_Behavioral_Patterns/3.5-Visitor.md)
- [3.6 Chain of Responsibility](03_Behavioral_Patterns/3.6-Chain-of-Responsibility.md)
- [3.7 Mediator](03_Behavioral_Patterns/3.7-Mediator.md)
- [3.8 Memento](03_Behavioral_Patterns/3.8-Memento.md)
- [3.9 Null](03_Behavioral_Patterns/3.9-Null.md)
- [3.10 Template](03_Behavioral_Patterns/3.10-Template.md)
- [3.11 Iterator](03_Behavioral_Patterns/3.11-Iterator.md)
- [3.12 Interpreter](03_Behavioral_Patterns/3.12-Interpreter.md)

# Introduction

-  **What are design Patterns?**
	- A **design pattern** is a reusable solution to a common design problem.    
	- Originated outside software: e.g., Christopher Alexander (architecture).
	- Helps avoid reinventing solutions.
	- Promotes:
	    - **Consistency**
	    - **Reliability**
	    - **Maintainability**
	        
> _“Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in a way that you can use this solution a million times over, without doing it the same way twice.”_ – Christopher Alexander

- **Why Use Design Patterns?**
	- Reuse well-tested solutions.
	- Make your code understandable to others.
	- Ease of maintenance and evolution.
	- Encourage **best practices** and **common vocabulary**.

 - **Pattern Categories Covered**
	- **Creational** → Object creation
		- Examples: Factory, Builder, Singleton
	- **Structural** → Object relationships
	    - Examples: Adapter, Facade, Composite    
	- **Behavioral** → Object communication
	    - Examples: Strategy, Observer, Command

## SOLID Principles

The SOLID principles are five fundamental rules for object-oriented software design. They help create systems that are more maintainable, understandable, and flexible.

- **SRP – Single Responsibility Principle**
    _“One class = One job”_
    A class should have a single responsibility or reason to change.
    
- **OCP – Open/Closed Principle**
    _“Open to extend, closed to modify”_
    A class’s behavior should be extendable (via inheritance or composition) without modifying its source code.
    
- **LSP – Liskov Substitution Principle**
    _“Subclasses can replace parents.”_
    Subclasses must be substitutable for their base classes without breaking functionality.
    
- **ISP – Interface Segregation Principle**
    _“Prefer many small interfaces”_
    It is better to have specific interfaces for each client than a general-purpose one that forces the implementation of unused methods.
    
- **DIP – Dependency Inversion Principle**
    _“Program to abstractions”_
    Code should depend on abstractions (interfaces), not on concrete implementations.
## Abstract Base Class (ABC)

- Abstract Base class definition
	1. Import module
	2. Inherit from `abc.ABC` class
	3. Decorate methods with `@abc.abstractmethod` or `@abc.abstractproperty`

```python
import abc

class MyABC(abc.ABC):
	"""Abstracy Base Class definition"""
	
    @abc.abstractmethod
    def do_something(self, value):
        """Required method"""

    @abc.abstractproperty
    def some_property(self):
        """Required property"""
```

- Concrete class implementation
	1. Inherit from `ABC`
	2. Implement all abstract methods/properties
	3. Use `@property` for properties

```python
class MyClass(MyABC):
	"""Implementation of abstract base class"""
	
    def __init__(self, value=None):
        self._myprop = value

    def do_something(self, value):
	    """Implementation of abstract class method"""
        self._myprop *= value

    @property
    def some_property(self):
	    """Implementation of abstract property"""
        return self._myprop
```
