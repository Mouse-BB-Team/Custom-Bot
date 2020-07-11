import yaml
from typing import List
from event import *


class FileReader:
    @staticmethod
    def read_from_file(filename: str) -> List[Event]:

        with open(filename) as file:
            read_list = yaml.load(file, Loader=yaml.FullLoader)

        event_list = []

        for element in read_list['sequence']:
            e = element['element']
            event_list.append(Event(e['x'], e['y'], e['dx'], e['dy'], e['delay'], e['event'], e['ord']))

        return event_list
