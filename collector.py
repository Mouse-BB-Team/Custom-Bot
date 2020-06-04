import sys
import getopt
from screen_collector import *


def print_help():
    print("-h  :  help")
    print("-f  :  filename")
    print("-n  :  sequence name")
    print("-i  :  sequence identifier")
    print("You need to pass all of arguments excepts -h !")


argv = sys.argv

opts = getopt.getopt(argv[1:], 'hf:n:i:')[0]

filename = None
sequence_name = None
sequence_id = None

is_help_requested = False

for o, v in opts:
    if o == '-h':
        print_help()
        is_help_requested = True
        break
    elif o == '-f':
        filename = v
    elif o == '-n':
        sequence_name = v
    elif o == '-i':
        sequence_id = v

if not is_help_requested:

    if filename is not None and sequence_name is not None and sequence_id is not None:

        print("Initialized screen collector for file: {}, sequence name: {}, sequence id: {}".format(filename, sequence_name, sequence_id))
        print("To terminate press ESC")

        ScreenCollector.run(filename, sequence_name, sequence_id)

    else:
        print("Not enough arguments!")
