
import keyboard
import time

from ..utils import utils


class OakLarder:

    # area of interest indexes
    LARDER_INDEX = '0'
    BUTLER_LEFT_INDEX = '1'
    BUTLER_UP_INDEX = '2'
    BUTLER_RIGHT_INDEX = '3'

    # remove oak larder right click menu offsets
    RX1 = -75
    RY1 = 100
    RX2 = 75
    RY2 = 115

    # build oak larder right click menu offsets
    BX1 = -100
    BY1 = 75
    BX2 = 100
    BY2 = 90

    def __init__(self):

        self.exit = '-'
        self.aoi = utils.get_aoi()

        # area of interest bounding boxes
        self.larder = self.aoi[self.LARDER_INDEX]
        self.bright = self.aoi[self.BUTLER_RIGHT_INDEX]
        self.bup = self.aoi[self.BUTLER_UP_INDEX]
        self.bleft = self.aoi[self.BUTLER_LEFT_INDEX]

        self.clicked_butler = False

        print('initialised')

    def run(self):

        print('running')

        while True:

            if keyboard.is_pressed('0'):
                # do something
                self.do_action()
            elif keyboard.is_pressed('1'):
                # butler left
                self.click_butler(self.bleft)
            elif keyboard.is_pressed('5'):
                self.click_butler(self.bup)
            elif keyboard.is_pressed('3'):
                self.click_butler(self.bright)
            elif keyboard.is_pressed('2'):
                self.make_larder()
            elif keyboard.is_pressed(self.exit):
                exit(1)
            else:
                time.sleep(0.01)

    def do_action(self):
        pass

    def click_butler(self, aoi):
        """
        Clicks butler at position within aoi
        First click will click once
        Second click will press 1 in dialogue
        :param aoi: position butler is bound by
        :return:
        """

        if self.clicked_butler:
            utils.wait_and_click(0.08, 0.15, click=False, key='space')

        utils.click_aoi(aoi)

        if not self.clicked_butler:
            self.clicked_butler = True
        else:

            # wait for dialogue to be open
            utils.wait(0.9, 1.2)

            # send butler off to bank
            utils.wait_and_click(0.08, 0.15, click=False, key='1')

    def make_larder(self):

        self.clicked_butler = False
        print('making oak larder')

        # right click the larder
        x, y = utils.right_click_aoi(self.larder)
        bbox = self.calculate_remove_menu_offset(x, y)

        # wait for right click menu to open
        utils.wait(0.3, 0.5)

        # click remove
        utils.click_aoi(bbox)

        # wait for dialogue to open
        time.sleep(1.1)
        # utils.wait(1.2, 1.5)

        # press '1' to remove
        utils.wait_and_click(0.08, 0.15, click=False, key='1')

        # wait for larder to be removed
        utils.wait(1.2, 1.5)

        # right click the larder hot spot
        x, y = utils.right_click_aoi(self.larder)
        bbox = self.calculate_build_menu_offset(x, y)

        # wait for right click menu to open
        utils.wait(0.3, 0.5)

        # click build
        utils.click_aoi(bbox)

        # wait for build creation menu
        utils.wait(0.9, 1.2)

        # press '2' to build an oak larder
        utils.wait_and_click(0.08, 0.15, click=False, key='2')

    def calculate_remove_menu_offset(self, x, y):
        """
        Returns bounding box of remove larder menu option
        relative to point it was right clicked from
        :param x: Mouse position at x
        :param y: Mouse position at y
        :return: dictionary top left and bottom right for
        """
        return dict(
            x1=x + self.RX1,
            y1=y + self.RY1,
            x2=x + self.RX2,
            y2=y + self.RY2,
        )

    def calculate_build_menu_offset(self, x, y):
        """
        Returns bounding box of build larder menu option
        relative to point it was right clicked from
        :param x: Mouse position at x
        :param y: Mouse position at y
        :return: dictionary top left and bottom right
        """
        return dict(
            x1=x + self.BX1,
            y1=y + self.BY1,
            x2=x + self.BX2,
            y2=y + self.BY2,
        )
