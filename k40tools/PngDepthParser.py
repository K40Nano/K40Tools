#!/usr/bin/env python

from PngRaster import PngRaster


def is_on(sample, pass_index):
    """
    Whether that pixel is white enough to zap this pass.
    
    :param sample:
    :param pass_index: which pass is this.
    :return:
    """
    return sample < pass_index


def parse_depth_png(png_file, plotter, spread=4, x=0, y=0):
    increment = spread
    on_count = 0
    off_count = 0
    print("Running Passes")
    passes = 5
    steps = 255 / (passes + 1)
    for threshhold in range(255-steps, steps, -steps):
        print("Burning samples brightness less than %d" % threshhold)
        plotter.move_abs(x-1, y-1) # Little hamfisted, I didn't make an api correct way to set the directions.
        plotter.move_abs(x, y)
        plotter.enter_compact_mode(210,spread)
        scanline_count = 0
        with open(png_file,"rb") as png:
            print("File Opened %s" % png_file)
            for scanline in PngRaster.png_scanlines(png):
                if increment < 0:
                    scanline = reversed(scanline)
                for i in scanline:
                    if is_on(i,threshhold):
                        if off_count != 0:
                            plotter.up()
                            plotter.move(off_count, 0)
                            plotter.down()
                            off_count = 0
                        on_count += increment
                    else:
                        if on_count != 0:
                            plotter.down()
                            plotter.move(on_count,0)
                            plotter.up()
                            on_count = 0
                        off_count += increment
                if off_count != 0:
                    plotter.up()
                    plotter.move(off_count, 0)
                    off_count = 0
                if on_count != 0:
                    plotter.down()
                    plotter.move(on_count,0)
                    on_count = 0
                plotter.up()
                if increment > 0:
                    plotter.move(1,0)
                    plotter.move(-1,0)
                else:
                    plotter.move(-1,0)
                    plotter.move(1,0)
                #plotter.move(0, step)
                increment = -increment
        plotter.exit_compact_mode_finish()
            

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
