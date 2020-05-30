
import sys
import time
import keyboard
import random
import pyautogui

from ..utils import utils
from qndnmz import constants


class HighAlch:

    DONE = 0

    CASTING_SPEED = constants.TICK * 5
    CAST_HOTKEY = 'c'

    def __init__(self, repeat=-1, current_tab='MAGIC', mode='auto'):

        # aoi should be overlap between high alc spell and inv 11
        self.aoi = utils.get_aoi()['0']
        self.repeats = repeat
        self.alched_at = None
        self.current_tab = current_tab
        self.mode = mode

        print(f'loaded in {mode} mode')

    def run(self):

        if self.mode == 'auto':
            self.auto_alch()
        elif self.mode == 'hotkey':
            self.hotkey_alch()

        # while True:
        #
        #     now = time.time()
        #
        #     if not utils.on_off_state():
        #
        #         if alchs_remaining == 0:
        #             self.exit()
        #
        #         elif self.can_cast:
        #
        #         elif self.current_tab == 'MAGIC':
        #
        #

    @property
    def can_cast(self):
        if self.alched_at is None:
            return False
        else:
            return time.time() - self.alched_at > self.CASTING_SPEED

    @property
    def time_til_can_cast(self):
        return max(0, (self.alched_at + self.CASTING_SPEED) - time.time())

    def hotkey_alch(self):
        """
        Casts high alc on item in aoi assuming the magic page is already open
        """
        while True:

            if utils.on_off_state():
                if keyboard.is_pressed(self.CAST_HOTKEY):

                    self.clean_print('casting')

                    # get the original mouse position so we can jump back to it later
                    pos = pyautogui.position()
                    ox, oy = pos.x, pos.y

                    # check if mouse is inside spell area
                    if not utils.mouse_inside(**self.aoi):
                        # move there if not
                        utils.move_to_aoi(**self.aoi)

                    # click the high alc spell
                    select_wait = utils.wait_and_click()

                    # wait for the menu to appear
                    menu_wait = utils.map_between(random.random(), 0.05, 0.15)
                    time.sleep(menu_wait)

                    # cast the spell on the item
                    self.alched_at = time.time()
                    cast_wait = utils.wait_and_click()

                    pyautogui.moveTo(ox, oy)

                else:
                    self.clean_print('sleeping')
                    time.sleep(0.01)
            else:
                self.clean_print('disabled')
                time.sleep(0.01)

    def auto_alch(self):

        print('running')
        alchs_remaining = self.repeats

        if self.current_tab == 'INVENTORY':
            utils.wait_and_click(click=False, key='f')
            time.sleep(utils.map_between(random.random(), 1, 3))
            self.current_tab = 'MAGIC'

        while alchs_remaining != 0:

            # caps lock acts as pause function
            if not utils.on_off_state():

                # check if mouse is inside spell area
                if not utils.mouse_inside(**self.aoi):
                    # move there if not
                    utils.move_to_aoi(**self.aoi)

                # click the high alc spell
                select_wait = utils.wait_and_click()

                # wait for the menu to appear
                menu_wait = 0.1
                time.sleep(menu_wait)

                #  ensure we're not jumping the gun
                if self.alched_at:
                    time.sleep(self.time_til_can_cast)

                # cast the spell on the item
                self.alched_at = time.time()
                cast_wait = utils.wait_and_click()

                alchs_remaining -= 1
                if self.repeats > 0:
                    statement = f'{alchs_remaining} alchs until {self.repeats}'
                else:
                    statement = f'alch {abs(alchs_remaining) - 1}'
                self.clean_print(statement)

                # wait for the menu to flip back
                time.sleep(utils.map_between(random.random(), 0.3, 1.2))

            else:
                self.clean_print(f'sleeping - {alchs_remaining} to go')
                time.sleep(0.01)

    def clean_print(self, statement, max=25):
        sys.stdout.write('\r')
        statement = statement + ' ' * (max - len(statement))
        sys.stdout.write(statement)
        sys.stdout.flush()

    def exit(self):
        self.clean_print('job done')
        exit(self.DONE)
