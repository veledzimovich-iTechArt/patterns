#!/usr/bin/env python3
import abc
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.message_pump import MessagePumpMeta

from models import (
    HeartAdapter, HeartModel, RGBObserver, BlinkObserver, BLINK_COLOR
)

print('\nMVC - Model(observer) Controller(create view) View(strategy)')

class FinalMeta(type(App), abc.ABCMeta):
    pass

class TermView(App, BlinkObserver, RGBObserver, metaclass=FinalMeta):

    def __init__(self, model, controller) -> None:
        super().__init__()
        self.model = model
        self.controller = controller

        self.model.register_rgb_observer(self)
        self.model.register_blink_observer(self)

        self.stripe = Static()
    def blink_update(self):
        self.stripe.styles.background = BLINK_COLOR

    def rgb_update(self):
        self.stripe.styles.background = self.model.get_rgb()

    def compose(self) -> ComposeResult:
        self.stripe.styles.height = "1fr"
        self.stripe.styles.background = self.model.get_rgb()
        yield self.stripe

class TermController:
    def __init__(self, model) -> None:
        self.model = model

        view = TermView(model, self)
        view.run()

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
    heart_model = HeartAdapter(HeartModel())
    heart_controller = TermController(heart_model)
