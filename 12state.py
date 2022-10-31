#!/usr/bin/env python3

import abc
import enum
import inspect
import random


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

print('\nState')
print('State manages object behaviour when object inner state has been changed. It is looks like object class changed')
print('Change behaviour on the runtime. Removes unnecessary IF')

@enum.unique
class States(enum.Enum):
    SOLD_OUT = 0
    NO_COIN = 1
    HAS_COIN = 2
    SOLD = 3
    WINNER = 4


class GumballMachine:
    def __init__(self, count):
        self.count = count

        if self.count > 0:
            self.state = States.NO_COIN
        else:
            self.state = States.SOLD_OUT

    def __str__(self):
        return f'State: {self.state} | Count: {self.count}'

    def insert_coin(self):
        if self.state == States.HAS_COIN:
            print("You can't insert another coin")
        elif self.state == States.NO_COIN:
            self.state = States.HAS_COIN
            print("You insert another a coin")
        elif self.state == States.SOLD_OUT:
            print("You can't insert another coin, the machine is sold out")
        elif self.state == States.SOLD:
            print("Please wait, we're already giving you a gumball")
        elif self.state == States.WINNER:
            print('Error: No winners here')

    def eject_coin(self):
        if self.state == States.HAS_COIN:
            self.state = States.NO_COIN
            print('Coin returned')
        elif self.state == States.NO_COIN:
            print('You have not inserted a coin')
        elif state == States.SOLD_OUT:
            print("You can’t eject, you haven’t inserted a quarter yet")
        elif self.state == States.SOLD:
            print('Sorry, you already turned the crank')
        elif self.state == States.WINNER:
            print('Error: No winners here')

    def turn_crank(self):
        if self.state == States.HAS_COIN:
            if random.random() < 0.1 and self.count > 1:
                self.state = States.WINNER
            else:
                self.state = States.SOLD

            print('You turned...')
            self.dispense()
        elif self.state == States.NO_COIN:
            print('You turned but there is no coin')
        elif self.state == States.SOLD_OUT:
            print("You turned but there are no gumballs")
        elif self.state == States.SOLD:
            print('Turning twice does not get you another gumball')
        elif self.state == States.WINNER:
            print('Error: No winners here')

    def dispense(self):
        if self.state == States.HAS_COIN:
            print('Error: No gumball. Eject coin')
        elif self.state == States.NO_COIN:
            print('Error: You need to pay')
        elif self.state == States.SOLD_OUT:
            print('Error: No gumball')
        elif self.state == States.SOLD:
            self.count-=1
            if self.count == 0:
                self.state = States.SOLD_OUT
                print('Last gumball!')
            else:
                self.state = States.NO_COIN

            print('A gumball comes')
        elif self.state == States.WINNER:
            self.count-=2
            if self.count == 0:
                self.state = States.SOLD_OUT
                print('Last gumballs!')
            else:
                self.state = States.NO_COIN
            print('\nWinner!\n')
            print('A gumball comes')

gm = GumballMachine(6)

print(gm)
gm.insert_coin()
gm.turn_crank()
print(gm)


class State(metaclass=abc.ABCMeta):
    def __init__(self, _machine):
        self._machine = _machine

    def __str__(self):
        return self.__class__.__name__

    def _get_method_name(self, frame):
        return f'"{inspect.getframeinfo(frame).function}"" action'

    def insert_coin(self):
        frame = inspect.currentframe()
        print(f'Error: wrong state {self} for {self._get_method_name(frame)}')

    def eject_coin(self):
        frame = inspect.currentframe()
        print(f'Error: wrong state {self} for {self._get_method_name(frame)}')

    def turn_crank(self):
        frame = inspect.currentframe()
        print(f'Error: wrong state {self} for {self._get_method_name(frame)}')

    def dispense(self):
        print('Error: No gumball')

    def refill(self):
        frame = inspect.currentframe()
        print(f'Error: wrong state {self} for {self._get_method_name(frame)}')


