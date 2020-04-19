
import sys
import time
import random
import pyautogui
import utils

# Bank spot changes every time you move the camera so these are not really constants!
# topleft Point(x=944, y=527)
# bottom right Point(x=1043, y=649)
BX1 = int(sys.argv[1]) # 944
BY1 = int(sys.argv[2]) # 527
BX2 = int(sys.argv[3]) # 1043
BY2 = int(sys.argv[4]) # 649

# herb spot inside bank - also not necessarily constant!
# Point(x=309, y=247)
# Point(x=355, y=288)
HX1 = 309
HY1 = 247
HX2 = 355
HY2 = 288

loop = list(range(0, 27, 4)) + list(range(25, 0, -4)) + list(range(2, 27, 4)) + list(range(27, 0, -4))


while True:

    if utils.on_off_state():

        # clean the herbs
        for i in loop:

            utils.move_to_index(i)
            utils.wait_and_click(0.08, 0.15)
            utils.wait_and_click(0.02, 0.04, click=False)

        # open the bank
        bx, by = utils.distribute_normally(x1=BX1, x2=BX2, y1=BY1, y2=BY2)
        pyautogui.moveTo(bx, by)
        utils.wait_and_click(0.08, 0.15)

        # wait for it to be open
        time.sleep(utils.map_between(random.random(), 0.5, 1))

        # deposit herbs
        n = random.randint(0, 27)
        utils.move_to_index(n)
        utils.wait_and_click(0.08, 0.15)

        # wait for them to be deposited
        utils.wait_and_click(0.2, 0.5, click=False)

        # withdraw more herbs
        hx, hy = utils.distribute_normally(x1=HX1, x2=HX2, y1=HY1, y2=HY2)
        pyautogui.moveTo(hx, hy)
        utils.wait_and_click(0.08, 0.15)

        # close bank menu
        pyautogui.keyDown('esc')
        utils.wait_and_click(0.08, 0.15, click=False, key='esc')

        # wait for bank menu to be closed
        utils.wait_and_click(0.2, 0.5, click=False)

    else:
        time.sleep(1)
