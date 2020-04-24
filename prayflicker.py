
import sys
import time
import pyautogui
import random
import logging

import utils
import constants

SLEEP_PERIOD = 0.1

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


class PrayFlicker:

    def __init__(self, interval=constants.DEFAULT_NPC_ATTACK_SPEED):
        self.script_started_at = None
        self.time_since_script_started = None
        self.flick = False
        self.flick_started_at = None

        self.prayer_on_at = None
        self.on_interval = 0
        self.off_interval = 0

        self.time_since_start = None
        self.ticks_since_start = None
        self.cycles_since_start = None
        self.cycles = 0
        self.completed_cycles_time = None

        self.interval = interval

        self.button = utils.QuickPrayerButton()

        # current mouse position
        self.cx = None
        self.cy = None

        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Sets up a logger instance in debug mode
        :return: :class:`logging.Logger`
        """

        logger = logging.getLogger('pf')
        logger.setLevel(logging.INFO)

        fm = logging.Formatter('%(asctime)s %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(fm)

        logger.addHandler(sh)

        return logger

    def run(self):

        self.logger.info('Running')

        while True:

            # collect info about current state from mouse and keyboard
            self._update()
            self.logger.debug(' '.join(
                [str(v) for v in [
                    utils.round_or_none(self.flick_started_at, 2),
                    utils.round_or_none(self.time_since_start, 2),
                    utils.round_or_none(self.ticks_since_start, 2),
                    self.cycles_since_start,
                    utils.round_or_none(self.completed_cycles_time, 2),
                    # self._should_turn_prayer_on(),
                    # self._should_turn_prayer_off()
                ]]
            ))

            # self.flick_started_at = time.time()
            # self.time_since_start = 0
            # self.ticks_since_start = 0
            # self.cycles_since_start = 0
            # self.completed_cycles_time = 0

            if self.flick:

                self.logger.debug('Flicking on')

                # DO PRAYER FLICKING
                if not self.prayer_on:

                    self.logger.debug('prayer_on = None')

                    # should we turn prayer on yet?
                    if self._should_turn_prayer_on():

                        self.logger.info('turning prayer on')

                        # move the mouse if necessary
                        # NOTE: caps lock should be turned off to temporarily disable
                        if not self._within_bounds:
                            x, y = self._move_within_bounds()
                            self.logger.debug(f'moved mouse to {x}, {y}')

                        # click the prayer on
                        self.prayer_on_at = time.time()
                        self.logger.debug(f'prayer_on_at {self.prayer_on_at}')
                        utils.wait_and_click(0.05, 0.15)

                        self._recalculate_intervals()
                        self.logger.debug(f'on_interval = {self.on_interval}, off_interval = {self.off_interval}')

                    else:
                        self.logger.debug('prayer off, waiting to turn on')
                        time.sleep(SLEEP_PERIOD)
                else:

                    if self._should_turn_prayer_off():

                        self.logger.info('turning prayer off')

                        # move the mouse if necessary
                        # NOTE: caps lock should be turned off to temporarily disable
                        if not self._within_bounds:
                            x, y = self._move_within_bounds()
                            self.logger.debug(f'moved mouse to {x}, {y}')

                        self.prayer_on_at = None
                        utils.wait_and_click(0.05, 0.15)

                        # increment cycles so we can check for the next round
                        self.cycles += 1

                    else:
                        self.logger.debug('prayer on, waiting to turn off')
                        time.sleep(SLEEP_PERIOD)

            else:
                self.logger.debug('waiting for request')
                time.sleep(SLEEP_PERIOD)

    def _update(self):

        # collect info about keyboard state
        if utils.on_off_state():
            self.flick = True

            # start the time from now if not already set
            if not self.flick_started_at:
                self.flick_started_at = time.time()
                self.time_since_start = 0
                self.ticks_since_start = 0
                self.cycles_since_start = 0
                self.completed_cycles_time = 0
            else:
                self.time_since_start = time.time() - self.flick_started_at
                self.ticks_since_start = self.time_since_start / constants.TICK
                self.cycles_since_start = int(self.ticks_since_start / self.interval)
                self.completed_cycles_time = self.cycles_since_start * constants.TICK * self.interval

        else:
            self.flick = False

            # clear the timers ready for next iteration
            self.flick_started_at = None
            self.time_since_start = None
            self.ticks_since_start = None
            self.cycles_since_start = None
            self.completed_cycles_time = None

        # locate current mouse position
        mxy = pyautogui.position()
        self.cx = mxy.x
        self.cy = mxy.y

    @property
    def _within_bounds(self):

        # determine if within quick prayer bounding box
        return self.button.x1 < self.cx < self.button.x2 and self.button.y1 < self.cy < self.button.y2

    @property
    def prayer_on(self):
        return bool(self.prayer_on_at)

    def _recalculate_intervals(self):

        # calculate a random start time for the next prayer flick
        rnd = utils.map_between(random.random(), -constants.HALF_TICK, constants.HALF_TICK)
        self.on_interval = constants.TICK * self.interval + rnd

        # calculate how long we'll keep the prayer on for
        rnd = utils.map_between(random.random(), constants.TICK, constants.TICK + constants.HALF_TICK)
        self.off_interval = rnd

    def _move_within_bounds(self):
        """
        Moves mouse to random (normally distributed) location
        within button bounding box
        """

        x, y = self.button.random_location()
        pyautogui.moveTo(x, y)

        return x, y

    def _should_turn_prayer_on(self):

        # |---|---|---|--+|-  = overall timeline
        # |           |       = completed cycles time
        #             |  |    = on interval
        #                |  | = off interval

        self.logger.info('prayer on: ' + ' '.join(
            [str(v) for v in [
                utils.round_or_none(self.time_since_start),
                utils.round_or_none(self.cycles),
                utils.round_or_none(self.on_interval),
            ]]
        ))

        if self.time_since_start == 0:
            return True

        return self.time_since_start > (self.cycles * self.interval * constants.TICK) + self.on_interval

    def _should_turn_prayer_off(self):
        # |---|---|---|--+|-  = overall timeline
        # |           |       = completed cycles time
        #             |  |    = on interval
        #                |  | = off interval

        self.logger.info('prayer off: ' + ' '.join(
            [str(v) for v in [
                utils.round_or_none(self.time_since_start),
                utils.round_or_none(self.cycles),
                utils.round_or_none(self.off_interval)
            ]]
        ))

        if self.time_since_start == 0:
            return False

        return self.time_since_start > (self.cycles * self.interval * constants.TICK) + self.on_interval + self.off_interval



if __name__ == '__main__':

    try:
        i = sys.argv[1]
    except IndexError:
        i = constants.DEFAULT_NPC_ATTACK_SPEED

    pf = PrayFlicker(interval=i)

    pf.run()

