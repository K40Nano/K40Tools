#!/usr/bin/env python

import struct
import zlib
from math import ceil


def get_stride(sample_count, bit_depth, width):
    return int(ceil(bit_depth * sample_count * float(width) / 8.0))


def get_sample_count(color_type):
    if color_type == 0:
        return 1
    elif color_type == 2:
        return 3
    elif color_type == 3:
        return 1
    elif color_type == 4:
        return 2
    elif color_type == 6:
        return 4
    else:
        return 1


def as_samples(bit_depth, sample_count, scanline, palette=None):
    pixel_length_in_bits = bit_depth * sample_count
    bit_depth_mask = (1 << bit_depth) - 1
    mask_sample_bits = (1 << pixel_length_in_bits) - 1
    total_samples = int(((len(scanline) - 1) * 8) / pixel_length_in_bits)
    for i in range(0, total_samples):
        start_pos_in_bits = (i * pixel_length_in_bits) + 8
        end_pos_in_bits = start_pos_in_bits + pixel_length_in_bits - 1
        start_pos_in_bytes = int(start_pos_in_bits / 8)
        end_pos_in_bytes = int(end_pos_in_bits / 8)

        section = scanline[start_pos_in_bytes:end_pos_in_bytes + 1]
        section = (4 - len(section)) * b'\x00' + section
        value = struct.unpack(">I", section)[0]
        unused_bits_right_of_sample = (8 - (end_pos_in_bits + 1) % 8) % 8
        sample = (value >> unused_bits_right_of_sample) & mask_sample_bits
        if sample_count == 1:
            if palette is None:
                yield sample
            else:
                sample = sample * 3
                red = palette[sample]
                green = palette[sample + 1]
                blue = palette[sample + 2]
                if isinstance(red, str):
                    red = ord(red)
                if isinstance(green, str):
                    green = ord(green)
                if isinstance(blue, str):
                    blue = ord(blue)
                yield [red, green, blue]
        else:
            yield [
                (sample >> bit_move) & bit_depth_mask
                for bit_move in range((sample_count - 1) * bit_depth, -1, -bit_depth)
            ]


def png_scanlines(file):
    if file.read(8) != b'\x89PNG\r\n\x1a\n':
        return  # Not a png file.
    decompress = zlib.decompressobj()
    buf = b''
    bit_depth = 0
    stride = 1
    sample_count = 1
    color_type = -1
    palette = None
    while True:
        length_bytes = file.read(4)
        if len(length_bytes) == 0:
            break
        length = struct.unpack(">I", length_bytes)[0]
        byte = file.read(4)
        signature = byte.decode('utf8')
        if len(signature) == 0:
            break
        if signature == 'IHDR':
            data = file.read(length)
            width = struct.unpack(">I", data[0:4])[0]
            # height = struct.unpack(">I", data[4:8])[0]

            bit_depth = data[8]
            if isinstance(bit_depth, str):
                bit_depth = ord(bit_depth)
            color_type = data[9]
            if isinstance(color_type, str):
                color_type = ord(color_type)
            sample_count = get_sample_count(color_type)
            stride = get_stride(sample_count, bit_depth, width) + 1
            file.seek(4, 1)  # skip crc
            continue
        elif signature == 'PLTE':
            data = file.read(length)
            if color_type == 3:
                palette = bytearray(data)
            file.seek(4, 1)
            continue
        elif signature == 'IDAT':
            while length > 0:
                read_amount = min(stride, length)
                buf += decompress.decompress(file.read(read_amount))
                length -= read_amount
                while len(buf) >= stride:
                    yield [x for x in as_samples(bit_depth, sample_count, buf[:stride], palette)]
                    buf = buf[stride:]
            file.seek(4, 1)  # skip crc
            continue
        elif signature == 'IEND':
            buf += decompress.flush()
            while len(buf) >= stride:
                yield [x for x in as_samples(bit_depth, sample_count, buf[:stride], palette)]
                buf = buf[stride:]
            file.seek(4, 1)
            return
        data = file.read(length)
        crc = file.read(4)


def is_on(sample, threshold):
    """
    Whether that pixel is should be zapped this pass.
    If the sample is multipart, takes color value.
    
    :param sample:
    :param threshold value.
    :return:
    """
    sample_value = sample
    if isinstance(sample, (list, tuple)):
        sample_value = max(sample[0], sample[1], sample[2])
    return sample_value < threshold


def parse_png(png_file, plotter, spread=1, passes=1, speed=210, x=0, y=0):
    on_count = 0
    off_count = 0
    print("Running Passes")
    step_amount = int(ceil(256.0 / float(passes + 1)))
    for threshold in range(step_amount, 255, step_amount):
        print("Burning samples brightness less than %d" % threshold)
        plotter.move_abs(x - 1, y - 1)
        plotter.move_abs(x, y)
        plotter.enter_compact_mode(speed, spread)

        with open(png_file, "rb") as png:
            print("File Opened %s" % png_file)
            increment = spread
            for scanline in png_scanlines(png):
                if increment < 0:
                    scanline = reversed(scanline)
                for i in scanline:
                    if is_on(i, threshold):
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
                if not plotter.h_switch():
                    plotter.move(0, spread)
                increment = -increment
        plotter.exit_compact_mode_break()
        plotter.move_abs(x, y)


if __name__ == "__main__":
    import sys

    argv = sys.argv
    from k40nano.NanoPlotter import NanoPlotter

    filename = None
    spread = 1
    if len(argv) >= 2:
        filename = argv[1]
        if len(argv) >= 3:
            spread = argv[2]
        with NanoPlotter() as plotter:
            parse_png(filename, plotter, spread)
