import yaml
from typing import List
from event import Event


class FileSaver:
    @staticmethod
    def save_to_file(filename: str, sequence_name: str, sequence_id, events: List[Event]):
        event_list = [{'element':
                           {'x': e.x, 'y': e.y, 'dx': e.dx, 'dy': e.dy, 'delay': e.delay, 'event': e.event, 'ord': no}
                       } for no, e in enumerate(events, 1)]

        content = {'name': sequence_name, 'id': sequence_id, 'sequence': event_list, 'sequence_length': len(event_list)}

        with open(filename, 'w') as file:
            yaml.dump(content, file)
