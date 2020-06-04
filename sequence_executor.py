from file_reader import *
from pyclick.humanclicker import HumanClicker
from pyautogui import *


class SequenceExecutor:
    @staticmethod
    def execute(filename):
        event_list = FileReader.read_from_file(filename)

        hc = HumanClicker()

        for e in event_list:
            if e.event == EventType.BUTTON_LEFT.value:
                hc.move((e.x, e.y), e.delay)
                leftClick(e.x, e.y)
            elif e.event == EventType.BUTTON_RIGHT.value:
                hc.move((e.x, e.y), e.delay)
                rightClick(e.x, e.y)
            elif e.event == EventType.SCROLL.value:
                vscroll(e.dy, e.x, e.y)
                hscroll(e.dx, e.x, e.y)
