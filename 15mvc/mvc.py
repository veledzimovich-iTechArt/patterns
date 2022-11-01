#!/usr/bin/env python3

import abc
import random
import re
import time
import tkinter as tk
from tkinter.ttk import Button

from models import (
    BlinkObserver,
    ColorModel,
    HeartAdapter,
    HeartModel,
    RGBObserver,
    INIT_COLOR, BLINK_COLOR
)

print('\nMVC - Model(observer) Controller(create view) View(strategy)')


class ColorView(tk.Tk, BlinkObserver, RGBObserver):
    def __init__(self, model, controller) -> None:
        super().__init__()
        self.model = model

        self.model.register_rgb_observer(self)
        self.model.register_blink_observer(self)

        self.controller = controller
        self.controls = None

    def create_view(self) -> None:
        self.geometry('256x256')
        self.title('View')
        self.configure(background=INIT_COLOR)

        self.label = tk.Label(
            self, text=INIT_COLOR, background=INIT_COLOR
        )
        self.label.pack()

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, side="bottom")
        self.control_button = Button(
            frame, text='Controls', command=self.open_controls,
        )
        self.control_button.pack(side="bottom")

    def create_menu(self) -> None:
        menu = tk.Menu(self)
        self.config(menu=menu)
        self.playback_menu = tk.Menu(menu)
        self.playback_menu.add_command(
            label="Start", command=self.controller.start
        )
        self.playback_menu.add_command(
            label="Stop", command=self.controller.stop
        )
        self.playback_menu.add_separator()
        self.playback_menu.add_command(label="Quit", command=self.destroy)
        menu.add_cascade(label="Play", menu=self.playback_menu)

    def close_controls(self) -> None:
        self.controls.destroy()
        self.control_button.config(state=tk.NORMAL)
        self.controls = None

    def open_controls(self) -> None:
        self.control_button.config(state=tk.DISABLED)

        self.controls = tk.Toplevel(self)
        self.controls.geometry('256x96')
        self.controls.title('Controls')
        self.controls.resizable(0,0)

        self.entry = tk.Entry(self.controls)
        self.entry.pack(expand=True)

        Button(
            self.controls,
            text='Set',
            command=lambda: self.controller.set_rgb(self.entry.get())
        ).pack()

        frame = tk.Frame(self.controls)
        frame.pack(side=tk.BOTTOM, expand=True)
        Button(
            frame ,
            text='-',
            command=lambda: self.controller.decrease_rgb()
        ).pack(side=tk.LEFT)

        Button(
            frame ,
            text='+',
            command=lambda: self.controller.increase_rgb()
        ).pack(side=tk.RIGHT)

        self.controls.protocol("WM_DELETE_WINDOW", self.close_controls)

    # observer
    def rgb_update(self) -> None:
        rgb = self.model.get_rgb()
        self.configure(background=rgb)
        self.label.configure(text=rgb, background=rgb)
        self.update_idletasks()

    # observer
    def blink_update(self) -> None:
        self.configure(background=BLINK_COLOR)
        self.label.configure(background=BLINK_COLOR)
        self.update_idletasks()

    def enable_start_menu_item(self) -> None:
        self.playback_menu.entryconfig("Start", state="normal")

    def disable_start_menu_item(self) -> None:
        self.playback_menu.entryconfig("Start", state="disabled")

    def enable_stop_menu_item(self) -> None:
        self.playback_menu.entryconfig("Stop", state="normal")

    def disable_stop_menu_item(self) -> None:
        self.playback_menu.entryconfig("Stop", state="disabled")

    def show_error(self) -> None:
        if self.controls:
            self.entry.delete(0, 'end')
            self.entry.insert(0, f'HEX numbers only: {INIT_COLOR}')

class ColorController:
    def __init__(self, model) -> None:
        self.model = model

        self.view = ColorView(model, self)
        self.view.create_view()
        self.view.create_menu()

        self.view.disable_stop_menu_item()
        self.view.enable_start_menu_item()

        self.view.mainloop()

    def start(self) -> None:
        self.view.disable_start_menu_item()
        self.view.enable_stop_menu_item()
        self.model.on()

    def stop(self) -> None:
        self.view.disable_stop_menu_item()
        self.view.enable_start_menu_item()
        self.model.off()

    def increase_rgb(self) -> None:
        rgb = int(self.model.get_rgb().replace('#', ''), base=16) + 8
        hrgb = f"#{rgb.to_bytes(3, byteorder='big').hex()}"
        self.model.set_rgb(hrgb)

    def decrease_rgb(self) -> None:
        rgb = int(self.model.get_rgb().replace('#',''), base=16) - 8
        if rgb > 0:
            hrgb = f"#{rgb.to_bytes(3, byteorder='big').hex()}"
            self.model.set_rgb(hrgb)
        else:
            self.model.set_rgb(BLINK_COLOR)

    def set_rgb(self, rgb: str) -> None:
        if re.match('^#\w{6}', rgb):
            self.model.set_rgb(rgb)
        else:
            self.view.show_error()


class HeartController:
    def __init__(self, model) -> None:
        self.model = model

        view = ColorView(model, self)
        view.create_view()
        view.create_menu()

        view.disable_stop_menu_item()
        view.disable_start_menu_item()

        view.mainloop()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def increase_rgb(self) -> None:
        pass

    def decrease_rgb(self) -> None:
        pass

    def set_rgb(self, rgb: str) -> None:
        pass


if __name__ == '__main__':
    color_model = ColorModel()
    color_controller = ColorController(color_model)

    # heart_model = HeartAdapter(HeartModel())
    # heart_controller = HeartController(heart_model)

