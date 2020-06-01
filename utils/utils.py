
import pyautogui
import random
import time
import numpy
import keyboard
import json
import os
import sys

from qndnmz import constants


def map_between(value, start, stop):
    """
    Maps a value between start and stop
    E.g. 0.5 between 0 and 100 would return 50
    :param value: Percentage between start and stop
    :type value: float
    :param start: minimum value to return
    :param stop: maximum value to return
    :return: mapped value
    :rtype: float
    """

    return (stop - start) * value + start


def wait_and_click(
        start=constants.CLICK_SPEED_LOWER_BOUND,
        stop=constants.CLICK_SPEED_UPPER_BOUND,
        click=True,
        key=None,
        right=False
):
    """
    Waits and optional clicks in a timely manner
    :param start:
    :param stop:
    :param click:
    :return:
    """

    wait_period = map_between(random.random(), start, stop)

    if sum([bool(p) for p in [click, key, right]]) > 1:
        raise NotImplementedError("Don't do more than one action at the same time")

    if click:
        pyautogui.mouseDown()
    elif key:
        pyautogui.keyDown(key)
    elif right:
        pyautogui.mouseDown(button=pyautogui.RIGHT)

    # print(f'waiting {wait_period}s')
    time.sleep(wait_period)

    if click:
        pyautogui.mouseUp()
    elif key:
        pyautogui.keyUp(key)
    elif right:
        pyautogui.mouseUp(button=pyautogui.RIGHT)

    return wait_period


def wait(start, stop):

    wait_period = map_between(random.random(), start, stop)
    time.sleep(wait_period)

    return wait_period


def on_off_state():
    """
    Uses caps lock as an on/off switch to determine state
    :return: 1 if caps lock is active else 0
    """
    import ctypes
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


def rand_inside(x1, y1, x2, y2):
    """
    Returns random coordinate inside bounding box
    """

    rx = map_between(random.random(), x1, x2)
    ry = map_between(random.random(), y1, y2)

    return rx, ry


def move_to_aoi(x1=0, y1=0, x2=5780, y2=1800):

    x, y = rand_inside(x1, y1, x2, y2)
    pyautogui.moveTo(x, y)

    return x, y


def mouse_inside(x1=0, y1=0, x2=5780, y2=1800):

    pos = pyautogui.position()
    x = pos.x
    y = pos.y

    return x1 < x < x2 and y1 < y < y2


def inventory_box_by_index(n):

    col = n % constants.SLOTS_HORIZONTAL
    row = n // constants.SLOTS_HORIZONTAL

    x1 = constants.INVENTORY_X1 + ((constants.ITEM_WIDTH + constants.INVENTORY_X_GAP) * col)
    y1 = constants.INVENTORY_Y1 + ((constants.ITEM_HEIGHT + constants.INVENTORY_Y_GAP) * row)

    x2 = x1 + constants.ITEM_WIDTH
    y2 = y1 + constants.ITEM_HEIGHT

    return x1, y1, x2, y2


def random_item_location(n):

    x1, y1, x2, y2 = inventory_box_by_index(n)
    return rand_inside(x1, y1, x2, y2)


def distribute_normally(x1=0, x2=1950, y1=0, y2=1050):
    centre = x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2

    x = numpy.random.normal(loc=centre[0], scale=(x2 - x1) / 8)
    y = numpy.random.normal(loc=centre[1], scale=(y2 - y1) / 8)

    # failsafe to make sure not out of bounds
    if x < x1:
        x = x1
    if x > x2:
        x = x2
    if y < y1:
        y = y1
    if y > y2:
        y = y2

    return int(x), int(y)


def move_to_index(n, normally=True):

    if normally:
        x1, y1, x2, y2 = inventory_box_by_index(n)
        nx, ny = distribute_normally(x1=x1, y1=y1, x2=x2, y2=y2)

        pyautogui.moveTo(nx, ny)

    else:
        rx, ry = random_item_location(n)
        pyautogui.moveTo(rx, ry)


class QuickPrayerButton:

    def __init__(self, sidebar=True):

        if sidebar:
            self.cx = 1245
            self.cy = 181
            self.cw = 15

            self.x1 = 1234
            self.y1 = 169
            self.x2 = 1258
            self.y2 = 193
        else:
            raise NotImplementedError

    def random_location(self, normal=True):
        """
        Returns a random location within the quick prayer box
        """
        if normal:
            return distribute_normally(x1=self.x1, x2=self.x2, y1=self.y1, y2=self.y2)
        else:
            raise NotImplementedError


def round_or_none(i, p=2):

    try:
        return round(i, p)
    except TypeError:
        return None


def click_aoi(aoi, speed=1):
    """
    clicks an area of interst
    :param aoi: dictionary of top left and bottom right
                within which to click
    :return: position clicked
    """

    x, y = distribute_normally(**aoi)
    pyautogui.moveTo(x, y)
    wait_and_click(
        constants.CLICK_SPEED_LOWER_BOUND * speed,
        constants.CLICK_SPEED_UPPER_BOUND * speed
    )

    return x, y


def right_click_aoi(aoi, speed=1):
    """
    right clicks an area of interst
    :param aoi: dictionary of top left and bottom right
                within which to click
    :return: position clicked
    """
    x, y = distribute_normally(**aoi)
    pyautogui.moveTo(x, y)
    wait_and_click(
        constants.CLICK_SPEED_LOWER_BOUND * speed,
        constants.CLICK_SPEED_UPPER_BOUND * speed,
        click=False, right=True
    )

    return x, y


def get_aoi():

    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', 'data', 'aoi.json'
        )
    )
    with open(path, 'r') as f:
        return json.load(f)


def int_or_list(val):

    try:
        return int(val)
    except ValueError:
        try:
            val = eval(val)
            if isinstance(val, list):
                return val
            else:
                raise ValueError
        except:
            raise ValueError


def clean_print(statement, max_=25):
    sys.stdout.write('\r')
    statement = statement + ' ' * (max_ - len(statement))
    sys.stdout.write(statement)
    sys.stdout.flush()
