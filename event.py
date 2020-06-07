from enum import Enum


class EventType(Enum):
    SCROLL = 'scroll'
    BUTTON_LEFT = 'left-button'
    BUTTON_RIGHT = 'right-button'
    MOVE = 'move'


class Event:
    def __init__(self, x, y, dx, dy, delay, event):
        self.x = x
        self.y = y
        self.delay = delay
        self.event = event
        self.dx = dx
        self.dy = dy
