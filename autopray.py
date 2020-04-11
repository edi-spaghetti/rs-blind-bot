"""
Quick and Dirty Auto-Pray Clicker
"""

import pyautogui
import random
from utils import map_between, wait_and_click
import time

# coords of rapid pray on runelite at full screen
X1 = 1444
Y1 = 642
X2 = 1474
Y2 = 674

while True:

    x = pyautogui.position().x
    y = pyautogui.position().y

    if X1 < x < X2 and Y1 < y < Y2:

        print('clicking rapid heal')
        # turn rapid heal on
        wait_and_click(0.05, 0.2)

        # wait a little bit
        wait_and_click(0.05, 0.2, click=False)

        # turn rapid heal off
        wait_and_click(0.05, 0.2)

        print('waiting for next cycle')
        # wait for next cycle
        wait_and_click(45, 59, click=False)
    else:
        print('out of bounds')
        time.sleep(1)

