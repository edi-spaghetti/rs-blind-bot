
import argparse

from . import blackjacker

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, default='hotkey')

args = parser.parse_args()

bj = blackjacker.BlackJacker(mode=args.mode)
bj.run()
