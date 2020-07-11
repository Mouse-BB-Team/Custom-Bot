import yaml
import logging.config
from typing import List
from event import *

logging.config.fileConfig('logger.config')


class SequenceFileReader:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def read_sequence_from_file(self, filename: str) -> List[Event]:

        with open(filename) as file:
            self.logger.info("Reading file: %s", filename)
            yaml_properties = yaml.load(file, Loader=yaml.FullLoader)

        event_list = []

        for sequence in yaml_properties['sequence']:
            e = sequence['element']
            event_list.append(Event(e['x'], e['y'], e['dx'], e['dy'], e['delay'], e['event'], e['ord']))

        return event_list
