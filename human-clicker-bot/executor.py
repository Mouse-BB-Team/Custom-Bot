import getopt
from sequence_executor import *


def print_help():
    print("-h  :  help")
    print("-f  :  filename")


argv = sys.argv

opts = getopt.getopt(argv[1:], 'hf:')[0]

filename = None

is_help_requested = False

for o, v in opts:
    if o == '-h':
        print_help()
        is_help_requested = True
        break
    elif o == '-f':
        filename = v

if not is_help_requested:
    SequenceExecutor.execute(filename)

