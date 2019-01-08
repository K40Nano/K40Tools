#!/usr/bin/env python

from PngRaster import PngRaster


def is_on(sample, pass_index=0):
    """
    (Experimental)
    Whether that pixel is on based on the pass number.
    During pass zero the 8th bit is used. During pass one the 7th bit is used. etc.
    Should allow greyscale images to turn into depth images.
    Giving different bits for each pass.

    :param sample:
    :param pass_index: which pass is this.
    :return:
    """
    return ((sample >> (7 - pass_index)) & 1) == 0


def parse_depth_png(png_file, plotter, spread=4, x=0, y=0):
    if isinstance(png_file, str):
        with open(png_file, "rb") as png_file:
            parse_depth_png(png_file, plotter)
            return
    increment = spread
    step = spread
    on_count = 0
    off_count = 0
    speeds = [20, 40, 80, 160]
    for passes in range(0, len(speeds)):
        plotter.move_abs(x, y)
        plotter.enter_compact_mode(speeds[passes])
        for scanline in PngRaster.png_scanlines(png_file):
            if increment < 0:
                scanline = reversed(scanline)
            for i in scanline:
                if is_on(i):
                    if off_count != 0:
                        plotter.up()
                        plotter.move(off_count, 0)
                        off_count = 0
                    on_count += increment
                else:
                    if on_count != 0:
                        plotter.down()
                        plotter.move(on_count, 0)
                        on_count = 0
                    off_count += increment
            if off_count != 0:
                plotter.up()
                plotter.move(off_count, 0)
                off_count = 0
            if on_count != 0:
                plotter.down()
                plotter.move(on_count, 0)
                on_count = 0
            plotter.up()
            plotter.move(0, step)
            increment = -increment
        plotter.exit_compact_mode_break()


if __name__ == "__main__":
    import sys

    argv = sys.argv
    from k40nano.NanoPlotter import NanoPlotter

    filename = None
    spread = 4
    if len(argv) >= 2:
        filename = argv[1]
        if len(argv) >= 3:
            spread = argv[2]
        with NanoPlotter() as plotter:
            parse_depth_png(filename, plotter, spread)
