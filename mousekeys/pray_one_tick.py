
import time
import keyboard

from ..utils import utils


class PrayOneTick:

    # ------ ------ ------
    #  |   |  |   |  |
    #  on off on off on
    LONG_PAUSE = 0.4
    SHORT_PAUSE = 0.2
    CYCLE = LONG_PAUSE + SHORT_PAUSE

    ADJUST = 0.01

    def __init__(self):
        self.qp = utils.get_aoi()['0']

        self.on_at = None
        self.pray_on = False
        self.off_at = None
        self.state = None

        print('loaded')

    def run(self):

        started_at = time.time()
        flicks = 0

        while True:

            self.state = utils.on_off_state()
            pause = (time.time() - (started_at + (flicks * self.CYCLE)))

            if keyboard.is_pressed('+'):
                started_at += self.ADJUST
                print(f'time moved forward {self.ADJUST}')
                time.sleep(0.05)
            elif keyboard.is_pressed('-'):
                started_at -= self.ADJUST
                print(f'time moved back {self.ADJUST}')
                time.sleep(0.05)

            if self.state:
                # make sure mouse is inside quick prayer bbox
                if not utils.mouse_inside(**self.qp):
                    utils.move_to_aoi(**self.qp)
            else:
                # switch prayer off if it's not already
                if self.pray_on:
                    if not utils.mouse_inside(**self.qp):
                        utils.move_to_aoi(**self.qp)
                    utils.wait_and_click(start=0.04, stop=0.09)
                    self.pray_on = False

            if self.pray_on:
                if pause > self.LONG_PAUSE:
                    clicked_at = time.time()

                    # if we're on then actually do it
                    if self.state:
                        utils.wait_and_click(start=0.04, stop=0.09)
                        self.pray_on = False
                        # print(f'flick {flicks} off at {clicked_at} - paused ({round(pause, 4)})')
            else:
                if pause > 0:
                    clicked_at = time.time()
                    flicks += 1

                    # if we're on the actually do it
                    if self.state:
                        utils.wait_and_click(start=0.04, stop=0.09)
                        self.pray_on = True

                        # print(f'flick {flicks} on at {clicked_at} - paused ({round(pause, 4)})')
