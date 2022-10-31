#!/usr/bin/env python3

import abc
import enum
import io
import inspect
import random
import requests
import time
import threading

from PIL import Image

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

print(
    '\nProxy - create object which managing ACCESS to the remote object or "expensive" resourse  or create protection to the resourse'
)


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
    def __init__(self, location: str, count: int=2):
        self.has_coin = HasCoin(self)
        self.no_coin = NoCoin(self)
        self.sold_out = SoldOut(self)
        self.sold = Sold(self)
        self.winner = Winner(self)

        self.location = location
        self.count = count

        self._proxy = None

        if self.count > 0:
            self.state = self.no_coin
        else:
            self.state = self.sold_out


    def __str__(self):
        return f'State: {self._state} | Count: {self.count}'

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, monitor):
        self._proxy = monitor

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location: int):
        self._location = location

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count: int):
        self._count = count

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: State):
        if self.proxy:
            self.proxy.clear()

        self._state = state

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


class Monitor(metaclass=abc.ABCMeta):
    def __init__(self, machine: GumballStateMachine):
        self._machine = machine

    @abc.abstractmethod
    def report(self):
        pass


class GumballMonitor(Monitor):

    def report(self):
        print('\n--Report--')
        print(f'Gumball Machine: {self._machine.location}')
        print(f'Gumball Count: {self._machine.count} gumballs')
        print(f'Gumball State: {self._machine.state}')


class GumballMonitorProxy(Monitor):

    def __init__(self, machine: GumballStateMachine):
        super().__init__(machine)
        self._cached_response = None
        self._machine.proxy = self

    def clear(self):
        self._cached_response = None

    def report(self):
        print('\n--Proxy Report--')
        if not self._cached_response:
            self._cached_response = (
                f'Gumball Machine: {self._machine.location}',
                f'Gumball Count: {self._machine.count} gumballs',
                f'Gumball State: {self._machine.state}'
            )

        for cached in self._cached_response:
            print(cached)


print('\nStateMachine')
gm1 = GumballStateMachine('NY', 6)
gm1.insert_coin()
gm1.turn_crank()
gm2 = GumballStateMachine('SF', 6)
gm2.insert_coin()
print(gm1)
print(gm2)

monitor1 = GumballMonitor(gm1)
monitor1.report()
monitor2 = GumballMonitor(gm2)
monitor2.report()

pm = GumballStateMachine('PM', 4)
monitor_proxy = GumballMonitorProxy(pm)
monitor_proxy.report()

pm.insert_coin()
pm.turn_crank()

monitor_proxy.report()

print('\nVirtual proxy')

class Icon(metaclass=abc.ABCMeta):
    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image: Image) -> None:
        self._image = image

    @abc.abstractmethod
    def get_width(self):
        pass

    @abc.abstractmethod
    def get_height(self):
        pass

    @abc.abstractmethod
    def paint(self):
        pass


class ImageIcon(Icon):
    def __init__(self, url: str, label: str = 'Label'):
        self.label = label

        filename = url.split('/')[-1]
        data = requests.get(url, allow_redirects=True)
        self.image = Image.open(io.BytesIO(data.content))

    def get_width(self):
        if self.image:
            return self.image.size[0]
        return 800

    def get_height(self):
        if self.image:
            return self.image.size[1]
        return 600

    def paint(self):
        print('Label:', self.label)
        self.image.show()


class ImageProxy(Icon):
    def __init__(self, url: str):
        self.url = url
        self._image: Image = None
        self.is_retrieving = False

    def get_width(self):
        if self.image:
            return self.image.get_width()
        return 800

    def get_height(self):
        if self.image:
            return self.image.get_height()
        return 600

    def _download_image(self, url: str):
        time.sleep(1)
        self.image = ImageIcon(self.url, 'Cover')
        self.image.paint()
        print('Done...')

    def paint(self):
        if self.image:
            self.image.paint()
        else:
            print('Loading...')
            if not self.is_retrieving:
                try:
                    self.is_retrieving = True
                    retrieval_thread = threading.Thread(
                        target=self._download_image, args=(self.url,)
                    )
                    retrieval_thread.start()
                except Exception as err:
                    self.is_retrieving = False
                    return err



iproxy = ImageProxy('http://google.com/favicon.ico')

print(iproxy.get_width())
print(iproxy.get_height())

print('Image:', iproxy.image)
print(iproxy.is_retrieving)

# while not iproxy.image:
#     err = iproxy.paint()
#     if err:
#         print('Error:', err)
#         break
#     print('Image:', iproxy.image)
#     print('Retrieving:', iproxy.is_retrieving)
#     time.sleep(0.3)


print('\nImage state')

class ImageState(metaclass=abc.ABCMeta):
    def __init__(self, machine):
        self.machine = machine
        self.is_retrieving = False

        self._image = None

    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image) -> Image:
        self._image = image

    @abc.abstractmethod
    def get_width(self):
        pass

    @abc.abstractmethod
    def get_height(self):
        pass

    @abc.abstractmethod
    def paint(self):
        pass


class HasImage(ImageState):
    def get_width(self):
        return self.machine.state.image.size[0]

    def get_height(self):
        return self.machine.state.image.size[1]

    def paint(self):
        self.machine.state.image.show()


