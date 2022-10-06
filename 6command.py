#!/usr/bin/env python3

import abc
import os

print('\nDesign pattens')

print('1 separate permanent and incapsulate flexible data/algorithms')
print('2 programm on the interface (abstract) level not realization')
print('3 composition better than inheritance')
print('4 Weak references')
print('5 open/closed')
print('6 Dependency inversion - code depends from abstractions NOT from realization (high level component [NYPizzaStore] is not depends from low level components [NYCheezePizza])')


print('\nCommand')
print('Encapsulate request in object and allows to include different actions in request, process of requests(transactions) registration, cancelation and quenee organization')


# receiver
class Light:
    def __init__(self, location='Default'):
        self.location = location

    def on(self):
        print('Light is on')

    def off(self):
        print('Light is off')


class GarageDoor:
    def __init__(self, location='Default'):
        self.location = location

    def light_on(self):
        print('Light is on')

    def light_off(self):
        print('Light is off')

    def up(self):
        print('Door is open')

    def down(self):
        print('Door is closed')

    def stop(self):
        print('Door is stop')

class Stereo:
    def __init__(self, location='Default'):
        self.location = location

    def on(self):
        print('Stereo is on')

    def off(self):
        print('Stereo is off')

    def set_CD(self):
        print('Set CD')

    def set_DVD(self):
        print('Set DVD')

    def set_radio(self):
        print('Set radio')

    def set_volume(self, value):
        print(f'Set volume to {value}')


class CeilingFan:
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    OFF = 0

    def __init__(self, location):
        self.location = location
        self.speed = CeilingFan.OFF

    def high(self):
        self.speed = CeilingFan.HIGH

    def medium(self):
        self.speed = CeilingFan.MEDIUM

    def low(self):
        self.speed = CeilingFan.LOW

    def off(self):
        self.speed = CeilingFan.OFF

    def get_speed(self):
        return self.speed


