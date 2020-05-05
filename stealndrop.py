

import sys
import time
import random
import pyautogui
import utils
import keyboard
import json


with open(r'C:\Users\Edi\Desktop\programming\qndnmz\data\aoi.json', 'r') as f:
    aoi = json.load(f)

shift_down = False
respawn_time = 2.4


while True:

    if utils.on_off_state():

        utils.click_aoi(aoi['0'])

        # wait for loot to appear in inv
        wait_inv = utils.wait_and_click(1.2, 1.8, click=False)

        pyautogui.keyDown('Shift')

        utils.move_to_index(0)
        wait_click = utils.wait_and_click(0.08, 0.15)

        pyautogui.keyUp('Shift')

        reaction_time = utils.map_between(random.random(), 0.15, 0.2)

        time.sleep((respawn_time - (wait_click + wait_inv)) + reaction_time)

    else:

        time.sleep(0.1)