class NoImage(ImageState):
    def get_width(self):
        return 800

    def get_height(self):
        return 600

    def _download_image(self, url: str):
        time.sleep(1)

        filename = url.split('/')[-1]
        data = requests.get(url, allow_redirects=True)
        image = Image.open(io.BytesIO(data.content))

        self.machine.state = self.machine.has_image
        self.machine.state.image = image
        print('Done...')

    def paint(self):
        print('Loading...')
        if not self.is_retrieving:
            self.is_retrieving = True
            try:
                retrieval_thread = threading.Thread(
                    target=self._download_image, args=(self.machine.url,)
                )
                retrieval_thread.start()
            except Exception as err:
                print(err)
                self.is_retrieving = False


class ImageMachine:
    def __init__(self, url: str, label: str = 'Label'):
        self.url = url
        self.label = label

        # states
        self.has_image = HasImage(self)
        self.no_image = NoImage(self)

        # default state
        self.state: ImageState = self.no_image

    @property
    def icon(self):
        return self.state.image

    def get_width(self):
        return self.state.get_width()

    def get_height(self):
        return self.state.get_height()

    def paint(self):
        self.state.paint()


# img_machine = ImageMachine('http://google.com/favicon.ico')

# print(img_machine.get_width())
# print(img_machine.get_height())

# print('Image:', img_machine.icon)

# while img_machine.state == img_machine.no_image:
#     img_machine.paint()
#     print('Image:', img_machine.icon)
#     time.sleep(0.3)

# img_machine.paint()


print('\nDefense proxy')

class BasePerson(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_gender(self):
        pass

    @abc.abstractmethod
    def get_interests(self):
        pass

    @abc.abstractmethod
    def get_hot_or_not_rating(self):
        pass

    @abc.abstractmethod
    def set_name(self, name: str):
        pass

    @abc.abstractmethod
    def set_gender(self, gender: str):
        pass

    @abc.abstractmethod
    def set_interests(self, interests: str):
        pass

    @abc.abstractmethod
    def set_hot_or_not_rating(self, rating: int):
        pass

class Person(BasePerson):
    def __init__(self):
        self._name = None
        self._gender = None
        self._interests = None
        self._rating = 0
        self._rating_count = 0

    def get_name(self):
        return self._name

    def get_gender(self):
        return self._gender

    def get_interests(self):
        return self._interests

    def get_hot_or_not_rating(self):
        if not self._rating_count:
            return 0
        return self._rating/self._rating_count

    def set_name(self, name: str):
        self._name = name

    def set_gender(self, gender: str):
        self._gender = gender

    def set_interests(self, interests: str):
        self._interests = interests

    def set_hot_or_not_rating(self, rating: int):
        self._rating += rating
        self._rating_count += 1


class MethodNotAllowedError(Exception):
    def __init__(self):
        super().__init__('Method not allowed')

class UknownMethodError(Exception):
    def __init__(self):
        super().__init__('Unknown method')

class Handler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def invoke(self, *args, **kwargs):
        pass


class OwnerHandler(Handler):
    def __init__(self, person: Person):
        self.person = person

    def invoke(self, method, value=None):
        try:
            if hasattr(self.person, method):
                if 'get' in method:
                    return getattr(self.person, method)()
                elif method == 'set_hot_or_not_rating':
                    raise MethodNotAllowedError()
                elif 'set' in method:
                    return getattr(self.person, method)(value)
            raise UknownMethodError()
        except Exception as err:
            print(err)

class NoOwnerHandler(Handler):
    def __init__(self, person: Person):
        self.person = person

    def invoke(self, method, value=None):
        try:
            if hasattr(self.person, method):
                if 'get' in method:
                    return getattr(self.person, method)()
                elif method == 'set_hot_or_not_rating':
                    return getattr(self.person, method)(value)
                elif 'set' in method:
                    raise MethodNotAllowedError()
            raise UknownMethodError()
        except Exception as err:
            print(err)



class ProxyPerson(BasePerson):

    @staticmethod
    def get_proxy(person, handler):
        return ProxyPerson(handler(person))

    def __init__(self, handler: Handler):
        self.handler = handler

    def get_name(self):
        return self.handler.invoke('get_name')

    def get_gender(self):
        return self.handler.invoke('get_gender')

    def get_interests(self):
        return self.handler.invoke('get_interests')

    def get_hot_or_not_rating(self):
        return self.handler.invoke('get_hot_or_not_rating')

    def set_name(self, name: str):
        self.handler.invoke('set_name', name)

    def set_gender(self, gender: str):
        self.handler.invoke('set_gender', gender)

    def set_interests(self, interests: str):
        self.handler.invoke('set_interests', interests)

    def set_hot_or_not_rating(self, rating: int):
        self.handler.invoke('set_hot_or_not_rating', rating)

p = Person()

print('Owner')
pp = ProxyPerson.get_proxy(p, OwnerHandler)

print('Set properties')
pp.set_name('Alex')
pp.set_gender('Male')
pp.set_interests(['PL', 'Photo'])

print(pp.get_name())
print(pp.get_gender())
print(pp.get_interests())
print(pp.get_hot_or_not_rating())

print('Set rating')
try:
    pp.set_hot_or_not_rating(2)
except (MethodNotAllowedError, UknownMethodError) as err:
    print(err)

print('No owner')
npp = ProxyPerson.get_proxy(p, NoOwnerHandler)

print('Set properties')
try:
    npp.set_name('Sasha')
    npp.set_gender('Female')
    npp.set_interests(['English'])
except (MethodNotAllowedError, UknownMethodError) as err:
    print(err)

print(npp.get_name())
print(npp.get_gender())
print(npp.get_interests())

print('Set rating')
npp.set_hot_or_not_rating(2)
print(npp.get_hot_or_not_rating())


