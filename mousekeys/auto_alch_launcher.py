
import argparse
from . import auto_alch

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--repeat', type=int, default=-1)
parser.add_argument('-t', '--tab', type=str, default='MAGIC')
args = parser.parse_args()

aa = auto_alch.HighAlch(repeat=args.repeat, current_tab=args.tab)
aa.run()
