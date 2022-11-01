#!/usr/bin/env python3

import abc

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

print('\nComplex patterns - combine two or more patterns')

class Quackable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def quack(self):
        pass

class MallardDuck(Quackable):
    def quack(self):
        print('Quack!')

class RedheadDuck(Quackable):
    def quack(self):
        print('Quack!')

class DuckCall(Quackable):
    def quack(self):
        print('Kwak!')

class RubberDuck(Quackable):
    def quack(self):
        print('Squeak!')

class Goose:
    def honk(self):
        print('Honk!')

# adapter
class GooseAdapter(Quackable):
    def __init__(self, goose):
        self.goose = goose

    def quack(self):
        self.goose.honk()

# decorator
class QuackCounter(Quackable):
    num_quacks = 0

    def __init__(self, duck: Quackable):
        self.duck = duck

    def quack(self):
        self.duck.quack()
        QuackCounter.num_quacks += 1

    @staticmethod
    def get_quacks():
        return QuackCounter.num_quacks


class DuckSimulator:
    def __init__(self):
        self.mallard_duck = QuackCounter(MallardDuck())
        self.redhead_duck = QuackCounter(RedheadDuck())
        self.duck_call = QuackCounter(DuckCall())
        self.rubber_duck = QuackCounter(RubberDuck())
        self.goose_duck = GooseAdapter(Goose())

    def simulate_all(self):
        self._simulate(self.mallard_duck)
        self._simulate(self.redhead_duck)
        self._simulate(self.duck_call )
        self._simulate(self.rubber_duck)
        self._simulate(self.goose_duck)

        print('The ducks quacked:', QuackCounter.get_quacks(), 'times')

    def _simulate(self, duck: Quackable):
        duck.quack()

print('\nAdapter & Decorator')
dc = DuckSimulator()
dc.simulate_all()

# factory
class AbstractDuckFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_mallard_duck(self):
        pass

    @abc.abstractmethod
    def create_redhead_duck(self):
        pass

    @abc.abstractmethod
    def create_duck_call(self):
        pass

    @abc.abstractmethod
    def create_rubber_duck(self):
        pass

class CountingDuckFactory(AbstractDuckFactory):
    def create_mallard_duck(self):
        return QuackCounter(MallardDuck())

    def create_redhead_duck(self):
        return QuackCounter(RedheadDuck())

    def create_duck_call(self):
        return QuackCounter(DuckCall())

    def create_rubber_duck(self):
        return QuackCounter(RubberDuck())

class GooseDuckFactory:
    def create_goose(self):
        return GooseAdapter(Goose())

# iterator

class Flock(Quackable):
    def __init__(self):
        self.quackers = []

    def add(self, *args):
        for arg in args:
            self.quackers.append(arg)

    def quack(self):
        iterator = iter(self.quackers)
        try:
            while q := next(iterator):
                q.quack()
        except StopIteration:
            # print('Stop Iteration')
            pass


class FactoryDuckSimulator:
    def simulate_all(self, duck_factory, goose_factory):
        mallard_duck = duck_factory.create_mallard_duck()
        redhead_duck = duck_factory.create_redhead_duck()
        duck_call = duck_factory.create_duck_call()
        rubber_duck = duck_factory.create_rubber_duck()
        goose_duck = goose_factory.create_goose()

        flock_ducks = Flock()
        flock_ducks.add(
            mallard_duck, redhead_duck, duck_call, rubber_duck, goose_duck
        )

        flock_mallards = Flock()
        flock_mallards.add(
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck()
        )

        flock_ducks.add(flock_mallards)

        self._simulate(flock_ducks)
        self._simulate(flock_mallards)

        print('The ducks quacked:', QuackCounter.get_quacks(), 'times')

    def _simulate(self, duck: Quackable):
        duck.quack()

