import time
import pyautogui
import keyboard

from utils import utils

EXIT_KEY = 'p'


def capture_bbox():
    xy = []
    xy.extend(pyautogui.mouseinfo.position())
    input('press enter for x2')
    xy.extend(pyautogui.mouseinfo.position())
    print({'x1': xy[0], 'y1': xy[1], 'x2': xy[2], 'y2': xy[3]})


aoi = {
    'bank': {'bbox': {'x1': 865, 'y1': 105, 'x2': 1110, 'y2': 316}, 'sleep': 0.6},
    'close_bank': {'sleep': 0.2, 'func': lambda: keyboard.press('esc')},
    'bank_herb': {'bbox': {'x1': 788, 'y1': 514, 'x2': 816, 'y2': 542}, 'sleep': 0.3},
    'bank_vial': {'bbox': {'x1': 854, 'y1': 511, 'x2': 889, 'y2': 546}, 'sleep': 0.3},
    'deposit_all': {'bbox': {'x1': 1027, 'y1': 717, 'x2': 1065, 'y2': 753}, 'sleep': 0.5},
    'inv_herb2': {'bbox': {'x1': 1668, 'y1': 749, 'x2': 1695, 'y2': 772}, 'sleep': 0.2},
    'inv_vial': {'bbox': {'x1': 1730, 'y1': 747, 'x2': 1758, 'y2': 776}, 'sleep': 0.5},
    'make_all': {'sleep': 9.5, 'func': lambda: keyboard.press('space')},
}

while True:

    for stage in ('bank', 'deposit_all', 'bank_herb', 'bank_vial', 'close_bank',
                  'inv_herb2', 'inv_vial', 'make_all'):

        if keyboard.is_pressed(EXIT_KEY):
            exit(1)

        bbox = aoi[stage].get('bbox')
        func = aoi[stage].get('func')
        if bbox:
            utils.click_aoi(bbox)
        elif func:
            func()

        time.sleep(aoi[stage]['sleep'])

    # open bank
    # deposit unfinished potions
    # withdraw 14 herbs
    # withdraw 14 vials of water
    # close the bank
    # use herb on vial
    # choose menu option make all
    # wait
