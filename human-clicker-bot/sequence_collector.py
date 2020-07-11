import argparse
import logging.config
from screen_collector import ScreenCollector

logging.config.fileConfig('logger.config')


class SequenceCollector:
    def __init__(self, filename, sequence_name, sequence_id):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.sequence_name = sequence_name
        self.sequence_id = sequence_id

    def run(self):
        screen_collector = ScreenCollector(self.filename, self.sequence_name, self.sequence_id)
        screen_collector.run()


if __name__ == '__main__':
    logger = logging.getLogger('Main')

    parser = argparse.ArgumentParser("Run the collection of the sequence")
    parser.add_argument('-f', help='File name to save the sequence', type=str, required=True)
    parser.add_argument('-n', help='Name of the sequence', type=str, required=True)
    parser.add_argument('-i', help='Sequence identifier', type=str, required=True)
    args = parser.parse_args()
    filename = args.f
    sequence_name = args.n
    sequence_id = args.i

    if filename is not None and sequence_name is not None and sequence_id is not None:
        sequence_collector = SequenceCollector(filename, sequence_name, sequence_id)
        logger.info("Initialized screen collector for file: %s, sequence name: %s, sequence id: %s", filename, sequence_name, sequence_id)
        logger.info("To terminate press ESC")
        sequence_collector.run()
