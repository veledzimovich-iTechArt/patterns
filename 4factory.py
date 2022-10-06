#!/usr/bin/env python3

import abc
import enum

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')

print('\nFactory Method - inheritance')
print(
    'Define how setup object, but allow to choose in subclasses type of the object class. Delegate process of creation object to subclasses. Creator do not have information about object type'
)
print('1. Do not save reference to concrete class in var')
print('2. Inherit from abstract class or iterface')
print('3. Methods does not redefine base class methods')

print('\nAbstract Factory - composition')
print('The interface to create related objects without dependency from concrete classes')

print('\nSimple Factory')

class Pizza(metaclass=abc.ABCMeta):
    def __init__(self, kind: str):
        self.kind = kind

    def __str__(self):
        return self.kind

    def prepare(self):
        pass

    def bake(self):
        pass

    def cut(self):
        pass

    def box(self):
        pass

class CheezePizza(Pizza):
    pass

class PeperoniPizza(Pizza):
    pass

class SimplePizzaFactory:
    def create_pizza(self, kind: str) -> Pizza:
        pizza = None
        if kind == 'cheese':
            pizza = CheezePizza(kind)
        elif kind == 'pepperoni':
            pizza = PeperoniPizza(kind)
        return pizza


class PizzaStore:
    def __init__(self, factory: SimplePizzaFactory):
        self.factory = factory

    def order(self, kind: str) -> Pizza:
        pizza = self.factory.create_pizza(kind)

        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()

        return pizza

sf = SimplePizzaFactory()
ps = PizzaStore(sf)
print(ps.order('cheese'))
print(ps.order('pepperoni'))


print('\nFactory Method')

# enums
class PizzaKind(str, enum.Enum):
    Cheese = 'cheese'
    Pepperoni = 'pepperoni'
    Clam = 'clam'
    Veggie = 'veggie'

class DoughKind(str, enum.Enum):
    Thin = 'Thin Crust Dough'
    Thick = 'Extra Thick Crust Dough'

class SauceKind(str, enum.Enum):
    Marinara = 'Marinara Sauce'
    PlumTomato = 'Plum Tomato Sauce'

class ToppingKind(str, enum.Enum):
    GratedReggianoCheese = 'Grated Reggiano Cheese'
    ShreddedMozzarellaCheese = 'Shredded Mozzarella Cheese'

# objects
class Pizza(metaclass=abc.ABCMeta):
    def __str__(self):
        sauce = f' with {self.sauce}' if self.sauce else ''

        if len(self.toppings) > 1:
            tops = ', '.join(self.toppings[:-1])
            tops = f', {tops} and {self.toppings[-1]}'
        elif len(self.toppings) == 1:
            tops = f' and {self.toppings[-1]}'
        else:
            tops = ''
        return f'{self.name} on {self.dough}{sauce}{tops}'

    def prepare(self):
        print(f'Preparing {self.name}')
        print(f'Tossing dough...')
        print(f'Adding sauces...')
        print(f'Adding toppings...', end=' ')
        print(f'{" ".join(self.toppings)}')

    def bake(self):
        print('Bake for 25 minutes at 350')

    def cut(self):
        print('Cutting the pizza into diagonal slices')

    def box(self):
        print('Place pizza in official PizzaStore box')


# depends from Pizza (abstract) only
class NYCheezePizza(Pizza):
    def __init__(self):
        self.name = 'NY Style Cheese Pizza'
        self.dough = DoughKind.Thin
        self.sauce = SauceKind.Marinara
        self.toppings = [ToppingKind.GratedReggianoCheese]

class NYPeperoniPizza(Pizza):
    name = 'NY Style Peperoni Pizza'
    dough = DoughKind.Thin
    sauce = SauceKind.Marinara
    toppings = [ToppingKind.ShreddedMozzarellaCheese]

class NYClamPizza(Pizza):
    name = 'NY Style Clam Pizza'
    dough = DoughKind.Thin
    sauce = SauceKind.Marinara
    toppings = []

class NYVeggiePizza(Pizza):
    name = 'NY Style Veggie Pizza'
    dough = DoughKind.Thin
    sauce = SauceKind.Marinara
    toppings = []

# depends from Pizza (abstract) only
class ChicagoCheezePizza(Pizza):
    name = 'Chicago Style Cheese Pizza'
    dough = DoughKind.Thick
    sauce = SauceKind.PlumTomato
    toppings = []

    def cut(self):
        print('Cutting the pizza into square slices')


