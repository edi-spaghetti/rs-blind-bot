
import keyboard
import pyautogui
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

        self.butler_positions = {
            'left': self.bleft,
            'up': self.bup,
            'right': self.bright
        }

        self.clicked_butler = False
        self.current_butler_position = None
        self.butler_actions = 0

        print('initialised')

    def run(self):

        print('running')

        while True:

            # don't do anything if we're not on the game screen
            # this usually happens because i forget to stop the script
            # while i'm checking something
            if pyautogui.position().x > 2880:

                if keyboard.is_pressed('0'):
                    # do something
                    self.pay_butler()
                elif keyboard.is_pressed('1'):
                    self.click_butler('left')
                elif keyboard.is_pressed('5'):
                    self.click_butler('up')
                elif keyboard.is_pressed('3'):
                    self.click_butler('right')
                elif keyboard.is_pressed('2'):
                    self.make_larder()
                elif keyboard.is_pressed(self.exit):
                    exit(1)
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)

    def pay_butler(self):
        """
        Pays the butler and resets
        Can be launched separately in case script starts
        halfway through some bank trips
        :return:
        """

        # listen to him moaning
        utils.wait_and_click(0.1, 0.2, click=False, key='space')

        # wait until he's finished
        utils.wait(0.9, 1.1)

        # pay the man/demon
        utils.wait_and_click(0.1, 0.2, click=False, key='1')

        # wait for his grubby hands to snatch up that dough
        utils.wait(0.9, 1.1)

        # roll your eyes at his eternal gratitude, and get him to do his job again
        # fucking demonic ingrate
        utils.wait_and_click(0.1, 0.2, click=False, key='space')

        # back to work, swine!
        self.make_larder()

        self.butler_actions = 0

    def click_butler(self, position):
        """
        Clicks butler at position within aoi
        First click will click once
        Second click will press 1 in dialogue
        :param position: position butler is bound by
        :return:
        """

        aoi = self.butler_positions[position]

        # if we haven't clicked him already, click him now
        if not self.clicked_butler:
            utils.click_aoi(aoi)

        if not self.clicked_butler:
            self.clicked_butler = True
            self.current_butler_position = position
        else:

            # send butler off to bank
            utils.wait_and_click(0.08, 0.15, click=False, key='1')

            self.butler_actions += 1
            print(f'dispatching butler on trip {self.butler_actions}')
            self.current_butler_position = None

            # make a new larder right away
            self.make_larder()

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
        time.sleep(0.9)
        # utils.wait(1.2, 1.5)

        # press '1' to remove
        utils.wait_and_click(0.08, 0.15, click=False, key='1')

        # wait for larder to be removed
        time.sleep(0.9)
        # utils.wait(1.2, 1.5)

        # right click the larder hot spot
        x, y = utils.right_click_aoi(self.larder)
        bbox = self.calculate_build_menu_offset(x, y)

        # wait for right click menu to open
        utils.wait(0.3, 0.5)

        # click build
        utils.click_aoi(bbox)

        # wait for build creation menu
        time.sleep(0.8)
        # utils.wait(0.9, 1.2)

        # press '2' to build an oak larder
        utils.wait_and_click(0.08, 0.15, click=False, key='2')

        # wait for larder to be built
        time.sleep(0.8)

        if self.current_butler_position:
            self.click_butler(self.current_butler_position)

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
