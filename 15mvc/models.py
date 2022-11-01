import abc
import random
import threading
import time

INIT_COLOR = '#000000'
BLINK_COLOR = '#FFFFFF'

class BeatListener(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def beat_event(self) -> None:
        pass

class Beat:
    def __init__(self, listener: BeatListener):
        self.listener = listener

    def start(self) -> None:
        self.event = threading.Event()
        self.thread = threading.Thread(
            target=self.beat_loop, args=(self.event,), daemon=True
        )
        self.thread.start()

    def stop(self) -> None:
        self.event.set()

    def beat_loop(self, event: threading.Event) -> None:
        while True:
            if event.is_set():
                break
            time.sleep(0.1)
            self.listener.beat_event()



class BaseColorModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def on(self) -> None:
        pass

    @abc.abstractmethod
    def off(self) -> None:
        pass

    @abc.abstractmethod
    def set_rgb(rgb: str) -> None:
        pass

    @abc.abstractmethod
    def get_rgb() -> str:
        pass

    @abc.abstractmethod
    def register_blink_observer(blink_observer) -> None:
        pass

    @abc.abstractmethod
    def remove_blink_observer(blink_observer) -> None:
        pass

    @abc.abstractmethod
    def register_rgb_observer(rgb_observer) -> None:
        pass

    @abc.abstractmethod
    def remove_rgb_observer(rgb_observer) -> None:
        pass


class BlinkObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def blink_update(self) -> None:
        pass

class RGBObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rgb_update(self) -> None:
        pass

class ColorObserverMixin:
    def register_blink_observer(self, blink_observer) -> None:
        self.blink_observers.add(blink_observer)

    def remove_blink_observer(self, blink_observer) -> None:
        self.blink_observers.remove(blink_observer)

    def notify_blink_observers(self) -> None:
        for observer in self.blink_observers:
            observer.blink_update()

    def register_rgb_observer(self, rgb_observer) -> None:
        self.rgb_observers.add(rgb_observer)

    def remove_rgb_observer(self, rgb_observer) -> None:
        self.rgb_observers.remove(rgb_observer)

    def notify_rgb_observers(self) -> None:
        for observer in self.rgb_observers:
            observer.rgb_update()


class ColorModel(ColorObserverMixin, BaseColorModel, BeatListener):
    def __init__(self) -> None:
        self.blink_observers: [BlinkObserver] = set()
        self.rgb_observers: [RGBObserver] = set()

        self.rgb: str = INIT_COLOR

        self.beat = Beat(self)

    def beat_event(self) -> None:
        self.notify_blink_observers()
        time.sleep(0.5)
        self.set_rgb(self.get_rgb())

    # manage model by controler
    def on(self) -> None:
        self.set_rgb(self.get_rgb())
        self.beat.start()

    def off(self) -> None:
        self.set_rgb(INIT_COLOR)
        self.beat.stop()

    def set_rgb(self, rgb: str) -> None:
        self.rgb = rgb
        self.notify_rgb_observers()

    # get & update data by controler and view
    def get_rgb(self) -> str:
        return self.rgb


class HeartModel(ColorObserverMixin):
    def __init__(self) -> None:
        self.blink_observers: [BlinkObserver] = set()
        self.rgb_observers: [RGBObserver] = set()

        self.beat = Beat(self)
        self.beat.start()

    def beat_event(self) -> None:
        self.notify_blink_observers()
        time.sleep(random.random())
        self.notify_rgb_observers()

    def get_heart_color(self) -> str:
        return "#FF0000"


class HeartAdapter(BaseColorModel):
    def __init__(self, heart: HeartModel) -> None:
        self.heart = heart

    def on(self) -> None:
        pass

    def off(self) -> None:
        pass

    def set_rgb(self, rgb: str) -> None:
        pass

    # get & update data by controler and view
    def get_rgb(self) -> str:
        return self.heart.get_heart_color()

    def register_blink_observer(self, blink_observer) -> None:
        self.heart.register_blink_observer(blink_observer)

    def remove_blink_observer(self, blink_observer) -> None:
        self.heart.remove_blink_observer(blink_observer)

    def notify_blink_observers(self) -> None:
        self.heart.notify_blink_observers()

    def register_rgb_observer(self, rgb_observer) -> None:
        self.heart.register_rgb_observer(rgb_observer)

    def remove_rgb_observer(self, rgb_observer) -> None:
        self.heart.remove_rgb_observer(rgb_observer)

    def notify_rgb_observers(self) -> None:
        self.heart.notify_rgb_observers()
