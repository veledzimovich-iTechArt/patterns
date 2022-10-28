#!/usr/bin/env python3

import abc
import datetime
from typing import List

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

print('\nIterator')
print('Iterator allows to get elements of collections without knowing inner realization of the elements. Iterator responsible for iteration not collection.')

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

class PancakeHouseMenuIterator:
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

    def pop(self):
        if self.position <= 0:
            raise StopIteration
        return self.items.pop()


class DinnerMenuIterator(Iterator):
    def __init__(self, items: dict):
        self.items = items
        self.position = 0
        self.keys = list(self.items.keys())

    @property
    def has_next(self):
        if self.position >= len(self.keys):
            return False
        else:
            return True

    def __next__(self):
        item = self.items[self.keys[self.position]]
        self.position = self.position + 1
        return item

    def pop(self):
        if self.position <= 0:
            raise StopIteration

        return self.items.pop(self.keys[-1], None)

class CafeMenuIterator(Iterator):
    def __init__(self, items: set):
        self.items = list(items)
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

    def pop(self):
        if self.position <= 0:
            raise StopIteration
        return self.items.pop()

class AlternatingMenuIterator(Iterator):
    def __init__(self, items: set):
        self.items = list(items)

        self.position = datetime.datetime.today().weekday() % 2

    @property
    def has_next(self):
        if self.position >= len(self.items):
            return False
        else:
            return True

    def __next__(self):
        item = self.items[self.position]
        self.position = self.position + 2
        return item


class MenuItem:
    def __init__(self, name, desc, vegetarian, price):
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


class Menu(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_iterator(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class PancakeHouseMenu(Menu):
    def __init__(self):
        self.menu_items = []

        self.add_item(
            'K&B’s Pancake Breakfast',
            'Pancakes with scrambled eggs, and toast',
            True,
            2.99
        )

        self.add_item(
            'Regular Pancake Breakfast',
            'Pancakes with fried eggs, sausage',
            False,
            2.99
        )
        self.add_item(
            'Blueberry',
            'Pancakes made with fresh blueberries',
            True,
            3.49
        )
        self.add_item(
            'Waffles',
            'Waffles, with your choice of blueberries or strawberries',
            True,
            3.59
        )

    def add_item(self, name, desc, vegetarian, price):
        menu_item = MenuItem(name, desc, vegetarian, price)
        self.menu_items.append(menu_item)

    # shows inner realization
    # def get_menu_items(self):
    #     return self.menu_items

    def get_iterator(self):
        return PancakeHouseMenuIterator(self.menu_items)


class DinnerMenu(Menu):
    def __init__(self):
        self.menu_items = dict()

        self.add_item(
            'Vegetarian BLT',
            '(Fakin’) Bacon with lettuce & tomato on whole wheat',
            True,
            2.99
        )
        self.add_item(
            'BLT',
            'Bacon with lettuce & tomato on whole wheat',
            False,
            2.99
        )
        self.add_item(
            'Soup of the day',
            'Soup of the day, with a side of potato salad',
            False,
            3.29
        )
        self.add_item(
            'Hotdog',
            'A hot dog, with saurkraut, relish, onions, topped with cheese',
            False,
            3.05
        )

    def add_item(self, name, desc, vegetarian, price):
        menu_item = MenuItem(name, desc, vegetarian, price)
        self.menu_items[name]=menu_item

    # shows inner realization
    # def get_menu_items(self):
    #     return self.menu_items

    def get_iterator(self):
        return DinnerMenuIterator(self.menu_items)


class CafeMenu(Menu):
    def __init__(self):
        self.menu_items = set()

        self.add_item(
            'Veggie Burger and Air Fries',
            'Veggie burger on a whole wheat bun, lettuce, tomato, and fries',
            True,
            3.99
        )
        self.add_item(
            'Soup of the day',
            'A cup of the soup of the day, with a side salad”',
            False,
            3.69
        )
        self.add_item(
            'Burrito',
            'A large burrito, with whole pinto beans, salsa, guacamole',
            True,
            4.29
        )

    def add_item(self, name, desc, vegetarian, price):
        menu_item = MenuItem(name, desc, vegetarian, price)
        self.menu_items.add(menu_item)

    def get_iterator(self, alt=False):
        return CafeMenuIterator(self.menu_items)


class AltCafeMenu(CafeMenu):
    def get_iterator(self):
        return AlternatingMenuIterator(self.menu_items)


phm = PancakeHouseMenu()
dm = DinnerMenu()
cm = CafeMenu()
am = AltCafeMenu()

print(phm)
print(dm)
print(cm)
print(am)

class Waiter:
    def __init__(self, *menus: List[Menu]):
        self.menus = menus

    def _print_menu(self, iterator):
        while iterator.has_next:
            item = next(iterator)
            print(item.get_name(), end=' |')
            print(item.get_price(), end='$| ')
            print(item.get_description())


    def print_menu(self):
        print('\nMenu')
        for menu in self.menus:
            print(f'\n----\n{menu}\n----', end='\n\n')
            iterator = menu.get_iterator()
            self._print_menu(iterator)

            print('\nRemove last')
            try:
                print(iterator.pop().get_name())
            except NotImplementedError as e:
                print(e)


w = Waiter(phm, dm, cm, am)

w.print_menu()



