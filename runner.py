import getopt
import os
import sys
import time
import yaml
from pynput import keyboard
import sequence_executor as executor
from pynput.keyboard import Listener as KeyboardListener


def run_scenarios(directory='scenarios'):
    filenames = os.listdir(directory)

    filenames[:] = [directory + '/' + file for file in filenames]

    file_id = list()

    for file in filenames:
        with open(file) as f:
            file_id.append((file, int(yaml.load(f, Loader=yaml.FullLoader)['id'])))

    sorted_list = sorted(file_id, key=lambda k: k[1])
    files = [name[0] for name in sorted_list]

    keyboard_listener = None

    def on_keyboard_press(key):
        if key == keyboard.Key.esc:
            keyboard_listener.stop()

    keyboard_listener = KeyboardListener(on_press=on_keyboard_press)
    keyboard_listener.start()

    for file in files:
        executor.SequenceExecutor.execute(file)
        print("XD")
        time.sleep(5)
        if not keyboard_listener.is_alive():
            sys.exit()


if __name__ == '__main__':

    def print_help():
        print("-h  :  help")
        print("-d  :  directory")


    argv = sys.argv

    opts = getopt.getopt(argv[1:], 'hd:')[0]

    root_dir = None

    is_help_requested = False

    for o, v in opts:
        if o == '-h':
            print_help()
            is_help_requested = True
            break
        elif o == '-d':
            root_dir = v

    if not is_help_requested:
        run_scenarios(directory=root_dir)
