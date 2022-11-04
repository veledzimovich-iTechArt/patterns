#!/usr/bin/env python3

import abc
import re
import sys
import tkinter as tk
from PIL import ImageTk, Image
import time

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

print("\nInterpreter - specifies how to evaluate sentences in a language.")


class BaseExpression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def interpret(self, ctx):
        pass

# EXPRESSION = '{COMMAND}|{SEQUENCE}|{REPETITION}'
INT = r'[0-9]+'
COMMANDS = 'right|left|up|down|paint'
COMMAND = f'^({COMMANDS})$'
SEQUENCE = f'\s*[({COMMANDS});\s*]+'
REPETITION = f'^loop\s+(?P<int>{INT})\s+{SEQUENCE}'
# EXPRESSION = EXPRESSION.format(
#     COMMAND=COMMAND, SEQUENCE=SEQUENCE, REPETITION=REPETITION
# )

class RightCommand(BaseExpression):
    def interpret(self, ctx):
        app = ctx['app']
        app.canvas.move(app.robot, 8, 0)

class LeftCommand(BaseExpression):
    def interpret(self, ctx):
        app = ctx['app']
        app.canvas.move(app.robot, -8, 0)

class UpCommand(BaseExpression):
    def interpret(self, ctx):
        app = ctx['app']
        app.canvas.move(app.robot, 0, -8)

class DownCommand(BaseExpression):
    def interpret(self, ctx):
        app = ctx['app']
        app.canvas.move(app.robot, 0, 8)

class PaintCommand(BaseExpression):
    def interpret(self, ctx):
        app = ctx['app']
        coords = app.canvas.coords(app.robot)
        app.paint(*coords)


class Expression(BaseExpression):
    commands = {
        'right': RightCommand,
        'left': LeftCommand,
        'up': UpCommand,
        'down': DownCommand,
        'paint': PaintCommand,
    }

    def is_repetion(self, code: str):
        return re.match(REPETITION, code)

    def is_sequence(self, code: str):
        return re.match(SEQUENCE, code)

    def is_command(self, code: str):
        return re.match(COMMAND, code)

    def interpret(self, ctx):
        if self.is_command(ctx['code']):
            self.commands[ctx['code']]().interpret(ctx)
        elif self.is_repetion(ctx['code']):
            Repetition().interpret(ctx)
        elif self.is_sequence(ctx['code']):
            Sequence().interpret(ctx)

class Sequence(BaseExpression):
    def interpret(self, ctx):
        all_expr = ctx['code'].split(';')
        for expr in all_expr:
            ctx = {**ctx}
            ctx['code'] = expr.strip()
            Expression().interpret(ctx)

class Repetition(BaseExpression):
    def interpret(self, ctx):
        loop = re.search(INT, ctx['code'])
        count = int(loop.group())
        ctx = {**ctx}
        ctx['code'] = ctx['code'][loop.end():].strip()
        for i in range(count):
            Expression().interpret(ctx)


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Interpreter')
        self.geometry("384x512")

        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, expand=True)
        self.canvas = tk.Canvas(
            frame,
            width=384,
            height=256,
            bg='gray', bd=1, highlightthickness=0
        )
        self.canvas.pack(side=tk.BOTTOM, expand=True)

        robot_image = ImageTk.PhotoImage(
            Image.new('RGB', (8, 8), (0, 255, 128))
        )
        self.path_image =ImageTk.PhotoImage(
            Image.new('RGB', (4, 4), (0, 128, 255))
        )

        self.robot = self.canvas.create_image(
            128, 64, anchor=tk.CENTER, image=robot_image
        )
        self.entry = tk.Text(
            self, width=42, height=16, highlightthickness=0
        )
        self.entry.insert(tk.END, 'loop 5 paint; right; paint; down; paint;')
        self.entry.pack()
        self.entry.bind(
            '<Return>', lambda e: Expression().interpret(self.get_context())
        )
        tk.Button(
            self,
            text='·',
            command=lambda: Expression().interpret(self.get_context())
        ).pack()

        self.mainloop()

    def paint(self, x, y):
        self.canvas.create_image(
            x, y, anchor=tk.CENTER, image=self.path_image
        )

    def get_context(self):
        code = self.entry.get('1.0', 'end-1c')

        return {'app': self, 'code': code}

if __name__=='__main__':
    App()


