
import pyautogui
import random
import time
import constants
import numpy

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


def wait_and_click(start, stop, click=True, key=None):
    """
    Waits and optional clicks in a timely manner
    :param start:
    :param stop:
    :param click:
    :return:
    """

    wait_period = map_between(random.random(), start, stop)

    if click and key:
        raise NotImplementedError("Don't click the mouse and a key at the same time")

    if click:
        pyautogui.mouseDown()
    elif key:
        pyautogui.keyDown(key)

    print(f'waiting {wait_period}s')
    time.sleep(wait_period)

    if click:
        pyautogui.mouseUp()
    elif key:
        pyautogui.keyUp(key)


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
