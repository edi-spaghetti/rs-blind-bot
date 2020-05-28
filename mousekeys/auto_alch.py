
import sys
import time
import keyboard
import random

from ..utils import utils
from qndnmz import constants


class HighAlch:

    DONE = 0

    CASTING_SPEED = constants.TICK * 5

    def __init__(self, repeat=-1, current_tab='MAGIC'):

        # aoi should be overlap between high alc spell and inv 11
        self.aoi = utils.get_aoi()['0']
        self.repeats = repeat
        self.alched_at = None
        self.current_tab = current_tab

        print('loaded')

    def run(self):

        alchs_remaining = self.repeats
        print('running')

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


    @property
    def can_cast(self):
        if self.alched_at is None:
            return False
        else:
            return time.time() - self.alched_at > self.CASTING_SPEED

    @property
    def time_til_can_cast(self):
        return max(0, (self.alched_at + self.CASTING_SPEED) - time.time())

    def clean_print(self, statement, max=25):
        sys.stdout.write('\r')
        statement = statement + ' ' * (max - len(statement))
        sys.stdout.write(statement)
        sys.stdout.flush()

    def exit(self):
        self.clean_print('job done')
        exit(self.DONE)
