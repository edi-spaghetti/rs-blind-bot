
import sys
import argparse

from .swapchopndrop import Lumberjack

lum = Lumberjack(sys.argv[1])
lum.run()
