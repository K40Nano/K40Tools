#!/usr/bin/env python

from __future__ import print_function

import sys

from k40nano import NanoPlotter


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
dx = 0
dy = 0
speed = 30
if len(argv) == 2:
    dx = unit_convert(argv[1])
    dy = dx
elif len(argv) == 3:
    dx = unit_convert(argv[1])
    dy = unit_convert(argv[2])
elif len(argv) == 4:
    dx = unit_convert(argv[1])
    dy = unit_convert(argv[2])
    speed = float(argv[3])
if dx != 0 or dy != 0:
    with NanoPlotter() as plotter:
        plotter.enter_compact_mode(speed)
        plotter.move(dx, dy)
