#!/usr/bin/env python3

import abc
import datetime
import random
import time
import tkinter as tk
from PIL import ImageTk, Image
import memory_profiler
import copy

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

print('\nOther patterns')
print('Bridge, Builder, Chain of Reasponsibility, Flyweight, Mediator, Memento, Prototype, Visitor')

print('\nBridge - split a large class into two separate hierarchies—abstraction and implementation—which can be developed independently of each other. Allows to extend abstraction(remote control) independently from concrete realization(tv)')

class BaseTv:
    def __init__(self):
        self.channel = 0
        self.power = False

    def on(self):
        self.power = True

    def off(self):
        self.power = False

    @property
    def tune_channel(self, channel):
        return self.channel

    @tune_channel.setter
    def tune_channel(self, channel):
        self.channel = channel


class BaseRemoteControl(metaclass=abc.ABCMeta):
    def __init__(self, device):
        self.device = device

    def on(self):
        self.device.power = True

    def off(self):
        self.device.power = False

    @abc.abstractmethod
    def set_channel(self, channel):
        pass

class RCA(BaseTv):
    def __str__(self):
        return f'{self.__class__.__name__}: {self.power}|{self.channel}'

class RCARemote(BaseRemoteControl):
    def set_channel(self, channel):
        if not self.device.power:
            self.device.tune_channel = channel
        else:
            print('Power off!')

class Sony(BaseTv):
    def __init__(self):
        super().__init__()
        self.recording = False

    def __str__(self):
        return f'{self.__class__.__name__}: {self.power}|{self.channel}|{self.recording}'

    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False


class SonyRemote(BaseRemoteControl):
    def set_channel(self, channel):
        self.device.on()
        self.device.tune_channel = channel

    def record_on(self):
        self.device.start_recording()

    def record_off(self):
        self.device.stop_recording()

rca = RCA()
rca_remote = RCARemote(rca)
rca_remote.set_channel(1)
rca_remote.on()
rca_remote.set_channel(1)
print(rca)

sony = Sony()
sony_remote = SonyRemote(sony)
sony_remote.set_channel(1)
sony_remote.record_on()
print(sony)


print('\nBuilder - lets construct complex objects step by step')

class BaseBody:
    def __str__(self):
        return self.__class__.__name__

class SteelBody(BaseBody):
    pass

class CarbonBody(BaseBody):
    pass

class Engine:
    def __str__(self):
        return self.__class__.__name__

class Car:
    def __init__(self):
        self.engine: Engine = None
        self.body: BaseBody = None
        self.computer: bool = False

    def __str__(self):
        return f'{self.__class__.__name__}: {self.engine}|{self.body}|{self.computer}'

class Manual:
    def __init__(self):
        self.engine_manual: str = None
        self.body_manual: str = None
        self.computer_manual: str = None

    def __str__(self):
        return f'{self.__class__.__name__}: {self.engine_manual}|{self.body_manual}|{self.computer_manual}'

class BaseBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reset():
        pass

    @abc.abstractmethod
    def set_engine(self):
        pass

    @abc.abstractmethod
    def set_body(self):
        pass

    @abc.abstractmethod
    def set_computer(self):
        pass

    @abc.abstractmethod
    def get_product(self):
        pass

class CarBuilder(BaseBuilder):
    def __init__(self):
        # could reset product
        self.car: Car = None

    def reset(self):
        self.car = Car()

    def set_engine(self, engine: Engine):
        self.car.engine = engine

    def set_body(self, body: BaseBody):
        self.car.body = body

    def set_computer(self, value: bool):
        self.car.computer = value

    def get_product(self) -> Car:
        # could reset product
        return self.car

class ManualBuilder:
    def __init__(self):
        self.manual: Manual = None

    def reset(self):
        self.manual = Manual()

    def set_engine(self, value: str):
        self.manual.engine_manual = value

    def set_body(self, value: str):
        self.manual.body_manual = value

    def set_computer(self, value: str):
        self.manual.computer_manual = value

    def get_product(self) -> Manual:
        return self.manual


class Director:
    def construct_car(self, builder: BaseBuilder):
        builder.reset()
        builder.set_engine(Engine())
        builder.set_body(SteelBody())

    def construct_modern_car(self, builder: BaseBuilder):
        builder.reset()
        builder.set_engine(Engine())
        builder.set_body(CarbonBody())
        builder.set_computer(True)

    def construct_manual(self, builder: BaseBuilder):
        builder.reset()
        builder.set_engine('car engine manual')
        builder.set_body('car body manual')
        builder.set_computer('car computer manual')

    def construct_modern_manual(self, builder: BaseBuilder):
        builder.reset()
        builder.set_engine('modern car engine manual')
        builder.set_body('modern car body manual')
        builder.set_computer('modern car computer manual')


director = Director()
car_builder = CarBuilder()
man_builder = ManualBuilder()

director.construct_car(car_builder)
car = car_builder.get_product()
print(car)

director.construct_manual(man_builder)
manual = man_builder.get_product()
print(manual)

