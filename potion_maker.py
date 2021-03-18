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
    'bank': {'bbox': {'x1': -1378, 'y1': 205, 'x2': -1268, 'y2': 378}, 'sleep': 0.6},
    'close_bank': {'sleep': 0.2, 'func': lambda: keyboard.press('esc')},
    'bank_herb': {'bbox': {'x1': -1400, 'y1': 457, 'x2': -1377, 'y2': 479}, 'sleep': 0.3},
    'bank_vial': {'bbox': {'x1': -1350, 'y1': 459, 'x2': -1328, 'y2': 481}, 'sleep': 0.3},
    'deposit_all': {'bbox': {'x1': -1235, 'y1': 594, 'x2': -1210, 'y2': 617}, 'sleep': 0.5},
    'inv_herb2': {'bbox': {'x1': -806, 'y1': 618, 'x2': -793, 'y2': 635}, 'sleep': 0.2},
    'inv_vial': {'bbox': {'x1': -764, 'y1': 616, 'x2': -749, 'y2': 632}, 'sleep': 0.5},
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