class ChicagoPeperoniPizza(Pizza):
    name = 'Chicago Style Peperoni Pizza'
    dough = DoughKind.Thick
    sauce = SauceKind.PlumTomato
    toppings = []

    def cut(self):
        print('Cutting the pizza into square slices')


class ChicagoClamPizza(Pizza):
    name = 'Chicago Style Clam Pizza'
    dough = DoughKind.Thick
    sauce = SauceKind.PlumTomato
    toppings = []

    def cut(self):
        print('Cutting the pizza into square slices')

class ChicagoVeggiePizza(Pizza):
    name = 'Chicago Style Veggie Pizza'
    dough = DoughKind.Thick
    sauce = SauceKind.PlumTomato
    toppings = []

    def cut(self):
        print('Cutting the pizza into square slices')

# creators
class PizzaStore(metaclass=abc.ABCMeta):

    def order(self, kind: PizzaKind) -> Pizza:
        # control process
        # weak reference
        pizza = self.create(kind)
        print('\nThank you for your order.')
        # code depends from abstract product Pizza
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        print('Enjoy!')
        return pizza

    # factory method
    # incapsulate data about product
    # we could use it without abstraction
    @abc.abstractmethod
    def create(self, kind: PizzaKind) -> Pizza:
        # isolate client code from subclass creation process
        pass

# depends from Pizza (abstract) only
class NYPizzaStore(PizzaStore):
    def create(self, kind: PizzaKind) -> Pizza:
        pizza = None
        match kind:
            case PizzaKind.Cheese:
                pizza = NYCheezePizza()
            case PizzaKind.Pepperoni:
                pizza = NYPeperoniPizza()
            case PizzaKind.Clam:
                pizza = NYClamPizza()
            case PizzaKind.Veggie:
                pizza = NYVeggiePizza()
        return pizza

# depends from Pizza (abstract) only
class ChicagoPizzaStore(PizzaStore):
    def create(self, kind: PizzaKind) -> Pizza:
        pizza = None
        match kind:
            case PizzaKind.Cheese:
                pizza = ChicagoCheezePizza()
            case PizzaKind.Pepperoni:
                pizza = ChicagoPeperoniPizza()
            case PizzaKind.Clam:
                pizza = ChicagoClamPizza()
            case PizzaKind.Veggie:
                pizza = ChicagoVeggiePizza()
        return pizza

nyps = NYPizzaStore()
print(nyps.order(PizzaKind.Cheese))
print(nyps.order(PizzaKind.Pepperoni))

nyps = ChicagoPizzaStore()
print(nyps.order(PizzaKind.Clam))


print('\nAbstract Factory')

