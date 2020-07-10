import yaml
from typing import List
from Event import *


class FileSaver:
    @staticmethod
    def save_to_file(filename: str, sequence_name: str, sequence_id, events: List[Event]):

        event_list = []

        no = 1

        for e in events:
            event_list.append({'element': {'x': e.x, 'y': e.y, 'dx': e.dx, 'dy': e.dy, 'delay': e.delay, 'event': e.event, 'ord': no}})
            no += 1

        content = {'name': sequence_name, 'id': sequence_id, 'sequence': event_list, 'sequence_length': no - 1}

        with open(filename, 'w') as file:
            yaml.dump(content, file)