# command
class Command(metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

    def store(self, log_file):
        with open(log_file, mode='a') as file:
            file.write(f'{self.__class__.__name__}-{id(self)}')
            file.write('\n')

    def load(self):
        self.execute()


class NoCommand(Command):
    def execute(self):
        raise NotImplementedError('No Command')
    def undo(self):
        raise NotImplementedError('No Command')

# concrete commands
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

class GarageDoorOpenCommand(Command):
    def __init__(self, garage_door: GarageDoor):
        self.garage_door = garage_door

    def execute(self):
        self.garage_door.up()
        self.garage_door.light_on()

    def undo(self):
        self.garage_door.down()
        self.garage_door.light_off()


class GarageDoorCloseCommand(Command):
    def __init__(self, garage_door: GarageDoor):
        self.garage_door = garage_door

    def execute(self):
        self.garage_door.down()
        self.garage_door.light_off()

    def undo(self):
        self.garage_door.up()
        self.garage_door.light_on()


class StereoOnWithCDCommand(Command):
    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def execute(self):
        self.stereo.on()
        self.stereo.set_CD()
        self.stereo.set_volume(11)

    def undo(self):
        self.stereo.off()


class StereoOff(Command):
    def __init__(self, stereo: Stereo):
        self.stereo = stereo

    def execute(self):
        self.stereo.off()

    def undo(self):
        self.stereo.on()


class BaseCeilingFanSpeedCommand(Command):
    def __init__(self, fan: CeilingFan):
        self.fan = fan
        self.prev_speed = None

    def undo(self):
        if self.prev_speed == CeilingFan.HIGH:
            self.fan.high()
        elif self.prev_speed == CeilingFan.MEDIUM:
            self.fan.medium()
        elif self.prev_speed == CeilingFan.LOW:
            self.fan.low()
        elif self.prev_speed == CeilingFan.OFF:
            self.fan.off()

class CeilingFanHighCommand(BaseCeilingFanSpeedCommand):
    def execute(self):
        self.prev_speed = self.fan.get_speed()
        self.fan.high()

class CeilingFanMediumCommand(BaseCeilingFanSpeedCommand):
    def execute(self):
        self.prev_speed = self.fan.get_speed()
        self.fan.medium()

class CeilingFanLowCommand(BaseCeilingFanSpeedCommand):
    def execute(self):
        self.prev_speed = self.fan.get_speed()
        self.fan.low()

class CeilingFanOffCommand(BaseCeilingFanSpeedCommand):
    def execute(self):
        self.prev_speed = self.fan.get_speed()
        self.fan.off()


# invoker (hold receiver and execude command)
class SimpleRemoteControl:
    def __init__(self):
        self.slot = None

    def set_command(self, command: Command):
        self.slot = command

    def button_pressed(self):
        if self.slot:
            self.slot.execute()

remote = SimpleRemoteControl()

light = Light()
light_command = LightOnCommand(light)

door = GarageDoor()
door_command = GarageDoorOpenCommand(door)

remote.set_command(light_command)
remote.button_pressed()

remote.set_command(door_command)
remote.button_pressed()


class RemoteControl():
    def __init__(self, number_of_slots=7):
        self.number_of_slots = number_of_slots
        self.on_commands = [NoCommand() for i in range(self.number_of_slots)]
        self.off_commands = [NoCommand() for i in range(self.number_of_slots)]
        self.undo_command = NoCommand()

        self.log_file = '6log.txt'
        self.clear_log()

    def __str__(self):
        out = ['---Remote Contol---']
        for slot in range(self.number_of_slots):
            out.append(
                f'[Slot {slot}] {self.on_commands[slot]} || {self.off_commands[slot]}')
        out.append(f'[undo] {self.undo_command}')
        return '\n'.join(out)

    def set_command(self, index, on_command: Command, off_command: Command):
        self.on_commands[index] = on_command
        self.off_commands[index] = off_command

    def on_button_pressed(self, index):
        if index < len(self.on_commands):
            try:
                self.on_commands[index].execute()
                self.on_commands[index].store(self.log_file)
                self.undo_command = self.on_commands[index]
            except NotImplementedError as err:
                print(err)

    def off_button_pressed(self, index):
        if index < len(self.off_commands):
            try:
                self.off_commands[index].execute()
                self.off_commands[index].store(self.log_file)
                self.undo_command = self.off_commands[index]
            except NotImplementedError as err:
                print(err)

    def undo_button_pressed(self):
        self.undo_command.undo()
        self.undo_command.store(self.log_file)

    def clear_log(self):
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

    def restore(self):

        if os.path.isfile(self.log_file):
            on_cmd = dict(
                (id(cmd), cmd) for cmd in self.on_commands
            )
            off_cmd = dict(
                (id(cmd), cmd) for cmd in self.off_commands
            )
            with open(self.log_file) as file:
                commands = file.readlines()
            for cmd in commands:
                name, cmd_id = cmd.strip().split('-')

                on_exitst = on_cmd.get(int(cmd_id))
                off_exists = off_cmd.get(int(cmd_id))

                if on_exitst:
                    on_exitst.execute()
                if off_exists:
                    off_exists.execute()


remote = RemoteControl()


light = Light()
light_on_command = LightOnCommand(light)
light_off_command = LightOffCommand(light)

door = GarageDoor()
door_on_command = GarageDoorOpenCommand(door)
door_off_command = GarageDoorCloseCommand(door)


remote.set_command(0, light_on_command, light_off_command)
remote.set_command(1, door_on_command, door_off_command)

remote.on_button_pressed(0)
remote.on_button_pressed(1)
remote.off_button_pressed(0)
remote.off_button_pressed(1)
remote.undo_button_pressed()


remote.on_button_pressed(2)
remote.off_button_pressed(2)


stereo = Stereo()
stereo_on_with_cd = StereoOnWithCDCommand(stereo)
stereo_off_with_cd = StereoOff(stereo)
remote.set_command(2, stereo_on_with_cd, stereo_off_with_cd)

remote.on_button_pressed(2)
remote.off_button_pressed(2)
print(remote)

remote = RemoteControl()
fan = CeilingFan('hall')
fan_high = CeilingFanHighCommand(fan)
fan_med = CeilingFanMediumCommand(fan)
fan_low = CeilingFanLowCommand(fan)
fan_off = CeilingFanOffCommand(fan)

remote.set_command(0, fan_high, fan_off)
remote.set_command(1, fan_med, fan_off)
remote.set_command(2, fan_low, fan_off)
print(remote)

remote.on_button_pressed(1)
remote.off_button_pressed(1)
print(remote)
remote.undo_button_pressed()
print(fan.get_speed())
remote.on_button_pressed(2)
remote.undo_button_pressed()
print(remote)
print(fan.get_speed())


print('\nMacro Command')
class MacroCommand(Command):
    def __init__(self, commands):
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()

    def undo(self):
        for command in self.commands:
            command.undo()

party_on = [light_on_command, stereo_on_with_cd, door_on_command]
party_off = [light_off_command, stereo_off_with_cd, door_off_command]

party_on_macro = MacroCommand(party_on)
party_off_macro = MacroCommand(party_off)

remote.set_command(3, party_on_macro, party_off_macro)
print(remote)
remote.on_button_pressed(3)
remote.off_button_pressed(3)
print(remote)
remote.undo_button_pressed()

print('\nRestore from log')
# restore commands
remote.restore()

print('\nLambda Command')

class LambdaRemoteControl:
    def __init__(self, number_of_slots=7):
        self.number_of_slots = number_of_slots
        no_command = lambda: ('No Command', None)
        self.on_commands = [no_command for i in range(self.number_of_slots)]
        self.off_commands = [no_command for i in range(self.number_of_slots)]
        self.undo_command = no_command

    def __str__(self):
        out = ['---Remote Contol---']
        for slot in range(self.number_of_slots):
            out.append(
                f'[Slot {slot}] {self.on_commands[slot]()[0]} || {self.off_commands[slot]()[0]}')
        out.append(f'[undo] {self.undo_command()[0]}')
        return '\n'.join(out)

    def set_command(
            self, index, name, on_command: Command, off_command: Command
        ):
        self.on_commands[index] = lambda: (name, on_command)
        self.off_commands[index] = lambda: (name, off_command)

    def on_button_pressed(self, index):
        if index < len(self.on_commands):
            _, cmd = self.on_commands[index]()
            if cmd:
                cmd()
                self.undo_command = self.on_commands[index]

    def off_button_pressed(self, index):
        if index < len(self.off_commands):
            _, cmd = self.off_commands[index]()
            if cmd:
                cmd()
                self.undo_command = self.off_commands[index]


    def undo_button_pressed(self):
        self.undo_command()[1]()

remote = LambdaRemoteControl()
remote.set_command(0, 'Light', lambda: light.on(), lambda: light.off())
print(remote)
remote.on_button_pressed(0)
remote.off_button_pressed(0)
remote.undo_button_pressed()

def lambda_stereo_on():
    stereo.on()
    stereo.set_CD()
    stereo.set_volume(11)

remote.set_command(1, 'Stereo', lambda_stereo_on, stereo.off)
remote.on_button_pressed(1)
remote.off_button_pressed(1)
remote.undo_button_pressed()
print(remote)
remote.on_button_pressed(2)

