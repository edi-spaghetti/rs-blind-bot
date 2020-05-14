
import time

from ..utils import utils


class PrayOneTick:

    # ------ ------ ------
    #  |   |  |   |  |
    #  on off on off on
    LONG_PAUSE = 0.4
    SHORT_PAUSE = 0.2
    CYCLE = LONG_PAUSE + SHORT_PAUSE

    def __init__(self):
        self.qp = utils.get_aoi()['0']

        self.on_at = None
        self.pray_on = False
        self.off_at = None

        print('loaded')

    def run(self):

        clicked_at = None
        started_at = None
        flicks = 0

        while True:

            if utils.on_off_state():

                if not started_at:
                    started_at = time.time()
                    flicks = 0

                if not utils.mouse_inside(**self.qp):
                    utils.move_to_aoi(**self.qp)

                pause = (time.time() - (started_at + (flicks * self.CYCLE)))

                if self.pray_on:
                    if pause > self.LONG_PAUSE:
                        clicked_at = time.time()
                        utils.wait_and_click(0.08, 0.015)
                        self.pray_on = False
                        flicks += 1
                        print(f'flick {flicks} off at {clicked_at} - paused ({round(pause, 4)})')
                else:
                    if pause > 0:
                        clicked_at = time.time()
                        utils.wait_and_click(0.08, 0.015)
                        self.pray_on = True
                        print(f'flick {flicks} on at {clicked_at} - paused ({round(pause, 4)})')

            else:

                # make sure prayer is off
                if self.pray_on:
                    if not utils.mouse_inside(**self.qp):
                        utils.move_to_aoi(**self.qp)
                    utils.wait_and_click(0.08, 0.015)

                # reset other variables
                self.pray_on = False
                started_at = None
                flicks = 0

                # wait for something to happen
                time.sleep(0.01)
