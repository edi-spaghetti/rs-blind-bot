
import sys
import time
import pyautogui

import utils
# from utils import on_off_state, wait_and_click

TICK = 0.6
SLEEP_PERIOD = 0.1

try:
    INTERVAL = int(sys.argv[1])
except IndexError:
    INTERVAL = 4  # default monster attack speed

CX = 1245
CY = 181
CW = 15

X1 = 1234
Y1 = 169
X2 = 1258
Y2 = 193


script_started_at = time.time()
flick = False
flick_started_at = None
prayer_on = False


while True:

    # get state

    time_since_script_started = time.time() - script_started_at
    current_tick = time_since_script_started // TICK

    # determine if we should be flicking or not
    if utils.on_off_state():
        flick = True

        # start the time from now if not already set
        if not flick_started_at:
            flick_started_at = time.time()

    else:
        flick = False

        # clear the timer ready for next iteration
        if flick_started_at:
            flick_started_at = None

    # locate current mouse position
    mxy = pyautogui.position()
    cx = mxy.x
    cy = mxy.y

    # determine if within quick prayer bounding box
    within_bounds = X1 < cx < X2 and Y1 < cy < Y2

    # determine time since started flicking
    time_since_started = time.time() - (flick_started_at or 0)
    ticks_since_started = time_since_started // TICK

    # do an action

    #
    if flick:

        # DO PRAYER FLICKING
        if within_bounds:
            if not ticks_since_started % INTERVAL:

                print('prayer on')
                utils.wait_and_click(0.05, 0.2)
                print('waiting')
                utils.wait_and_click(TICK/3, TICK/2, click=False)
                print('prayer off')
                utils.wait_and_click(0.05, 0.2)
            else:
                print('waiting for next interval')
                time.sleep(SLEEP_PERIOD)
        else:
            x, y = utils.rand_inside(X1, Y1, X2, Y2)
            pyautogui.moveTo(x, y)

    else:
        print('waiting for request')
        time.sleep(SLEEP_PERIOD)