print('\nFactory')
duck_factory = CountingDuckFactory()
goose_factory = GooseDuckFactory()
fdc = FactoryDuckSimulator()
fdc.simulate_all(duck_factory, goose_factory)


print('\nObserver')

class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, duck):
        pass

class QuackoLogist(Observer):
    def update(self, duck):
        print('QuackoLogist:', duck, 'just quacked.')

class HonkLogist(Observer):
    def update(self, duck):
        print('HonkLogist:', duck, 'just honked.')


class QuackObservable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register(self, observer):
        pass

    @abc.abstractmethod
    def notify(self):
        pass


class Observable(QuackObservable):
    def __init__(self, duck: QuackObservable):
        self.duck = duck
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def notify(self):
        iterator = iter(self.observers)
        try:
            while obs := next(iterator):
                obs.update(self.duck)
        except StopIteration:
            pass


class Quackable(QuackObservable):
    @abc.abstractmethod
    def quack(self):
        pass


class BaseQuackableMixin(Quackable):
    def __init__(self):
        self.observable = Observable(self)

    def __str__(self):
        return self.__class__.__name__

    def quack(self):
        print('Quack!')
        self.notify()

    def register(self, observer):
        self.observable.register(observer)

    def notify(self):
        self.observable.notify()

class MallardDuck(BaseQuackableMixin):
    pass

class RedheadDuck(BaseQuackableMixin):
    pass


class GooseAdapter(BaseQuackableMixin):
    def __init__(self, goose):
        super().__init__()
        self.goose = goose

    def quack(self):
        self.goose.honk()
        self.notify()


class ObservableQuackCounter(Quackable):
    num_quacks = 0

    def __init__(self, duck: Quackable):
        self.duck = duck

    def quack(self):
        self.duck.quack()
        ObservableQuackCounter.num_quacks += 1

    def register(self, observer):
        self.duck.observable.register(observer)

    def notify(self):
        self.duck.observable.notify()

    @staticmethod
    def get_quacks():
        return ObservableQuackCounter.num_quacks


class ObservableCountingDuckFactory(AbstractDuckFactory):
    def create_mallard_duck(self):
        return ObservableQuackCounter(MallardDuck())

    def create_redhead_duck(self):
        return ObservableQuackCounter(RedheadDuck())

    def create_duck_call(self):
        return ObservableQuackCounter(DuckCall())

    def create_rubber_duck(self):
        return ObservableQuackCounter(RubberDuck())


class ObservableFlock(Quackable):
    def __init__(self):
        self.quackers = []
        self.observable = Observable(self)

    def add(self, *args):
        for arg in args:
            self.quackers.append(arg)

    def quack(self):
        iterator = iter(self.quackers)
        try:
            while q := next(iterator):
                q.quack()
        except StopIteration:
            # print('Stop Iteration')
            pass

    def register(self, observer):
        for quacker in self.quackers:
            quacker.register(observer)

    def notify(self):
        self.observable.notify()


class ObserverDuckSimulator:
    def simulate_all(self, duck_factory, goose_factory):
        flock_mallards = ObservableFlock()
        flock_mallards.add(
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck(),
            duck_factory.create_mallard_duck()
        )
        quackologist = QuackoLogist()
        flock_mallards.register(quackologist)
        self._simulate(flock_mallards)

        redhead_duck = duck_factory.create_redhead_duck()
        redhead_duck.register(quackologist)
        self._simulate(redhead_duck)

        gooselogist = HonkLogist()
        goose_duck = goose_factory.create_goose()
        goose_duck.register(quackologist)
        goose_duck.register(gooselogist)
        self._simulate(goose_duck)

        print(
            'The ducks quacked:', ObservableQuackCounter.get_quacks(), 'times'
        )

    def _simulate(self, duck: Quackable):
        duck.quack()


duck_factory = ObservableCountingDuckFactory()
goose_factory = GooseDuckFactory()
odc = ObserverDuckSimulator()
odc.simulate_all(duck_factory, goose_factory)
