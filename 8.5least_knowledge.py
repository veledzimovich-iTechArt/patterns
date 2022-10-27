#!/usr/bin/env python3

print('\nPrinciple of Least Knowledge (loose coupling, minimum awareness)')
print('- allowed to call object methods')
print('- allowed to call methods from object passed as parameter')
print('- allowed to call methods from created objects')
print('- allowed to call self componets methods')
print('- globals')

class Engine:
    def start(self):
        print('Start')

class Doors:
    def lock(self):
        print('Locked')

class Key:
    def turns(self):
        print('Turns')
        return True

class Car:
    def __init__(self, engine):
        self.engine = engine


    def start(self, key):
        doors = Doors()

        # allowed to call methods from object passed as parameter
        authorised = key.turns()
        if authorised:
            # allowed to call self componets methods
            self.engine.start()
            # allowed to call methods from created objects
            doors.lock()
            # allowed to call object methods
            self.update_display()


    def update_display(self):
        print('Dispay on')

engine = Engine()
key = Key()
car = Car(engine=engine)
car.start(key)
