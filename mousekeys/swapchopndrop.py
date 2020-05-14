
import time
import pyautogui
from ..utils import utils
import keyboard


class Lumberjack:

    EXIT_KEY = '-'
    loop = list(range(0, 27, 4)) + list(range(25, 0, -4)) + list(range(2, 27, 4)) + list(range(27, 0, -4))
    inv = list(range(27))

    def __init__(self, slots):
        self.trees = utils.get_aoi()
        self.slots = utils.int_or_list(slots)
        print('ready')

    @property
    def inventory(self):
        if isinstance(self.slots, int):
            return list(range(self.slots))
        elif isinstance(self.slots, list):
            return self.slots
        else:
            raise ValueError

    def run(self):

        print('running')

        while True:

            if pyautogui.position().x < 2880:

                if keyboard.is_pressed('1'):
                    utils.click_aoi(self.trees['0'])
                elif keyboard.is_pressed('2'):
                    utils.click_aoi(self.trees['1'])
                elif keyboard.is_pressed('0'):
                    self.drop_all()
                elif keyboard.is_pressed('3'):
                    self.drop_one()
                elif keyboard.is_pressed('4'):
                    self.add_nest()
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)

    def add_nest(self):
        if isinstance(self.slots, int):
            self.slots -= 1
            print(f'removing inventory item at index {self.slots}')
        elif isinstance(self.slots, list):
            i = self.slots.pop(-1)
            print(f'removing inventory item at index {i}')
        else:
            raise ValueError

        time.sleep(0.5)

    def test_shift(self):
        utils.move_to_index(1)
        time.sleep(1)
        pyautogui.keyDown('Shift')
        time.sleep(1)
        pyautogui.keyUp('Shift')

    def drop_one(self):
        utils.move_to_index(0)
        pyautogui.keyDown('Shift')
        # utils.wait_and_click(0.015, 0.03)

        import random
        wait_period = utils.map_between(random.random(), 0.015, 0.03)
        pyautogui.mouseDown()
        time.sleep(wait_period)
        pyautogui.mouseUp()

        pyautogui.keyUp('Shift')

    def drop_all(self):

        print(f'dropping {len(self.inventory)}')

        utils.move_to_index(0)
        time.sleep(1)
        pyautogui.keyDown('Shift')

        for i in self.inventory:

            # if we have to pause here then something went wrong
            # probably best just to restart!
            if keyboard.is_pressed(self.EXIT_KEY):
                pyautogui.keyUp('Shift')
                exit(1)

            # pyautogui.keyDown('Shift')
            utils.move_to_index(i)
            utils.wait_and_click(0.015, 0.03)

        # lift up shift
        pyautogui.keyUp('Shift')
