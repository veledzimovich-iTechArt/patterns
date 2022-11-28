# Design patterns

## Principles

- Separate permanent and incapsulate flexible data/algorithms
- Programm on the interface (abstract) level not realization
- Composition better than inheritance
- Weak references
- Open/closed
- Dependency inversion - code depends from abstractions NOT from realization
- Principle of Least Knowledge - connect only with close friends
- Hollywood principe - high level component define behaviour of low level components.
- Single responsibility principe - one cause to change

## Pattern
Pattern is a solving task in context

- context - typical situation to use pattern
- task - our goal depends of context restrictions
- solving - code structure to reach goals with restrictions

Patterns balance of "powers"
- goal (light side)
- restrictions (dark side)

## Catalog of patterns by "Gang of Four"

Optional: Cristofer Alexander "A Pattern Language"

### Goal

#### Creational
- Singleton
- Abstract Factory
- Factory method

#### Behavioral (interaction and responsibilites among classes)
- State
- Strategy
- Iterator
- Observer
- Template method

#### Structural (combine objects together)
- Decorator
- Facade
- Adapter
- Complex
- Proxy

### Class or Object

#### Class patterns(inheritance)
- Template method
- Factory method
- Adapter

#### Object patterns(composition)
- Singleton
- Abstract factory
- State
- Strategy
- Iterator
- Observer
- Decorator
- Facade
- Complex
- Proxy

## How To

- Keep it simple
- Patterns aren't perfect solutuion (customize patterns)
- Use patterns when needed (for places where system could changed)
- Refactoring it is time for using patterns
- Remove patterns when needed
- Avoid over-engineering

Patterns is a words to talk about code structure.

## Antipatterns - looks like nice solution
- Golden hammer (use everywhere only one well-known technology)

## Links
https://refactoring.guru/design-patterns