director.construct_modern_car(car_builder)
modern_car = car_builder.get_product()
print(modern_car)

director.construct_modern_manual(man_builder)
modern_manual = man_builder.get_product()
print(modern_manual)

print('\nChain of Responsibility - lets pass requests along a chain of handlers')

class BaseHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_next(nxt):
        pass

    @abc.abstractmethod
    def handle_request(self):
        pass

class Handler(BaseHandler):
    def __init__(self, app):
        self.app = app
        self.next = None

    def set_next(self, nxt: BaseHandler):
        self.next = nxt

    def handle_request(self, request):
        if self.next:
            self.next.handle_request(request)
        else:
            print('Done')

class SpamHandler(Handler):
    def can_handle(self, request):
        return 'spam' in request
    def handle_request(self, request):
        if self.can_handle(request):
            print(f'Request deleted: {request}')
        else:
            super().handle_request(request)


class FeedbackHandler(Handler):
    def can_handle(self, request):
        return '*' in request

    def handle_request(self, request):
        if self.can_handle(request):
            self.app.feedback_folder.append(request)
        else:
            super().handle_request(request)


class LocationHandler(Handler):
    def can_handle(self, request):
        return 'city' in request

    def handle_request(self, request):
        if self.can_handle(request):
            self.app.location_folder.append(request.split('city:')[1].strip())
        else:
            super().handle_request(request)


class ComplaintHandler(Handler):
    def can_handle(self, request):
        return True

    def handle_request(self, request):
        if self.can_handle(request):
            self.app.complaint_folder.append(request)
        else:
            super().handle_request(request)


class App:
    def __init__(self):
        self.feedback_folder = []
        self.location_folder = []
        self.complaint_folder = []

        self.set_chain_of_responsibility()

    def set_chain_of_responsibility(self):
        self.h1: Handler = SpamHandler(self)
        self.h2: Handler = FeedbackHandler(self)
        self.h3: Handler = LocationHandler(self)
        self.h4: Handler = ComplaintHandler(self)

        self.h1.set_next(self.h2)
        self.h2.set_next(self.h3)
        self.h3.set_next(self.h4)

    def process_request(self, request):
        self.h1.handle_request(request)

app = App()

requests = ['spam', '**', '****', '*', 'city: New York', 'it is a spam', 'too much errors']

for r in requests:
    app.process_request(r)

print(app.feedback_folder)
print(app.location_folder)
print(app.complaint_folder)


print('\nFlyweight -  lets fit more objects into the available amount of RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object')

win = tk.Tk()
win.title('Flyweight')
win.geometry("256x256")
canvas= tk.Canvas(win, width= 256, height= 256)
canvas.pack()

new_clone = Image.new('RGBA', (16, 16), (255, 0, 0, 255))

class Sprite:
    def __init__(self, x, y):
        self.image = ImageTk.PhotoImage(new_clone)
        self.x = x
        self.y = y

    def display(self, x, y):
        canvas.create_image(x,y, anchor=tk.NW, image=self.image)

class FlyweightSprite:
    def __init__(self):
        self.image = ImageTk.PhotoImage(new_clone)

class MovingSpriteState:
    def __init__(self, sprite, x, y):
        self.sprite: FlyweightSprite = sprite
        self.x = x
        self.y = y

    def display(self, x, y):
        canvas.create_image(x,y, anchor=tk.NW, image=self.sprite.image)


class SpriteManager:
    def __init__(self):
        self.moving_sprites = []

    @memory_profiler.profile
    def create_sprites(self, number):
        for i in range(number):
            self.moving_sprites.append(
                Sprite(
                    random.randint(0, 256), random.randint(0, 256)
                )
            )

    @memory_profiler.profile
    def create_flyweight_sprites(self, sprite, number):
        for i in range(number):
            self.moving_sprites.append(
                MovingSpriteState(
                    sprite, random.randint(0, 256), random.randint(0, 256)
                )
            )

    @memory_profiler.profile
    def display_sprites(self):
        for s in self.moving_sprites:
            s.display(s.x, s.y)

number_of_sprites = 1000
sm = SpriteManager()
# more memory
# sm.create_sprites(number_of_sprites)

# consume less memory
# sm.create_flyweight_sprites(FlyweightSprite(), number_of_sprites)

# sm.display_sprites()
# win.mainloop()

print("\nMediator - lets reduce chaotic dependencies between objects")

class Mediator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def notify(self, event: str) -> None:
        pass

class BaseComponent(metaclass=abc.ABCMeta):
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.register(self)

    def __str__(self):
        return self.__class__.__name__

class Alarm(BaseComponent):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.is_alarm: bool = False

    def off(self):
        self.is_alarm = False

    def on(self):
        self.is_alarm = True
        count = 0
        while self.is_alarm and count < 4:
            time.sleep(0.2)
            print('Alarm!\a')
            count += 1

