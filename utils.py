
import pyautogui
import random
import time


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


def wait_and_click(start, stop, click=True):
    """
    Waits and optional clicks in a timely manner
    :param start:
    :param stop:
    :param click:
    :return:
    """

    wait_period = map_between(random.random(), start, stop)

    if click:
        pyautogui.mouseDown()

    print(f'waiting {wait_period}s')
    time.sleep(wait_period)

    if click:
        pyautogui.mouseUp()


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
