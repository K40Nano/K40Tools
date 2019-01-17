#!/usr/bin/env python

from __future__ import print_function

import sys
import time
from math import sqrt

from k40nano import NanoPlotter, LaserSpeed


def unit_convert(value):
    if value.endswith("in"):
        return int(round(1000 * float(value[:-2])))
    elif value.endswith("mm"):
        return int(round(39.3701 * float(value[:-2])))
    elif value.endswith("cm"):
        return int(round(393.701 * float(value[:-2])))
    elif value.endswith("ft"):
        return int(round(12000 * float(value[:-2])))
    return int(value)


argv = sys.argv

if len(argv) == 1:
    print("SlowMove <X> <Y> <MM_Per_Second> <Board> <Gear>")
    exit(0)

if len(argv) >= 2:
    dx = unit_convert(argv[1])
else:
    dx = 0

if len(argv) >= 3:
    dy = unit_convert(argv[2])
else:
    dy = dx

if len(argv) >= 4:
    speed = float(argv[3])
else:
    speed = 30

if len(argv) >= 5:
    board = str(argv[4])
else:
    board = "M2"

if len(argv) >= 6:
    gear = int(argv[5])
else:
    gear = None

if dx != 0 or dy != 0:
    t = time.time()
    with NanoPlotter() as plotter:
        speedcode = LaserSpeed.get_code_from_speed(speed, board=board, gear=gear)
        plotter.enter_compact_mode(speedcode)
        plotter.move(dx, dy)
    t = time.time() - t
    d = sqrt(dx * dx + dy * dy)
    print("Moved dx=%f dy=%f distance=%f in %f seconds at an overall rate: %fin/s" % (dx, dy, d, t, d / (1000 * t)))
