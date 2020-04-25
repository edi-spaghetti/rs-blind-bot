"""
Crafts gold amulets
"""

import argparse
import pyautogui
import random

from utils import (
    on_off_state,
    distribute_normally,
    wait_and_click,
    move_to_index
)

AOI = {
    'bank': dict(x1=82, y1=601, x2=143, y2=710),
    'amulet': dict(x1=278, y1=463, x2=313, y2=498),
    'bars': dict(x1=390, y1=336, x2=422, y2=367),
    'furnace': dict(x1=1296, y1=327, x2=1354, y2=402)
}

ORDER = ['bars', 'furnace', 'amulet', 'bank']

def is_key(v):
    if v not in AOI.keys():
        raise KeyError
    return str(v)

parser = argparse.ArgumentParser()
parser.add_argument('-sp', '--start_point', type=str, default='bars')


while True:

    if on_off_state():

        # withdraw the gold bars
        gx, gy = distribute_normally(**AOI['bars'])
        pyautogui.moveTo(gx, gy)
        wait_and_click(0.08, 0.15)

        # wait for the bars to be withdrawn
        wait_and_click(0.2, 0.5, click=False)

        # click the furnace
        fx, fy = distribute_normally(**AOI['furnace'])
        pyautogui.moveTo(fx, fy)
        wait_and_click(0.08, 0.15)

        # wait to get to the furnace / crafting menu
        wait_and_click(5.96, 6.30, click=False)

        # click the amulet option
        ax, ay = distribute_normally(**AOI['amulet'])
        pyautogui.moveTo(ax, ay)
        wait_and_click(0.08, 0.15)

        # wait for the amulets to be done
        wait_and_click(48.2, 49.7, click=False)

        # click the bank
        bx, by = distribute_normally(**AOI['bank'])
        pyautogui.moveTo(bx, by)
        wait_and_click(0.08, 0.15)

        # wait to get back to the bank
        wait_and_click(5.96, 6.30, click=False)

        # deposit the amulets
        i = random.randint(1, 27)
        move_to_index(i)
        wait_and_click(0.08, 0.15)

        # wait for amulets to be deposited
        wait_and_click(0.2, 0.5, click=False)
