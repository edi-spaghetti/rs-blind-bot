
import sys
import time
import random
import pyautogui
import utils
import keyboard

loop = list(range(0, 27, 4)) + list(range(25, 0, -4)) + list(range(2, 27, 4)) + list(range(27, 0, -4))

EXIT_KEY = 'p'

# dictionary of areas of interest
willows = {
    'left': {
        'x1': 595,
        'y1': 460,
        'x2': 726,
        'y2': 552
    },
    'right': {
        'x1': 837,
        'y1': 451,

        'x2': 959,
        'y2': 543
    },
}

while True:

    if keyboard.is_pressed('j'):

        utils.click_aoi(willows['left'])

    elif keyboard.is_pressed('k'):

        utils.click_aoi(willows['right'])

    elif keyboard.is_pressed('l'):

        # hold down shift
        pyautogui.keyDown('Shift')

        # drop everything
        for i in loop:

            # if we have to pause here then something went wrong
            # probably best just to restart!
            if keyboard.is_pressed(EXIT_KEY):
                pyautogui.keyUp('Shift')
                exit(1)

            utils.move_to_index(i)
            utils.wait_and_click(0.05, 0.08)
            # utils.wait_and_click(0.01, 0.1, click=False)

        # lift up shift
        pyautogui.keyUp('Shift')

    else:
        time.sleep(0.2)

