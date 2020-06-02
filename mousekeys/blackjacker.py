

import keyboard
import pyautogui
import time
import random

from ..utils import utils


class BlackJacker:

    OFFSET = {
        'knockout': {
            'x1': -184, 'y1': 99, 'x2': 183, 'y2': 114
        },
        'pickpocket': {
            'x1': -186, 'y1': 54, 'x2': 183, 'y2': 69
        }
    }

    def __init__(self, mode='hotkey'):
        self.mode = mode
        self.knockout_at = None
        self.pickpocket_at = None
        self.num_pockets_picked = 0
        self.pos = None

        print(f'loaded in {mode} mode')

    def run(self):

        print('running')

        while True:

            if utils.on_off_state():

                if self.mode == 'hotkey':
                    self.hotkey_blackjack()
                elif self.mode == 'auto':
                    self.auto_blackjack()
                else:
                    raise NotImplementedError(f'invalid mode {self.mode}')
            else:
                utils.clean_print('disabled')
                time.sleep(0.01)

    def do_action(self, action_name):

        pos = pyautogui.position()
        ox, oy = pos.x, pos.y

        # right click npc for menu
        utils.wait_and_click(
            start=0.02, stop=0.03,
            click=False, right=True)

        # wait for menu to open
        time.sleep(0.05)

        bbox = self.get_bbox(action_name, ox, oy)
        utils.click_aoi(bbox, speed=0.5)

        # nx, ny = utils.distribute_normally(
        #     x1=ox-5,y1=oy-5, x2=ox+5, y2=oy+5
        # )

        pyautogui.moveTo(ox, oy)

    def get_bbox(self, item, x, y):

        return dict(
            x1=self.OFFSET[item]['x1'] + x,
            y1=self.OFFSET[item]['y1'] + y,
            x2=self.OFFSET[item]['x2'] + x,
            y2=self.OFFSET[item]['y2'] + y
        )

    def hotkey_blackjack(self):
        if keyboard.is_pressed('c'):
            utils.clean_print('knocking out')
            self.do_action('knockout')
        elif keyboard.is_pressed('v'):
            utils.clean_print('picking pocket')
            self.do_action('pickpocket')
        elif keyboard.is_pressed('x'):
            utils.clean_print('knock picking')
            self.do_action('knockout')
            time.sleep(0.4)
            self.do_action('pickpocket')
        else:
            utils.clean_print('sleeping')
            time.sleep(0.01)

    def auto_blackjack(self):

        if not self.knockout_at:
            self.knockout_at = time.time()
            self.do_action('knockout')
            time.sleep(0.6)
        else:
            if time.time() > self.knockout_at + (1.2 * self.num_pockets_picked) + 1.2:
                self.do_action('pickpocket')
                self.num_pockets_picked += 1

                # start again once we've done two
                if self.num_pockets_picked == 2:
                    self.knockout_at = None
                    self.num_pockets_picked = 0
                    time.sleep(1.2)
            else:
                utils.clean_print('waiting')
