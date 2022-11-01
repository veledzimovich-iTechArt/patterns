#!/usr/bin/env python3

import random
import re
import sys
from flask import (
    current_app,
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from flask_socketio import SocketIO, emit

from models import (
    ColorModel, RGBObserver, BlinkObserver, INIT_COLOR, BLINK_COLOR
)

print('\nMVC - Model(observer) Controller(create view) View(strategy)')

class WebView(Flask, RGBObserver, BlinkObserver):

    def __init__(self, *args, model, controller, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model = model
        self.controller = controller

        self.model.register_rgb_observer(self)
        self.model.register_blink_observer(self)

        self.config['SECRET_KEY'] = 'secret_key'
        self.socketio = SocketIO(self)
        self.add_url_rule(
            '/', view_func=self.index
        )
        self.add_url_rule(
            '/controls', view_func=self.controls, methods=['POST']
        )
        self.add_url_rule(
            '/switch', view_func=self.switch, methods=['POST']
        )
        self.start_btn = False
        self.stop_btn = False
        self.error = ""
    def execute(self):
        self.socketio.run(self, debug=True, host='0.0.0.0', port=5000)

    def blink_update(self):
        with self.app_context():
            r = lambda: random.randint(0,255)
            color = f'#{r():02X}{r():02X}{r():02X}'
            self.socketio.emit('blink', {'color': color})

    def rgb_update(self):
        rgb = self.model.get_rgb()
        with self.app_context():
            self.socketio.emit('rgb', {'color': rgb})

    def index(self):
        return render_template(
            'index.html',
            color=self.model.get_rgb(),
            error=self.error,
            start_disabled=self.start_btn,
            stop_disabled=self.stop_btn
        )

    def controls(self):
        if request.form.get('increase') == '>>':
            self.controller.increase_rgb()
        elif request.form.get('decrease') == '<<':
            self.controller.decrease_rgb()
        elif request.form.get('set') == 'Set':
            try:
                self.controller.set_rgb(request.form.get('color'))
            except Exception:
                self.error = f'HEX numbers only: {INIT_COLOR}'
                redirect(url_for('index'), 304)
        return redirect(url_for('index'), 301)


    def switch(self):
        if request.form.get('on') == 'On':
            self.controller.start()
        elif request.form.get('off') == 'Off':
            self.controller.stop()
        return redirect(url_for('index'), 301)

    def enable_start_menu_item(self) -> None:
        self.start_btn = False

    def disable_start_menu_item(self) -> None:
        self.start_btn = True

    def enable_stop_menu_item(self) -> None:
        self.stop_btn = False

    def disable_stop_menu_item(self) -> None:
        self.stop_btn = True


class WebController:
    def __init__(self, model) -> None:
        self.model = model
        self.view = WebView('Web View', model=model, controller=self)
        self.view.disable_stop_menu_item()
        self.view.enable_start_menu_item()
        self.view.execute()

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
            raise Exception()


if __name__ == '__main__':
    color_model = ColorModel()
    web_controller = WebController(color_model)


