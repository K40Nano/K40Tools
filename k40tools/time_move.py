#!/usr/bin/env python

from __future__ import print_function

import sys, time, math

from k40nano import NanoPlotter, LaserSpeed

speedcode = None
speedvalue = 0
speed = 1
sample = 5
for s in range(0,sample):
    t = -time.time()
    distance = 3937
    with NanoPlotter() as plotter:
        speedcode = LaserSpeed.get_code_from_speed(speed, board="M2")
        speedvalue = LaserSpeed.parse_speed_code(speedcode)
        plotter.enter_compact_mode(speedcode)
        for squares in range(0,1):
            plotter.move(0, distance)
    t += time.time()
    real_speed_mils = distance / t
    real_speed = real_speed_mils / 25.4
    print(speed, ",", speedvalue, ",", t, ",", real_speed_mils, ",", real_speed, real_speed / speed )
    with NanoPlotter() as plotter:
        plotter.home()