class CoffeMachine(BaseComponent):
    def __init__(self, mediator):
        super().__init__(mediator)
        self.kind: str = 'Cappuchino'

    def set_kind(self, kind: str):
        self.kind = kind

    def get_coffe(self):
        print(f'Get a cup of coffe: {self.kind}')

    def on(self):
        self.mediator.notify('coffe')
        self.get_coffe()

class Calendar(BaseComponent):
    def is_weekend(self):
        return datetime.datetime.now().weekday() in (5, 6)

    def on(self):
        self.mediator.notify('calendar')
        print('Today: ', datetime.datetime.now())

class SmartHouseManager(Mediator):
    def __init__(self):
        self.__alarm: Alarm = None
        self.__coffe_machine: CoffeMachine = None
        self.__calendar: Calendar = None

    def register(self, component: BaseComponent):
        if isinstance(component, Alarm):
            self.__alarm = component
        elif isinstance(component, CoffeMachine):
            self.__coffe_machine = component
        elif isinstance(component, Calendar):
            self.__calendar = component

    def notify(self, event) -> None:
        if event == 'coffe':
            self.__alarm.on()
            if self.__calendar.is_weekend():
                self.__alarm.off()
        elif event == 'calendar':
            if not self.__calendar.is_weekend():
                self.__coffe_machine.set_kind('Espresso')
            self.__coffe_machine.on()


smh = SmartHouseManager()

alarm = Alarm(smh)
coffe_machine = CoffeMachine(smh)
calendar = Calendar(smh)

# calendar.on()
# coffe_machine.on()

print('\nMemento - lets save and restore the previous state of an object without revealing the details of its implementation.')

class Creature:
    def __init__(self, name, x, y):
        self.__name = name
        self.x = x
        self.y = y

    def __str__(self):
        return self.__name

class MasterGameObject:
    class GameMemento:
        def __init__(self, level, objects):
            self.level = level
            self.objects: list = copy.deepcopy(objects)
            self.__date = datetime.datetime.now().strftime('%d/%m/%y %H:%M')

        def __str__(self):
            return f'{self.__class__.__name__}: {self.__date}'

        def get_date(self) -> str:
            return self.__date

    def __init__(self):
        self.__level = 1
        self.__objects: list = []

    def __str__(self):
        obj = "\n".join([str(i) for i in self.__objects])
        return f'Game State\nLevel: {self.__level}\nCreatures:\n{obj}\n'

    def set_level(self, level: int) -> None:
        self.__level = level

    def add_object(self, obj: Creature) -> None:
        self.__objects.append(obj)

    def remove_object(self) -> None:
        self.__objects.pop()

    def save(self):
        return self.GameMemento(self.__level, self.__objects)

    def restore(self, memento):
        self.__level = memento.level
        self.__objects = memento.objects


class History:
    def __init__(self, game: MasterGameObject):
        self.__game = game
        self.__history: list = []

    def __str__(self):
        his = ''.join([str(i) for i in self.__history])
        return f'History:\n{his}\n---\n'

    def push(self):
        print('Save Game')
        m = self.__game.save()
        self.__history.append(m)

    def pop(self):
        print('Restore Game')
        if self.__history:
            self.__game.restore(self.__history.pop())
        else:
            print('Error: Empty history!')
        print()

mgm = MasterGameObject()
hi = History(mgm)

print(hi)
hi.pop()

mgm.add_object(Creature('Knight', 0, 0))
mgm.add_object(Creature('Dragon', 1, 1))
print(mgm)

hi.push()
print(hi)

mgm.remove_object()
mgm.set_level(2)
print(mgm)
hi.pop()

print(hi)
print(mgm)

print('\nPrototype -  lets copy existing objects without making your code dependent on their classes.')

class Prototype(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def clone(self):
        pass

class Monster(Prototype):
    def __init__(self, name=None, health=None):
        self.__name = name
        self.__health = health
    def __str__(self):
        return f'{super().__str__()}| Name: {self.__name} | Health: {self.__health}'

    def hit(self, damage):
        self.__health -= damage

    def clone(self):
        return Monster(self.__name, self.__health)


m = Monster('Moster', 16)
clone = m.clone()
m.hit(2)
print(m)
print(clone)

print('\nVisitor - lets separate algorithms from the objects on which they operate.')

class Visitor:
    def visitRoot(self, node):
        print(f'Root childs: {node.get_size()}')

    def visitChild(self, node):
        print(f'Child: {node.get_name()}')

class BaseNode(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class Root(BaseNode):
    def __init__(self):
        self.__childs = []

    def add(self, child):
        self.__childs.append(child)

    def get_size(self):
        return len(self.__childs)

    def accept(self, visitor: Visitor) -> None:
        visitor.visitRoot(self)


class Child(BaseNode):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def accept(self, visitor: Visitor) -> None:
        visitor.visitChild(self)

visitor = Visitor()

rt = Root()
ch1 = Child('42')
ch2 = Child('196')
rt.add(ch1)
rt.add(ch2)


items = [rt, ch1, ch2]

for item in items:
    item.accept(visitor)
