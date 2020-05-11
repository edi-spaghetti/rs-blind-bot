
import time
import os
import keyboard
import pyautogui
import json


aoi_count = 0
aoi = {}
tl_done = False
br_done = False
tl = br = None
print('ready')

while True:

    if keyboard.is_pressed('y') and not tl_done:
        tl = pyautogui.position()
        tl_done = True
        print(f'top left at {tl}')

    if keyboard.is_pressed('u') and not br_done:
        br = pyautogui.position()
        br_done = True
        print(f'bottom right at {br}')

    if tl_done and br_done:

        # add another
        if keyboard.is_pressed('i'):
            aoi[str(aoi_count)] = {"x1": tl.x, "y1": tl.y, "x2": br.x, "y2": br.y}
            tl_done = br_done = False
            print('next')
            aoi_count += 1

        # finish here
        if keyboard.is_pressed('o'):
            aoi[str(aoi_count)] = {"x1": tl.x, "y1": tl.y, "x2": br.x, "y2": br.y}
            print('done')
            break

    time.sleep(0.05)

with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'aoi.json'), 'w') as f:
    json.dump(aoi, f)