class Ingridient(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

class Dough(Ingridient):
    pass

class Sauce(Ingridient):
    pass

class Cheese(Ingridient):
    pass

class Veggie(Ingridient):
    pass

class Pepperoni(Ingridient):
    pass

class Clams(Ingridient):
    pass

class ThinCrustDough(Dough):
    pass

class ThickCrustDough(Dough):
    pass

class MarinaraSauce(Sauce):
    pass

class PlumTomatoSauce(Sauce):
    pass

class ReggianoCheese(Cheese):
    pass

class MozzarellaCheese(Cheese):
    pass

class Garlic(Veggie):
    pass

class Onion(Veggie):
    pass

class Mushroom(Veggie):
    pass

class RedPepper(Veggie):
    pass

class BlackOlives(Veggie):
    pass

class Spinach(Veggie):
    pass

class EggPlant(Veggie):
    pass

class SlicedPeperoni(Pepperoni):
    pass

class FreshClams(Clams):
    pass

class FrozenClams(Clams):
    pass

class PizzaIngridienFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createDough(self) -> Dough:
        pass
    @abc.abstractmethod
    def createSauce(self) -> Sauce:
        pass
    @abc.abstractmethod
    def createCheese(self) -> Cheese:
        pass
    @abc.abstractmethod
    def createVeggies(self) -> list[Veggie]:
        pass
    @abc.abstractmethod
    def createPeperoni(self) -> Pepperoni:
        pass
    @abc.abstractmethod
    def createClam(self) -> Clams:
        pass

class NYPizzaIngridientFactory(PizzaIngridienFactory):
    def createDough(self):
        return ThinCrustDough()
    def createSauce(self):
        return MarinaraSauce()
    def createCheese(self):
        return ReggianoCheese()
    def createVeggies(self) -> []:
        return [Garlic(), Onion(), Mushroom(), RedPepper()]
    def createPeperoni(self):
        return SlicedPeperoni()
    def createClam(self) -> []:
        return FreshClams()

class ChicagoPizzaIngridientFactory(PizzaIngridienFactory):
    def createDough(self):
        return ThickCrustDough()
    def createSauce(self):
        return PlumTomatoSauce()
    def createCheese(self):
        return MozzarellaCheese()
    def createVeggies(self) -> []:
        return [BlackOlives(), Spinach(), EggPlant()]
    def createPeperoni(self):
        return SlicedPeperoni()
    def createClam(self) -> []:
        return FrozenClams()

# objects
class Pizza(metaclass=abc.ABCMeta):
    def __init__(self, ingredientFactory):
        self.ingredientFactory = ingredientFactory

    def __str__(self):
        n = self.name
        d = self.dough
        s = self.sauce
        ch = self.cheese
        p = self.peperoni
        cl = self.clam

        if len(self.veggies) > 1:
            v = ', '.join([str(i) for i in self.veggies])
        elif len(self.veggies) == 1:
            v = f' {self.veggies[-1]}'
        else:
            v = ''
        return f'{n} on {d} with {s} covered by {ch}, {p}, {v} and {cl}'

    def prepare(self):
        print(f'Preparing {self.name}')
        self.dough = self.ingredientFactory.createDough()
        self.sauce = self.ingredientFactory.createSauce()
        self.cheese = self.ingredientFactory.createCheese()
        self.veggies = self.ingredientFactory.createVeggies()
        self.peperoni = self.ingredientFactory.createPeperoni()
        self.clam  = self.ingredientFactory.createClam()
        print(f'Tossing - {self.dough}')
        print(f'Adding - {self.sauce}')
        print(f'Adding - {self.cheese}')
        print(f'Adding: ', end=' ')
        print(f'{" ".join([str(i) for i in self.veggies])}')
        print(f'Adding - {self.peperoni}')
        print(f'Adding - {self.clam}')

    def bake(self):
        print('Bake for 25 minutes at 350')

    def cut(self):
        print('Cutting the pizza into diagonal slices')

    def box(self):
        print('Place pizza in official PizzaStore box')

# depends from Pizza (abstract) only
class NYCheezePizza(Pizza):
    name = 'NY Style Cheese Pizza'

class NYPeperoniPizza(Pizza):
    name = 'NY Style Peperoni Pizza'

class NYClamPizza(Pizza):
    name = 'NY Style Clam Pizza'

class NYVeggiePizza(Pizza):
    name = 'NY Style Veggie Pizza'

# depends from Pizza (abstract) only
class ChicagoCheezePizza(Pizza):
    name = 'Chicago Style Cheese Pizza'

    def cut(self):
        print('Cutting the pizza into square slices')


class ChicagoPeperoniPizza(Pizza):
    name = 'Chicago Style Peperoni Pizza'

    def cut(self):
        print('Cutting the pizza into square slices')


class ChicagoClamPizza(Pizza):
    name = 'Chicago Style Clam Pizza'

    def cut(self):
        print('Cutting the pizza into square slices')

class ChicagoVeggiePizza(Pizza):
    name = 'Chicago Style Veggie Pizza'

    def cut(self):
        print('Cutting the pizza into square slices')


# depends from Pizza (abstract) only
class NYPizzaStore(PizzaStore):
    def create(self, kind: PizzaKind) -> Pizza:
        pizza = None
        ingredientFactory = NYPizzaIngridientFactory()

        match kind:
            case PizzaKind.Cheese:
                pizza = NYCheezePizza(ingredientFactory)
            case PizzaKind.Pepperoni:
                pizza = NYPeperoniPizza(ingredientFactory)
            case PizzaKind.Clam:
                pizza = NYClamPizza(ingredientFactory)
            case PizzaKind.Veggie:
                pizza = NYVeggiePizza(ingredientFactory)
        return pizza

# depends from Pizza (abstract) only
class ChicagoPizzaStore(PizzaStore):
    def create(self, kind: PizzaKind) -> Pizza:
        pizza = None
        ingredientFactory = ChicagoPizzaIngridientFactory()

        match kind:
            case PizzaKind.Cheese:
                pizza = ChicagoCheezePizza(ingredientFactory)
            case PizzaKind.Pepperoni:
                pizza = ChicagoPeperoniPizza(ingredientFactory)
            case PizzaKind.Clam:
                pizza = ChicagoClamPizza(ingredientFactory)
            case PizzaKind.Veggie:
                pizza = ChicagoVeggiePizza(ingredientFactory)
        return pizza

nyps = NYPizzaStore()
print(nyps.order(PizzaKind.Cheese))
print(nyps.order(PizzaKind.Pepperoni))

cps = ChicagoPizzaStore()
print(cps.order(PizzaKind.Clam))
