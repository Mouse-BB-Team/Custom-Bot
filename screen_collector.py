from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller
from pynput.keyboard import Listener as KeyboardListener
from pynput import keyboard
from pynput import mouse
from random import uniform
from pyautogui import *
from file_saver import *
from math import floor, sqrt


class ScreenCollector:
    p_prev = position()

    @staticmethod
    def run(filename, sequence_name, sequence_id):
        mouse_controller = Controller()

        def compute_delay(p: (int, int), p_prev: (int, int)):

            min_deviation = 0.9
            max_deviation = 1.0
            bias = 0.4

            def distance(p1: (int, int), p2: (int, int)):
                print(p1, p2)
                return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            print(distance(p, p_prev))
            return distance(p, p_prev) * uniform(min_deviation, max_deviation) * 1e-3 + bias

        events = []

        def on_click(x, y, button, pressed):

            p = (floor(x), floor(y))

            if pressed:
                if button == mouse.Button.left:
                    events.append(Event(p[0], p[1], 0, 0, compute_delay(p, ScreenCollector.p_prev), EventType.BUTTON_LEFT.value))
                elif button == mouse.Button.right:
                    events.append(Event(p[0], p[1], 0, 0, compute_delay(p, ScreenCollector.p_prev), EventType.BUTTON_RIGHT.value))

            ScreenCollector.p_prev = p

        def on_scroll(x, y, dx, dy):

            p = (floor(x), floor(y))

            if len(events) > 0:
                previous = events[len(events) - 1]

                if previous.event == EventType.SCROLL.value and previous.dx * dx >= 0 and previous.dy * dy >= 0:
                    previous.dx += dx
                    previous.dy += dy
                else:
                    events.append(Event(p[0], p[1], dx, dy, compute_delay(p, ScreenCollector.p_prev), EventType.SCROLL.value))

            else:
                events.append(Event(p[0], p[1], dx, dy, compute_delay(p, ScreenCollector.p_prev), EventType.SCROLL.value))

            ScreenCollector.p_prev = p

        def on_space_record_move(x, y):

            p = (floor(x), floor(y))

            events.append(Event(p[0], p[1], 0, 0, compute_delay(p, ScreenCollector.p_prev), EventType.MOVE.value))

            ScreenCollector.p_prev = p

        with MouseListener(on_click=on_click, on_scroll=on_scroll) as mouse_listener:
            def on_keyboard_press(key):
                if key == keyboard.Key.esc:
                    mouse_listener.stop()

                    FileSaver.save_to_file(filename, sequence_name, sequence_id, events)

                    return False

                elif key == keyboard.Key.caps_lock:
                    on_space_record_move(*mouse_controller.position)

            with KeyboardListener(on_press=on_keyboard_press) as keyboard_listener:
                keyboard_listener.join()

            mouse_listener.join()
