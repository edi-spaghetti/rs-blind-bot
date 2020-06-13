
import argparse

from . import auto_cast


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--spell', type=str)

args = parser.parse_args()

ac = auto_cast.AutoCaster(spell_name=args.spell)
ac.run()
