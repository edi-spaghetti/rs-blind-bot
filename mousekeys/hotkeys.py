
import keyboard

from ..utils import utils


class HotKeys:

    def __init__(self):

        self.aoi = utils.get_aoi()
        print('loaded')

    def run(self):

        max_aoi_index = len(self.aoi)

        while True:

            for i in range(max_aoi_index):
                index = str(i)
                if keyboard.is_pressed(str(i)):
                    utils.clean_print(f'clicked aoi {i}')
                    utils.click_aoi(self.aoi[index])
