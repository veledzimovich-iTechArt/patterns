#!/usr/bin/env python3

import abc
from collections import deque
from rich import inspect
from typing import List, Optional, Tuple


print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')
print('7 Principle of Least Knowledge - (loose coupling, minimum awareness) connect only with close friends')
print('8 Hollywood principe (Don not call us. We call you) high level component define behaviour of low level components.')
print('9 Single responsibility principe (cohension) - one cause to change')

print('\nComposite')
print('Composite lets you compose objects into tree structures and then work with these structures as if they were individual objects.')


# iterators

class Iterator(metaclass=abc.ABCMeta):
    def __iter__(self):
        return self

    @property
    @abc.abstractmethod
    def has_next(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass

    def pop(self):
        raise NotImplementedError(
            f'{self.__class__.__name__} does not support pop'
        )


class SimpleIterator(Iterator):
    def __init__(self, items):
        self.items = items
        self.position = 0

    @property
    def has_next(self):
        if self.position >= len(self.items):
            return False
        else:
            return True

    def __next__(self):
        item = self.items[self.position]
        self.position = self.position + 1
        return item


class NullIterator(Iterator):
    @property
    def has_next(self):
        return False

    def __next__(self):
        return None


class CompositeIterator(Iterator):
    def __init__(self, iterator):
        self.stack = deque([iterator])

    def __iter__(self):
        return self

    @property
    def has_next(self):
        if not self.stack:
            return False
        # take top
        iterator = self.stack[0]
        if iterator.has_next:
            return True
        else:
            self.stack.popleft()
            return self.has_next

    def __next__(self):
        if self.has_next:
            iterator = self.stack[0]
            component = next(iterator)
            self.stack.append(component.create_iterator())
            return component
        return None

# components

class Component(metaclass=abc.ABCMeta):
    def add(self):
        raise AttributeError('method is not supported')
    def remove(self):
        raise AttributeError('method is not supported')
    def get_child(self, index: int):
        raise AttributeError('method is not supported')
    def print(self):
        raise AttributeError('method is not supported')
    def create_iterator(self):
        raise AttributeError('method is not supported')

class MenuComponent(Component):
    def get_name(self):
        raise AttributeError('method is not supported')
    def get_description(self):
        raise AttributeError('method is not supported')
    def get_price(self):
        raise AttributeError('method is not supported')
    @property
    def is_vegetarian(self):
        raise AttributeError('property is not supported')


class MenuItem(MenuComponent):
    def __init__(self, name: str, desc: str, vegetarian: bool, price: int):
        self._name = name
        self._desc = desc
        self._vegetarian = vegetarian
        self._price = price

    def get_name(self):
        return self._name

    def get_description(self):
        return self._desc

    def is_vegetarian(self):
        return self._vegetarian

    def get_price(self):
        return self._price

    def print(self):
        print(self.get_name(), end=' |')
        if self.is_vegetarian:
            print('(v)')

        print(self.get_price(), end='$ | ')
        print(self.get_description())

    def create_iterator(self):
        return NullIterator()


class Menu(MenuComponent):
    def __init__(self, name: str, desc: str) -> None:
        self._name = name
        self._desc = desc
        self.menu_components: List[MenuComponent]  = []
        self._iterator = None

    def add(self, *menu_components: Tuple[MenuComponent]) -> None:
        self.menu_components.extend(menu_components)

    def remove(self, menu_component: MenuComponent) -> None:
        item = self.menu_components.index(menu_component)
        self.menu_components.remove(item)

    def get_child(index: int) -> Optional[MenuComponent]:
        if index >= len(self.menu_components):
            return self.menu_component[index]
        return None

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._desc

    def get_price(self):
        return sum(
            component.get_price() for component in self.menu_components
        )

    def print(self) -> None:
        print('----')
        print(self.get_name(), end=' | ')
        print(self.get_description(), end=' | ')
        print(self.get_price(), end='$ |\n')
        print('----')

        for component in self.menu_components:
            component.print()

    def create_iterator(self):
        if self._iterator:
            return self._iterator
        self._iterator = CompositeIterator(
            SimpleIterator(self.menu_components)
        )
        return self._iterator

# waiter

class Waiter:
    def __init__(self, menus: MenuComponent) -> None:
        self.menus = menus

    def print_menu(self) -> None:
        self.menus.print()

    def print_vegetarian(self):
        iterator = self.menus.create_iterator()
        print('----')
        print('VEGETRIAN MENU | (V) |')
        print('----')
        while iterator.has_next:
            component = next(iterator)
            try:
                if component.is_vegetarian:
                    component.print()
            except AttributeError as e:
                print(e)


phm = Menu('PANCAKE HOUSE MENU', 'Breakfast')
phm.add(
    MenuItem(
        'K&B’s Pancake Breakfast',
        'Pancakes with scrambled eggs, and toast',
        True,
        2.99
    ),
    MenuItem(
        'Regular Pancake Breakfast',
        'Pancakes with fried eggs, sausage',
        False,
        2.99
    )
)
dm = Menu('DINER MENU', 'Lunch')
dm.add(
    MenuItem(
        'Vegetarian BLT',
        '(Fakin’) Bacon with lettuce & tomato on whole wheat',
        True,
        2.99
    ),
    MenuItem(
        'BLT',
        'Bacon with lettuce & tomato on whole wheat',
        False,
        2.99
    )
)
cm = Menu('CAFE MENU', 'Dinner')
cm.add(
    MenuItem(
        'Veggie Burger and Air Fries',
        'Veggie burger on a whole wheat bun, lettuce, tomato, and fries',
        True,
        3.99
    ),
    MenuItem(
        'Soup of the day',
        'A cup of the soup of the day, with a side salad”',
        False,
        3.69
    )
)
dsm = Menu('DESSERT MENU', 'Dessert')
dsm.add(
    MenuItem(
        'Apple Pie',
        'Apple pie with a flakey crust, topped with vanilla icecream',
        True,
        1.59
    )
)
dm.add(dsm)


menu = Menu('MENU', 'All menus')

menu.add(phm, dm, cm)
Waiter(menu).print_menu()

Waiter(menu).print_vegetarian()

print('\nComposite Iterator')
iterator = menu.create_iterator()

while iterator.has_next:
    print('-')
    next(iterator).print()
    print('-')


# realize childs for list objects
