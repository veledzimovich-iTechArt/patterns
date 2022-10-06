#!/usr/bin/env python3

import abc
import sys

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')
print('7 Principle of Least Knowledge - (loose coupling, minimum awareness) connect only with close friends')


print('\nFacade')
print('Provide universal interface for group of iterfaces in subsystem. Create high-level interface which simplify subsystem')

class Base:
    def __str__(self):
        return self.__class__.__name__

class Amplifier(Base):
    def on(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def set_dvd(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def set_surround_sound(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def set_volume(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class Tuner(Base):
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class DvdPlayer(Base):
    def on(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def play(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def stop(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def eject(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class CdPlayer(Base):
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class Projector(Base):
    def on(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def wide_screen(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class TheaterLights(Base):
    def on(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def dim(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class Screen(Base):
    def up(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)
    def down(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

class PopcornPopper(Base):
    def on(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def pop(self, *args):
        print(self, sys._getframe().f_code.co_name, *args)
    def off(self, *args):
        print(self, sys._getframe(  ).f_code.co_name, *args)

amp = Amplifier()
tuner = Tuner()
dvd = DvdPlayer()
cd = CdPlayer()
projector = Projector()
lights = TheaterLights()
screen = Screen()
popper = PopcornPopper()


class HomeTheaterFacade:
    def __init__(self, amp, tuner, dvd, cd, projector, screen, lights, popper):
        self.amp = amp
        self.tuner = tuner
        self.dvd = dvd
        self.cd = cd
        self.projector = projector
        self.screen = screen
        self.lights = lights
        self.popper = popper


    def watchMovie(self, movie_name):
        print('\nGet ready to watch a movie...')
        self.popper.on()
        self.popper.pop()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on()
        self.projector.wide_screen()
        self.amp.on()
        self.amp.set_dvd(movie_name)
        self.amp.set_surround_sound()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie_name)

    def end_movie(self):
        print('\nShutting movie theater down...')
        self.popper.off();
        self.lights.on();
        self.screen.up();
        self.projector.off();
        self.amp.off();
        self.dvd.stop();
        self.dvd.eject();
        self.dvd.off();

ht = HomeTheaterFacade(amp, tuner, dvd, cd, projector, screen, lights, popper)
ht.watchMovie('Star Wars')
ht.end_movie()


