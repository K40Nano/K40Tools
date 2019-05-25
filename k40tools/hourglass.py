#!/usr/bin/env python

from __future__ import print_function

import sys

from k40nano import NanoPlotter, LaserSpeed

argv = sys.argv

if len(argv) == 1:
    print("hourglass.py <d_ratio>")
    print("Default   is 0.261199033289")
    print("sqrt(2)-1 is 0.41421356237")
    exit(0)

if len(argv) >= 2:
    d_ratio = float(argv[1])
else:
    d_ratio = None

speed = 40

with NanoPlotter() as plotter:
    speedcode = LaserSpeed.get_code_from_speed(speed, d_ratio=d_ratio)
    plotter.enter_compact_mode(speedcode)
    plotter.down()
    plotter.move(500, 0)
    plotter.move(-500,500)
    plotter.move(500,0)
    plotter.move(-500,-500)

