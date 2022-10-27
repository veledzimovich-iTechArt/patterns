#!/usr/bin/env python3

import abc
import random
import sys
import os

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')
print('7 Principle of Least Knowledge - (loose coupling, minimum awareness) connect only with close friends')
print('8 Hollywood principe (Don not call us. We call you) high level component define behaviour of low level components.')

print('\nTemplate method')
print('Create algorithm sceleton/scheme in special method and leave realization of some steps for subclasses. Subclases can redifine parts of the algortihm without changing it structure. Usually protect special method from redefinition')

print('Special method includes concrete methods, abstarct methods and hooks')


class Coffee:
    def prepare(self):
        print('\nCoffee')
        self.boil()
        self.brew_coffe_grinds()
        self.pour_in_cup()
        self.add_sugar_and_milk()

    def boil(self):
        print('Boiling water')

    def brew_coffe_grinds(self):
        print('Dripping coffee throung filter')

    def pour_in_cup(self):
        print('Pouring into cup')

    def add_sugar_and_milk(self):
        print('Adding sugar and milk')


class Tea:
    def prepare(self):
        print('\nTea')
        self.boil()
        self.steep_tea_bag()
        self.pour_in_cup()
        self.add_lemon()

    def boil(self):
        print('Boiling water')

    def steep_tea_bag(self):
        print('Steeping the tea')

    def pour_in_cup(self):
        print('Pouring into cup')

    def add_lemon(self):
        print('Adding lemon')

coffee = Coffee()
coffee.prepare()

tea = Tea()
tea.prepare()

print('\nSimple Base Class')

class Beverage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def prepare(self):
        pass

    def boil(self):
        print('Boiling water')

    def pour_in_cup(self):
        print('Pouring into cup')


class Coffee(Beverage):
    def prepare(self):
        print('\nCoffee')
        self.boil()
        self.brew_coffe_grinds()
        self.pour_in_cup()
        self.add_sugar_and_milk()

    def brew_coffe_grinds(self):
        print('Dripping coffee throung filter')

    def add_sugar_and_milk(self):
        print('Adding sugar and milk')


class Tea(Beverage):
    def prepare(self):
        print('\nTea')
        self.boil()
        self.steep_tea_bag()
        self.pour_in_cup()
        self.add_lemon()

    def steep_tea_bag(self):
        print('Steeping the tea')

    def add_lemon(self):
        print('Adding lemon')

coffee = Coffee()
coffee.prepare()

tea = Tea()
tea.prepare()


print('\nTemplate method')
class AbsBeverage(metaclass=abc.ABCMeta):
    def __prepare(self):
        print(f'\n{self.__class__.__name__}')
        self.__boil()
        self.brew()
        self.__pour_in_cup()
        self.add_condiments()

    def prepare(self):
        self.__prepare()

    def __boil(self):
        print('Boiling water')

    @abc.abstractmethod
    def brew(self):
        pass

    def __pour_in_cup(self):
        print('Pouring into cup')

    @abc.abstractmethod
    def add_condiments(self):
        pass

class Coffee(AbsBeverage):

    def brew(self):
        print('Dripping coffee throung filter')

    def add_condiments(self):
        print('Adding sugar and milk')


class Tea(AbsBeverage):

    def brew(self):
        print('Steeping the tea')

    def add_condiments(self):
        print('Adding lemon')

coffee = Coffee()
coffee.prepare()

tea = Tea()
tea.prepare()


print('\nhooks')

class AbsBeverageWithHook(metaclass=abc.ABCMeta):
    def __prepare(self):
        print(f'\n{self.__class__.__name__}')
        self.__boil()
        self.brew()
        self.__pour_in_cup()
        if self.is_add_condiments():
            self.add_condiments()

    def prepare(self):
        self.__prepare()

    def __boil(self):
        print('Boiling water')

    @abc.abstractmethod
    def brew(self):
        pass

    def __pour_in_cup(self):
        print('Pouring into cup')

    @abc.abstractmethod
    def add_condiments(self):
        pass

    # hook
    def is_add_condiments(self):
        return True



class CoffeeWithHook(AbsBeverageWithHook):

    def brew(self):
        print('Dripping coffee throung filter')

    def add_condiments(self):
        print('Adding sugar and milk')

    def is_add_condiments(self):
        answer = input('Sugar and Milk?')
        if answer.lower().startswith('y'):
            return True
        return False

coffee = CoffeeWithHook()
# coffee.prepare()


print('\nsort')

class Comparable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __lt__(self, other):
        pass

class Duck(Comparable):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return f'{self.name} {self.weight}'

    def __repr__(self):
        return f'{self.name} {self.weight}'

    def __lt__(self, other):
        return self.weight < other.weight


ducks = [Duck(chr(97+i), i) for i in range(4)]
random.shuffle(ducks)
print(ducks)
ducks.sort()
for duck in ducks:
    print(duck)

