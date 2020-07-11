import logging.config
from pyautogui import *
from event import EventType
from file_saver import *
from math import floor, sqrt
from pynput import keyboard
from pynput import mouse
from random import uniform
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller
from pynput.keyboard import Listener as KeyboardListener

logging.config.fileConfig('logger.config')


class ScreenCollector:
    def __init__(self, filename, sequence_name, sequence_id):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.sequence_name = sequence_name
        self.sequence_id = sequence_id
        self.p_prev: (int, int) = position()
        self.mouse_controller = Controller()
        self.events = list()

    def compute_delay(self, p: (int, int)):

        min_deviation = 0.9
        max_deviation = 1.0
        bias = 0.4

        def distance(p1: (int, int), p2: (int, int)):
            return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        self.logger.info("%f", distance(p, self.p_prev))
        self.logger.info("%s%s", p, self.p_prev)
        return distance(p, self.p_prev) * uniform(min_deviation, max_deviation) * 1e-3 + bias

    def on_click(self, x, y, button, pressed):

        p = (floor(x), floor(y))

        if pressed:
            if button == mouse.Button.left:
                self.events.append(
                    Event(p[0], p[1], 0, 0, self.compute_delay(p), EventType.BUTTON_LEFT.value))
            elif button == mouse.Button.right:
                self.events.append(
                    Event(p[0], p[1], 0, 0, self.compute_delay(p),
                          EventType.BUTTON_RIGHT.value))
        self.p_prev = p

    def on_scroll(self, x, y, dx, dy):

        p = (floor(x), floor(y))

        if len(self.events) > 0:
            previous = self.events[len(self.events) - 1]

            if previous.event == EventType.SCROLL.value and previous.dx * dx >= 0 and previous.dy * dy >= 0:
                previous.dx += dx
                previous.dy += dy
            else:
                self.events.append(
                    Event(p[0], p[1], dx, dy, self.compute_delay(p), EventType.SCROLL.value))
        else:
            self.events.append(
                Event(p[0], p[1], dx, dy, self.compute_delay(p), EventType.SCROLL.value))

        self.p_prev = p

    def on_caps_lock_record_move(self, x, y):

        p = (floor(x), floor(y))

        self.events.append(Event(p[0], p[1], 0, 0, self.compute_delay(p), EventType.MOVE.value))

        self.p_prev = p

    def run(self):

        with MouseListener(on_click=self.on_click, on_scroll=self.on_scroll) as mouse_listener:
            def on_keyboard_press(key):
                if key == keyboard.Key.esc:
                    mouse_listener.stop()

                    FileSaver.save_to_file(self.filename, self.sequence_name, self.sequence_id, self.events)

                    return False

                elif key == keyboard.Key.caps_lock:
                    self.on_caps_lock_record_move(*self.mouse_controller.position)

            with KeyboardListener(on_press=on_keyboard_press) as keyboard_listener:
                keyboard_listener.join()

            mouse_listener.join()
