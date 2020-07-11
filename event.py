from enum import Enum


class EventType(Enum):
    MOVE = 'move'
    BUTTON_LEFT = 'left-button'
    BUTTON_RIGHT = 'right-button'
    SCROLL = 'scroll'


class Event:
    def __init__(self, x, y, dx, dy, delay, event, order=0):
        self.x = x
        self.y = y
        self.delay = delay
        self.event = event
        self.dx = dx
        self.dy = dy
        self.order = order
