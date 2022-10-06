#!/usr/bin/env python3

import abc
import enum
import io

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')
print('5 open/closed')

print('\nDecorator')
print('Add new features to the object before or after objects method call')


print('\nSimple example - inheritance')

class Beverage(metaclass=abc.ABCMeta):

    def __init__(self, description):
        self.__description = description
        self.__milk = False
        self.__soy = False
        self.__mocha = False
        self.__whip = False
        self.__milk_cost = 1
        self.__soy_cost = 2
        self.__mocha_cost = 3
        self.__whip_cost = 4

    def __str__(self):
        return f'Beverage: {self.__description.title()}\n$: {self.cost()}'

    @property
    def has_milk(self):
        return self.__milk

    @has_milk.setter
    def set_milk(self, add_milk):
        self.__milk = add_milk

    @property
    def has_soy(self):
        return self.__soy

    @has_soy.setter
    def set_soy(self, add_soy):
        self.__soy = add_soy

    @property
    def has_mocha(self):
        return self.__mocha

    @has_mocha.setter
    def set_mocha(self, add_mocha):
        self.__mocha = add_mocha

    @property
    def has_whip(self):
        return self.__whip

    @has_whip.setter
    def set_whip(self, add_whip):
        self.__whip = add_whip

    @abc.abstractmethod
    def cost(self):
        topping = 0
        if self.has_milk:
            topping+=self.__milk_cost
        if self.has_soy:
            topping+=self.__soy_cost
        if self.has_mocha:
            topping+=self.__mocha_cost
        if self.has_whip:
            topping+=self.__whip_cost

        return topping


class HouseBlend(Beverage):

    def cost(self):
        return 1.5 + super().cost()


class DarkRoast(Beverage):

    def cost(self):
        return 2 + super().cost()

hb = HouseBlend('house blend')
hb.set_milk = True
dr = DarkRoast('dark roast')
dr.set_soy = True
dr.set_mocha = True
dr.set_whip = True

print(hb)
print(dr)


print('\nAdvanced example - extension')

@enum.unique
class Size(enum.Enum):
    TALL = 1
    GRANDE = 2
    VENTI = 3

class Beverage(metaclass=abc.ABCMeta):
    _description = 'Unknown'

    def __init__(self, cost):
        self._size = Size.TALL
        self._cost = cost

    def __str__(self):
        return f'{self.get_description().title()}\n$: {self.cost()}'

    def get_description(self):
        return f'{self._description} - {self.size.name}'

    @abc.abstractmethod
    def cost(self):
        pass

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Size):
        self._size = size



class Decorator(Beverage):
    def __init__(self, beverage, cost):
        super().__init__(cost)
        self.beverage = beverage

    def get_description(self):
        return f'{self.beverage.get_description()} | {self._description}'

    def cost(self):
        total = self._cost * self.beverage.size.value
        return self.beverage.cost() + total

class Milk(Decorator):
    _description = 'Milk'

class Soy(Decorator):
    _description = 'Soy'

class Mocha(Decorator):
    _description = 'Mocha'

class Whip(Decorator):
    _description = 'Whip'



class HouseBlend(Beverage):
    _description = 'House Blend'

    def cost(self):
        return self._cost


class DarkRoast(Beverage):
    _description = 'Dark Roast'

    def cost(self):
        return self._cost

class Espresso(Beverage):
    _description = 'Espresso'

    def cost(self):
        return self._cost

class Decaf(Beverage):
    _description = 'Decaf'

    def cost(self):
        return self._cost



drink = Whip(Mocha(Soy(HouseBlend(1.5), 1), 0.5), 2)
print(drink)

coffee = DarkRoast(2)
drink = Milk(coffee, 1.5)
print(drink)
coffee.size = Size.VENTI
drink = Milk(coffee, 1.5)
print(drink)


print('\nExample')
# print(help(io.StringIO))

class AbstractStringIODecorator(io.StringIO):
    def __init__(self, string, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.string = string

    def seek(self, *args, **kwargs):
        self.string.seek( *args, **kwargs)
    def write(self,  *args, **kwargs):
        self.string.write( *args, **kwargs)
    @abc.abstractmethod
    def read(self, num=None):
        pass

class CamelCaseStringIO(AbstractStringIODecorator):
    def read(self, num=None):
        return self.string.read(num).title().replace(' ', '')


class BraceStringIO(AbstractStringIODecorator):
    def __init__(self, string, chars, *args, **kwargs):
        super().__init__(string, *args, **kwargs)
        self.chars = chars

    def read(self, num=None):
        return f'{self.chars[0]}{self.string.read(num)}{self.chars[1]}'


output = io.StringIO()
output.write('to upper case')
output.seek(0)
print(output.read())
output.close()

decorate = BraceStringIO(CamelCaseStringIO(io.StringIO()), ('--[ ', ' ]--'))
decorate.write('to Upper Case')
decorate.seek(0)
print(decorate.read())
decorate.close()

