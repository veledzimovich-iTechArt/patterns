#!/usr/bin/env python3

import abc

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')

print('\nSingleton')
print('Gurantee that class has only one instance and provide global endpoint to get this instance')

class Singleton:
    count = 0
    instance: 'Singleton' = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.count += 1
            cls.instance = super().__new__(cls)
        return cls.instance

    def __str__(self):
        return f'{self.__class__.__name__} - {self.count}'

    @staticmethod
    def get_instance():
        if Singleton.instance == None:
            Singleton.count += 1
            Singleton.instance = Singleton()
        return Singleton.instance


single = Singleton()
print(single)

other = Singleton()
print(other)
print(single is other)

getsingle = Singleton.get_instance()
print(getsingle)
print(getsingle is other)


class Boiler:
    _count = 0
    _empty = True
    _boiled = False
    def __init__(self):
        Boiler._count+=1
        self._count = Boiler._count

    def __str__(self):
        name = self.__class__.__name__
        return f'{name} - {self._count} |{self.is_empty}-{self.is_boiled}'

    @property
    def is_empty(self):
        return Boiler._empty

    @property
    def is_boiled(self):
        return Boiler._boiled

    def fill(self):
        if self.is_empty:
            Boiler._empty = False

    def boil(self):
        if not self.is_empty and not self.is_boiled:
            Boiler._boiled = True

    def drain(self):
        if not self.is_empty and self.is_boiled:
            Boiler._empty = True
            Boiler._boiled = False


# artificial example

boiler1 = Boiler()

print(boiler1)
boiler1.fill()
print(boiler1)
boiler1.boil()
print(boiler1)

boiler2 = Boiler()
boiler2.drain()
print('boiler1 is boiler2', boiler1 is boiler2)
# here is a problem we rewrite class variables
print(boiler1)
print(boiler2)

print('\nSingleBoiler')
class SingleBoiler:
    _count = 0
    _empty = True
    _boiled = False
    _instance: 'SingleBoiler' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._count += 1
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._count = SingleBoiler._count

    def __str__(self):
        name = self.__class__.__name__
        return f'{name} - {self._count} |{self.is_empty}-{self.is_boiled}'

    @property
    def is_empty(self):
        return SingleBoiler._empty

    @property
    def is_boiled(self):
        return SingleBoiler._boiled

    def fill(self):
        if self.is_empty:
            SingleBoiler._empty = False

    def boil(self):
        if not self.is_empty and not self.is_boiled:
            SingleBoiler._boiled = True

    def drain(self):
        if not self.is_empty and self.is_boiled:
            SingleBoiler._empty = True
            SingleBoiler._boiled = False

boiler1 = SingleBoiler()

print(boiler1)
boiler1.fill()
print(boiler1)
boiler1.boil()
print(boiler1)

boiler2 = SingleBoiler()
boiler2.drain()
print('boiler1 is boiler2', boiler1 is boiler2)
print(boiler1)
print(boiler2)

# init before starting threads
# threads
import threading
import time
print('\nThreads')
class TSin:
    _count = 0
    _instance: 'SingleBoiler' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._count += 1
            cls._instance = super().__new__(cls)
        return cls._instance

    def __str__(self):
        name = self.__class__.__name__
        return f'{name}: {self._count}'


def thread_function(name):
    print(f'Start {name}')
    time.sleep(2)
    ts = TSin()
    print(ts)
    print(f'Fin {name}')

threads = list()
for i in range(3):
    th = threading.Thread(target=thread_function, args=[i])
    threads.append(th)
    th.start()

for i, th in enumerate(threads):
    print('Join', i, th)
    th.join()
    print('Done')


