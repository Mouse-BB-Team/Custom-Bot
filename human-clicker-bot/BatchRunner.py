import logging
import logging.config
import argparse
import os
import sys
import threading
import time
import yaml
from SequenceExecutor import SequenceExecutor
from pynput import keyboard
from pynput.keyboard import Listener as KeyboardListener

logging.config.fileConfig('logger.config')


class BatchRunner(threading.Thread):

    def __init__(self, delay, directory):
        self.logger = logging.getLogger(self.__class__.__name__)

        if directory is None:
            self.directory = '../scenarios'
        else:
            self.directory = directory

        if delay is None:
            self.delay = 5
        else:
            self.delay = delay

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName(self.__class__.__name__)

    def run(self) -> None:
        filenames = os.listdir(self.directory)

        filenames[:] = [self.directory + '/' + file for file in filenames]

        paths_order = list()

        for file in filenames:
            with open(file) as f:
                paths_order.append((file, int(yaml.load(f, Loader=yaml.FullLoader)['id'])))

        paths_order = sorted(paths_order, key=lambda k: k[1])
        files = [path_order[0] for path_order in paths_order]

        for file in files:
            executor = SequenceExecutor(file)
            executor.start()
            executor.join()
            self.logger.info("Sleeping %ss ...", delay)
            time.sleep(self.delay)

    def stop(self):
        self._stop()


if __name__ == '__main__':

    logger = logging.getLogger('Main')

    parser = argparse.ArgumentParser(description='Execute batch of yaml sequences from directory')
    parser.add_argument('-d', required=False, type=str, help='director with yaml sequences')
    parser.add_argument('-t', required=False, type=int, help='delay time between execution of sequences')
    args = parser.parse_args()
    root_dir = args.d
    delay = args.t

    runner = BatchRunner(delay, root_dir)
    runner.start()

    logger.info("Batch runner started ...")

    def on_keyboard_press(key):
        if key == keyboard.Key.esc:
            logger.warning("Execution interrupted by user")
            try:
                runner.stop()
            except AssertionError:
                sys.exit()


    with KeyboardListener(on_press=on_keyboard_press) as keyboard_listener:
        keyboard_listener.join()

    logger.info("Batch runner finished execution")
