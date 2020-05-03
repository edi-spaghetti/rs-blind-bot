
import sys
import time
import random
import pyautogui
import utils
import keyboard

# Bank spot changes every time you move the camera so these are not really constants!
# topleft Point(x=944, y=527)
# bottom right Point(x=1043, y=649)
BX1 = int(sys.argv[1]) # 944
BY1 = int(sys.argv[2]) # 527
BX2 = int(sys.argv[3]) # 1043
BY2 = int(sys.argv[4]) # 649

# sulphur spot inside bank - also not necessarily constant
SX1 = 817
SY1 = 375
SX2 = 846
SY2 = 404

# compot
CX1 = 820
CY1 = 430
CX2 = 852
CY2 = 461

loop = list(range(0, 27, 4)) + list(range(25, 0, -4)) + list(range(2, 27, 4)) + list(range(27, 0, -4))

# assumes we start with an inventory of grimy herbs
inventory = [False] * 28
# assume we start with bank closed
bank_open = False
bank_hex = 'FF971CB0'
EXIT_KEY = 'p'


while True:

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # make the fertiliser
    for i in loop:

        # if we have to pause here then something went wrong
        # probably best just to restart!
        if keyboard.is_pressed(EXIT_KEY):
            exit(1)

        utils.move_to_index(i)
        utils.wait_and_click(0.05, 0.08)
        utils.wait_and_click(0.01, 0.1, click=False)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # open the bank
    bx, by = utils.distribute_normally(x1=BX1, x2=BX2, y1=BY1, y2=BY2)
    pyautogui.moveTo(bx, by)
    utils.wait_and_click(0.08, 0.15)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # wait for it to be open
    time.sleep(utils.map_between(random.random(), 0.5, 1))

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # withdraw more sulphur
    hx, hy = utils.distribute_normally(x1=SX1, x2=SX2, y1=SY1, y2=SY2)
    pyautogui.moveTo(hx, hy)
    utils.wait_and_click(0.08, 0.15)

    # wait for them to be withdrawn
    utils.wait_and_click(0.4, 0.6, click=False)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # deposit fertiliser
    n = random.choice([1, 3, 4, 6, 9, 11, 12, 14, 17, 19, 20, 22, 25, 27])
    utils.move_to_index(n)
    utils.wait_and_click(0.08, 0.15)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # wait for them to be deposited
    utils.wait_and_click(0.4, 0.6, click=False)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # withdraw more compost
    hx, hy = utils.distribute_normally(x1=CX1, x2=CX2, y1=CY1, y2=CY2)
    pyautogui.moveTo(hx, hy)
    utils.wait_and_click(0.08, 0.15)

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # close bank menu
    pyautogui.keyDown('esc')
    utils.wait_and_click(0.08, 0.15, click=False, key='esc')

    if keyboard.is_pressed(EXIT_KEY):
        exit(1)

    # wait for bank menu to be closed
    utils.wait_and_click(0.35, 0.6, click=False)
