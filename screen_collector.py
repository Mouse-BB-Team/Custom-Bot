from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller
from pynput.keyboard import Listener as KeyboardListener
from pynput import keyboard
from pynput import mouse
from random import uniform
from file_saver import *
from math import floor


class ScreenCollector:
    @staticmethod
    def run(filename, sequence_name, sequence_id):
        mouse_controller = Controller()

        def random_delay():
            return uniform(2, 3)

        events = []

        def on_click(x, y, button, pressed):
            if pressed:
                if button == mouse.Button.left:
                    events.append(Event(floor(x), floor(y), 0, 0, random_delay(), EventType.BUTTON_LEFT.value))
                elif button == mouse.Button.right:
                    events.append(Event(floor(x), floor(y), 0, 0, random_delay(), EventType.BUTTON_RIGHT.value))

        def on_scroll(x, y, dx, dy):
            if len(events) > 0:
                previous = events[len(events) - 1]

                if previous.event == EventType.SCROLL.value and previous.dx * dx >= 0 and previous.dy * dy >= 0:
                    previous.dx += dx
                    previous.dy += dy
                else:
                    events.append(Event(floor(x), floor(y), dx, dy, random_delay(), EventType.SCROLL.value))

            else:
                events.append(Event(floor(x), floor(y), dx, dy, random_delay(), EventType.SCROLL.value))

        def on_space_record_move(x, y):
            events.append(Event(floor(x), floor(y), 0, 0, random_delay(), EventType.MOVE.value))

        with MouseListener(on_click=on_click, on_scroll=on_scroll) as mouse_listener:
            def on_keyboard_press(key):
                if key == keyboard.Key.esc:
                    mouse_listener.stop()

                    FileSaver.save_to_file(filename, sequence_name, sequence_id, events)

                    return False

                elif key == keyboard.Key.space:
                    on_space_record_move(*mouse_controller.position)

            with KeyboardListener(on_press=on_keyboard_press) as keyboard_listener:
                keyboard_listener.join()

            mouse_listener.join()
