import argparse
import logging.config
import threading

from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener
from SequenceFileReader import *
from pyclick.humanclicker import HumanClicker
from pyautogui import *

logging.config.fileConfig('logger.config')


class SequenceExecutor(threading.Thread):

    def __init__(self, filename):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.reader = SequenceFileReader()
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName(self.__class__.__name__)

    def smooth_scroll(self, hc, e):

        max_length = 6
        between_delay = 0.5

        hc.move((e.x, e.y), e.delay)

        times = abs(e.dy) // max_length
        rest = abs(e.dy) % max_length

        for i in range(0, times):
            if e.dy > 0:
                scroll(max_length, e.x, e.y)
            else:
                scroll(-max_length, e.x, e.y)
            sleep(between_delay)

        if e.dy > 0:
            scroll(rest, e.x, e.y)
        else:
            scroll(-rest, e.x, e.y)

        sleep(between_delay)

    def run(self) -> None:

        self.logger.info("Starting execution: %s", self.filename)

        event_list = self.reader.read_sequence_from_file(self.filename)
        event_list.sort(key=lambda x: x.order, reverse=False)

        mouse = HumanClicker()

        for e in event_list:
            if e.event == EventType.BUTTON_LEFT.value:
                mouse.move((e.x, e.y), e.delay)
                leftClick(e.x, e.y)
            elif e.event == EventType.BUTTON_RIGHT.value:
                mouse.move((e.x, e.y), e.delay)
                rightClick(e.x, e.y)
            elif e.event == EventType.SCROLL.value:
                self.smooth_scroll(mouse, e)
            elif e.event == EventType.MOVE.value:
                mouse.move((e.x, e.y), e.delay)

        self.logger.info("Finished execution: of %s", self.filename)

    def stop(self):
        self._stop()


if __name__ == '__main__':

    logger = logging.getLogger('Main')

    parser = argparse.ArgumentParser(description='Execute sequence from yaml file')
    parser.add_argument('-f', required=True, type=str, help='path to file with sequence to execute')
    args = parser.parse_args()
    filename = args.f

    executor = SequenceExecutor(filename)
    executor.start()

    def on_keyboard_press(key):
        if key == keyboard.Key.esc:
            logger.warning("Execution interrupted by user")
            try:
                executor.stop()
            except AssertionError:
                sys.exit()


    with KeyboardListener(on_press=on_keyboard_press) as keyboard_listener:
        keyboard_listener.join()
