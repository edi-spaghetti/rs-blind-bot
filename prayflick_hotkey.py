
import sys
import time
import pyautogui
import utils

CX = 1245
CY = 181
CW = 15

X1 = 1234
Y1 = 169
X2 = 1258
Y2 = 193

TICK = 0.6
MICROTICK = 0.01

QUICK_PRAYER_BOUNDING_BOX = X1, Y1, X2, Y2

# assume we start with prayer off
prayer_on = False
prayer_on_at = prayer_off_at = None

print('loaded')

while True:

    #    # determine state     #    #

    # locate current mouse position
    mxy = pyautogui.position()
    cx = mxy.x
    cy = mxy.y

    # determine if within quick prayer bounding box
    within_bounds = X1 <= cx <= X2 and Y1 <= cy <= Y2

    state_on = utils.on_off_state()

    #    # perform action     #    #

    if state_on and not prayer_on:

        prayer_on_at = time.time()
        print(f'turning on prayer at {prayer_on_at}')

        # move mouse to pray flick area if necessary
        if not within_bounds:

            print(f'currently at {cx}, {cy}: moving to area first')

            x, y = utils.rand_inside(*QUICK_PRAYER_BOUNDING_BOX)
            pyautogui.moveTo(x, y)

        # adjusted based on testing here
        # http://instantclick.io/click-test
        utils.wait_and_click(0.08, 0.15)
        prayer_on = True

    elif prayer_on and not state_on:

        prayer_off_at = time.time()
        print(f'turning off prayer {prayer_off_at} ({prayer_off_at - prayer_on_at})')

        # move mouse to pray flick area if necessary
        if not within_bounds:

            print(f'currently at {cx}, {cy}: moving to area first')

            x, y = utils.rand_inside(*QUICK_PRAYER_BOUNDING_BOX)
            pyautogui.moveTo(x, y)

        # adjusted based on testing here
        # http://instantclick.io/click-test
        utils.wait_and_click(0.08, 0.15)
        prayer_on = False

    time.sleep(MICROTICK)