class NoCoin(State):
    def insert_coin(self):
        self._machine.state = self._machine.has_coin_state
        print("You insert another a coin")

    def eject_coin(self):
        print('You have not inserted a coin')

    def turn_crank(self):
        print('You turned but there is no coin')

    def dispense(self):
        print('Error: You need to pay')


class HasCoin(State):
    def insert_coin(self):
        print("You can't insert another coin")

    def eject_coin(self):
        self._machine.state = self._machine.no_coin_state
        print('Coin returned')

    def turn_crank(self):
        self._machine.state = self._machine.sold_state
        if random.random() > 0.5 and self._machine.count > 1:
            self._machine.state = self._machine.winner

        print('You turned...')


class Sold(State):
    def insert_coin(self):
        print("Please wait, we're already giving you a gumball")

    def eject_coin(self):
        print('Sorry, you already turned the crank')

    def turn_crank(self):
        print('Turning twice does not get you another gumball')

    def dispense(self):
        self._machine.release_ball()

        if self._machine.count > 0:
            self._machine.state = self._machine.no_coin_state
        else:
            self._machine.state = self._machine.sold_out_state
            print('No gumballs')


class SoldOut(State):
    def insert_coin(self):
        print("You can't insert another coin, the machine is sold out")

    def eject_coin(self):
        print("You can’t eject, you haven’t inserted a quarter yet")

    def turn_crank(self):
        print("You turned but there are no gumballs")

    def refill(self):
        self._machine.state = self._machine.no_coin_state

class Winner(State):

    def dispense(self):
        self._machine.release_ball()
        print('\nWinner!\n')
        self._machine.release_ball()

        if self._machine.count > 0:
            self._machine.state = self._machine.no_coin_state
        else:
            self._machine.state = self._machine.sold_out_state
            print('No gumballs')


class GumballStateMachine:
    def __init__(self, count=2):
        self.has_coin = HasCoin(self)
        self.no_coin = NoCoin(self)
        self.sold_out = SoldOut(self)
        self.sold = Sold(self)
        self.winner = Winner(self)

        self.count = count

        if self.count > 0:
            self.state = self.no_coin
        else:
            self.state = self.sold_out

    def __str__(self):
        return f'State: {self._state} | Count: {self.count}'

    def insert_coin(self):
        self.state.insert_coin()

    def eject_coin(self):
        self.state.eject_coin()

    def turn_crank(self):
        self.state.turn_crank()
        if self.state in (self.sold_state, self.winner):
            self.state.dispense()

    def release_ball(self):
        print('A gumball comes')
        if self.count != 0:
            self.count -= 1

    def refill_machine(self, balls=2):
        if self.state == self.sold_out:
            self.count += balls
            print('Machine Refilled.')
        self.state.refill()
        print(self)

    @property
    def has_coin_state(self):
        return self.has_coin

    @property
    def no_coin_state(self):
        return self.no_coin

    @property
    def sold_out_state(self):
        return self.sold_out

    @property
    def sold_state(self):
        return self.sold

    @property
    def winner_state(self):
        return self.winner

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: State):
        self._state = state

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count: int):
        self._count = count


print('\nStateMachine')
gm1 = GumballStateMachine(6)
gm2 = GumballStateMachine(6)
print('State Machine 1')
print(gm1)
gm1.insert_coin()
gm1.turn_crank()
print(gm1)
gm1.insert_coin()
gm1.turn_crank()
print(gm1)
gm1.turn_crank()
print(gm1)
print('State Machine 2')
print(gm2)

gm1.refill_machine()
gm1.insert_coin()
gm1.turn_crank()
print(gm1)

gm1.insert_coin()
gm1.turn_crank()
print(gm1)

gm1.insert_coin()
gm1.turn_crank()
print(gm1)
gm1.refill_machine()
