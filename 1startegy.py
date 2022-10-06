#!/usr/bin/env python3

import abc

print('\nDesign pattens')


print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')

print('\nStrategy')
print('Strategy create algorithms and incapsulate to make them iterchangeable')
print('Allowed to modify and extend them easily')


print('\n\nSimple example - empty redefine')

class Duck(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def display(self):
        pass

    def swim(self):
        print('`I can swim!')


class EmptyDuck(Duck):
    def swim(self):
        # empty redefine bad idea
        pass


print('\nSimple example - inheritance')

class FlyPermanentMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fly(self):
        pass


class QuackPermanentMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def quack(self):
        pass


class MallardDuck(Duck, FlyPermanentMixin, QuackPermanentMixin):
    def display(self):
        print(f'-- {self} --')

    def fly(self):
        print('I can fly!')

    def quack(self):
        print('I can quack!')


class RubberDuck(Duck, QuackPermanentMixin):
    def display(self):
        print(f'** {self} **')

    def quack(self):
        print('I can quack!')


class DecoyDuck(Duck):
    def display(self):
        print(f'// {self} //')


mallard = MallardDuck()
rubber = RubberDuck()
decoy = DecoyDuck()

print(mallard)
mallard.display()
mallard.swim()
mallard.quack()
mallard.fly()

print(rubber)
rubber.display()
rubber.swim()
rubber.quack()
print(getattr(rubber, 'fly', 'No quack method'))

print(decoy)
decoy.display()
decoy.swim()
print(getattr(decoy, 'quack', 'No quack method'))
print(getattr(decoy, 'fly', 'No fly method'))


print('\nAdvanced example - composition')


# iterface
class QuackBehanvior(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def quack(self):
        pass


# realizations
class Quack(QuackBehanvior):
    def quack(self):
        print(f'{self}: I can quack!')


class Squeak(QuackBehanvior):
    def quack(self):
        print(f'{self}: I can squeack!')


class MuteQuack(QuackBehanvior):
    def quack(self):
        print(f'{self}: ...')



# iterface
class FlyBehavior(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fly(self):
        pass


# realizations
class FlyWithWings(FlyBehavior):
    def fly(self):
        print('I can fly with wings!')


class RocketFly(FlyBehavior):
    def fly(self):
        print('I can fly with a rocket!')



class FlyNoWay(FlyBehavior):
    def fly(self):
        print('I can\'t fly!')



class FlexDuck(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def quack_behavior(self, quack_behavior: QuackBehanvior):
        return self._quack_behavior

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehanvior):
        self._quack_behavior = quack_behavior

    @property
    @abc.abstractmethod
    def fly_behavior(self, fly_behavior: FlyBehavior):
        return self._fly_behavior

    @fly_behavior.setter
    def fly_behavior(self, fly_behavior: FlyBehavior):
        self._fly_behavior = fly_behavior

    @abc.abstractmethod
    def display(self):
        pass

    def swim(self):
        print('swim')

    def performFly(self):
        self.fly_behavior.fly()

    def performQuack(self):
        self.quack_behavior.quack()


class RedheadDuck(FlexDuck):
    def __init__(self):
        self._quack_behavior: QuackBehanvior = Quack()
        self._fly_behavior: FlyBehavior = FlyWithWings()

    @property
    def quack_behavior(self):
        return self._quack_behavior

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehanvior):
        self._quack_behavior = quack_behavior

    @property
    def fly_behavior(self):
        return self._fly_behavior

    @fly_behavior.setter
    def fly_behavior(self, fly_behavior: FlyBehavior):
        self._fly_behavior = fly_behavior

    def display(self):
        print(f'++ {self} ++')


class ModelDuck(FlexDuck):
    _quack_behavior: QuackBehanvior = MuteQuack()
    _fly_behavior: FlyBehavior = FlyNoWay()

    @property
    def quack_behavior(self):
        return self._quack_behavior

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehanvior):
        self._quack_behavior = quack_behavior

    @property
    def fly_behavior(self):
        return self._fly_behavior

    @fly_behavior.setter
    def fly_behavior(self, fly_behavior: FlyBehavior):
        self._fly_behavior = fly_behavior


    def display(self):
        print(f'<< {self} >>')


print('-- instances --')

redhead = RedheadDuck()
print(redhead)
redhead.display()
redhead.swim()
redhead.performQuack()
redhead.performFly()


print('-- set fly --')

model = ModelDuck()
print(model)
model.display()
model.swim()
model.performQuack()
model.performFly()
print('model set fly')
model.fly_behavior = RocketFly()
model.performFly()

print('-- set quack --')

repeater = ModelDuck()
print(repeater)
repeater.display()
repeater.swim()
repeater.performQuack()
repeater.performFly()
print('repeater set quack')
repeater.quack_behavior = Squeak()
repeater.performQuack()

print('model')
model.performQuack()


class Decoy:
    _quack_behavior: QuackBehanvior = Quack()

    def __str__(self):
        return self.__class__.__name__

    @property
    def quack_behavior(self):
        return self._quack_behavior

    @quack_behavior.setter
    def quack_behavior(self, quack_behavior: QuackBehanvior):
        self._quack_behavior = quack_behavior

    def performQuack(self):
        self.quack_behavior.quack()


fake = Decoy()
print(fake)
fake.performQuack()


print('\nHierarchy')


class WeaponBehavior(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def useWeapon(self):
        pass


class AxeBehavior(WeaponBehavior):
    def useWeapon(self):
        print('Axe')


class SwordBehavior(WeaponBehavior):
    def useWeapon(self):
        print('Sword')


class KnifeBehavior(WeaponBehavior):
    def useWeapon(self):
        print('Knife')


class Character:
    @property
    @abc.abstractmethod
    def weapon_behavior(self, weapon_behavior: WeaponBehavior):
        return self._weapon_behavior

    @weapon_behavior.setter
    def set_weapon(self, weapon_behavior: WeaponBehavior):
        self._weapon_behavior = weapon_behavior

    def fight(self):
        self._weapon_behavior.useWeapon()


class Knight(Character):
    _weapon_behavior = KnifeBehavior()

class Troll(Character):
    pass


k1 = Knight()
print(k1)
k1.fight()
k1.set_weapon = SwordBehavior()
k1.fight()

k2 = Knight()
k2.fight()

t = Troll()
print(t)
t.set_weapon = AxeBehavior()
t.fight()

