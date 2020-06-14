
import pyautogui
import keyboard
import time

from ..utils import utils


class AutoCaster:

    CAST_KEY = 'c'
    MULTI_CAST_KEY = 'x'

    def __init__(self, spell_name=None):

        self.multi_cast = False
        self.spell_name = spell_name or 'spell'
        self.aoi = utils.get_aoi()['0']
        print(f'loaded with {self.spell_name}')

    def run(self):

        print('running')

        while True:

            if utils.on_off_state():

                if keyboard.is_pressed(self.CAST_KEY):
                    self.cast_spell()
                elif keyboard.is_pressed(self.MULTI_CAST_KEY):
                    self.multi_cast = True
                elif self.multi_cast:
                    self.cast_spell()
                else:
                    utils.clean_print('waiting')
                    time.sleep(0.01)
            else:
                self.multi_cast = False
                utils.clean_print('disabled')
                time.sleep(0.01)

    def cast_spell(self):
        utils.clean_print(f'arming {self.spell_name}')

        # keep track of where to cast the spell
        pos = pyautogui.position()
        x = pos.x
        y = pos.y

        # click the spell icon in spellbook
        utils.click_aoi(self.aoi)

        utils.clean_print(f'casting {self.spell_name}')

        # go back to original mouse position
        pyautogui.moveTo(x, y)

        # wait a bit for game to catch up
        time.sleep(0.1)

        # cast the spell
        utils.wait_and_click()
