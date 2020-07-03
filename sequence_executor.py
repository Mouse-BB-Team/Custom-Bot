from file_reader import *
from pyclick.humanclicker import HumanClicker
from pyautogui import *


class SequenceExecutor:

    @staticmethod
    def smooth_scroll(hc, e):

        max_length = 6
        between_delay = 0.5

        hc.move((e.x, e.y), e.delay)

        times = abs(e.dy) // max_length
        rest = abs(e.dy) % max_length

        for i in range(0, times):
            if e.dy > 0:
                scroll(max_length, e.x, e.y)
            else:
                scroll(-max_length, e.x, e.y)
            sleep(between_delay)

        if e.dy > 0:
            scroll(rest, e.x, e.y)
        else:
            scroll(-rest, e.x, e.y)

        sleep(between_delay)

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
                SequenceExecutor.smooth_scroll(hc, e)
            elif e.event == EventType.MOVE.value:
                hc.move((e.x, e.y), e.delay)
