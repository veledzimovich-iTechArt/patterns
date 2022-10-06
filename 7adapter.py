#!/usr/bin/env python3

import abc

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')

print('\nAdapter')
print('Convert class interface to an other interface.')

print('\nObject Adapter')

class Duck(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def quack(self):
        pass

    @abc.abstractmethod
    def fly(self):
        pass

class Turkey(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def gobble(self):
        pass

    @abc.abstractmethod
    def fly(self):
        pass

class MallardDuck(Duck):
    def quack(self):
        print('Quack!')

    def fly(self):
        print('I’m flying!')


class WildTurkey(Turkey):
    def gobble(self):
        print('Gobble!')

    def fly(self):
        print('I’m flying a short distance!')


class TurkeyAdapter(Duck):

    def __init__(self, turkey: Turkey):
        self.turkey = turkey

    def fly(self):
        for i in range(5):
            self.turkey.fly()

    def quack(self):
        self.turkey.gobble()


class DuckAdapter(Turkey):

    def __init__(self, duck: Duck):
        self.duck = duck

    def fly(self):
        super().fly()

    def gobble(self):
        self.duck.quack()

def test_duck(duck: Duck):
    duck.quack()
    duck.fly()

def test_turkey(turkey: Turkey):
    turkey.gobble()
    turkey.fly()


mallard_duck = MallardDuck()

wild_turkey = WildTurkey()
wild_turkey.gobble()
wild_turkey.fly()

wild_turkey_adapter = TurkeyAdapter(wild_turkey)
mallard_duck_adapter = DuckAdapter(mallard_duck)

# test_duck(mallard_duck)
test_duck(wild_turkey_adapter)

# test_turkey(wild_turkey)
test_turkey(mallard_duck_adapter)

print('\nClass Adapter')

class DuckTurkey(Duck, WildTurkey):
    def quack(self):
        WildTurkey.gobble(self)

    def fly(self):
        WildTurkey.fly(self)

class TurkeyDuck(Turkey, MallardDuck):

    def gobble(self):
        MallardDuck.quack(self)

    def fly(self):
        MallardDuck.fly(self)


duck_like_turkey = DuckTurkey()
test_duck(duck_like_turkey)

turkey_like_duck = TurkeyDuck()
test_turkey(turkey_like_duck)


print('\nIterators')

class Iterator:
    def __init__(self, items):
        self._total = len(items)
        self.items = iter(items)

    def __len__(self):
        return self._total

    def has_elements(self):
        return self._total>0

    def next_element(self):
        self._total-=1
        return next(self.items)



class IteratorWithRemove:
    def __init__(self, items):
        self._total = len(items)
        self.items = iter(items)

    def __len__(self):
        return self._total

    def has_next(self):
        return self._total>0

    def next(self):
        self._total-=1
        return next(self.items)

    def remove(self, index):
        items = list(self.items)
        items.remove(items[index])
        self._total = len(items)
        self.items = iter(items)


class EnumeratorIterator(IteratorWithRemove):
    def __init__(self, iterator: Iterator):
        self.iterator = iterator

    def __len__(self):
        return self.iterator._total

    def has_next(self):
        return self.iterator.has_elements()

    def next(self):
        return self.iterator.next_element()

    def remove(self, index):
        raise NotImplementedError('No method remove')

def test_iterator_with_remove(iterator):
    while iterator.has_next():
        print(iterator.next(), end=' ')
        if len(iterator)==2:
            try:
                iterator.remove(len(iterator)-1)
            except NotImplementedError as e:
                print(e)
    print()

lst = list(range(4))

iterator = Iterator(lst)
while iterator.has_elements():
    print(iterator.next_element(), end=' ')
print()

iterator_with_remove = IteratorWithRemove(lst)
test_iterator_with_remove(iterator_with_remove)

iterator = Iterator(lst)
enum_iter = EnumeratorIterator(iterator)
test_iterator_with_remove(enum_iter)

