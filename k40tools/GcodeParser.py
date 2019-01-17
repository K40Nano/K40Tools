def parse(f):
    comment = None
    code = ""
    value = ""
    command_map = {}
    ord_a = ord('a')
    ord_A = ord('A')
    ord_z = ord('z')
    ord_Z = ord('Z')
    while True:
        byte = f.read(1)
        if byte is None:
            break
        if len(byte) == 0:
            break
        is_end = byte == b'\n' or byte == b'\r'
        if comment is not None:
            if byte == b')' or is_end:
                command_map['comment'] = comment
                comment = None
                if not is_end:
                    continue
            else:
                try:
                    comment += byte.decode('utf8')
                except UnicodeDecodeError:
                    pass  # skip utf8 fail
                continue
        if byte == b'(':
            comment = ""
            continue
        elif byte == b';':
            comment = ""
            continue
        elif byte == b'\t':
            continue
        elif byte == b' ':
            continue
        elif byte == b'/' and len(code) == 0:
            continue
        b = ord(byte)
        if ord('0') <= b <= ord('9') \
                or byte == b'+' \
                or byte == b'-' \
                or byte == b'.':
            value += byte.decode('utf8')
            continue

        if ord_A <= b <= ord_Z:
            b = b - ord_A + ord_a
            byte = chr(b)
        is_letter = ord_a <= b <= ord_z
        if (is_letter or is_end) and len(code) != 0:
            command_map[code] = float(value)
            code = ""
            value = ""
        if is_letter:
            code += str(byte)
            continue
        elif is_end:
            if len(command_map) == 0:
                continue
            yield command_map
            command_map = {}
            code = ""
            value = ""
            continue


def parse_gcode(f, plotter, properties=None):
    if isinstance(f, str):
        with open(f, "rb") as f:
            parse_gcode(f, plotter)
            return
    flip_x = 1  # Assumes the GCode is flip_x, -1 is flip, 1 is normal
    flip_y = -1  # Assumes the Gcode is flip_y,  -1 is flip, 1 is normal
    absolute_mode = True  # G21 DEFAULT
    scale = 25.4  # Initially assume mm mode G20. 25.4 mils in an mm. G20 DEFAULT
    feed_scale = (1.0 / 25.4) * (1.0 / 60.0)  # inches to mm, seconds to minutes. G94 DEFAULT
    is_down = False
    feed_rate = 1000 * feed_scale
    for gc in parse(f):
        if 'comment' in gc:
            comment = gc['comment']
            pass
        if 'g' in gc:
            if gc['g'] == 0.0:
                plotter.up()
                plotter.exit_compact_mode_reset()
                if 'x' in gc:
                    x = gc['x'] * scale * flip_x
                else:
                    x = 0

                if 'y' in gc:
                    y = gc['y'] * scale * flip_y
                else:
                    y = 0
                if absolute_mode:
                    plotter.move_abs(int(round(x)), int(round(y)))
                else:
                    plotter.move(int(round(x)), int(round(y)))
            elif gc['g'] == 1.0:
                if not is_down:
                    plotter.down()
                plotter.enter_compact_mode(feed_rate)
                if 'x' in gc:
                    x = gc['x'] * scale * flip_x
                else:
                    x = 0

                if 'y' in gc:
                    y = gc['y'] * scale * flip_y
                else:
                    y = 0
                if absolute_mode:
                    plotter.move_abs(int(round(x)), int(round(y)))
                else:
                    plotter.move(int(round(x)), int(round(y)))
            elif gc['g'] == 28.0:
                plotter.home()
            elif gc['g'] == 21.0 or gc['g'] == 71.0:
                scale = 25.4  # g20 is mm mode. 25.4 mils in a mm
            elif gc['g'] == 20.0 or gc['g'] == 70.0:
                scale = 1000.0  # g20 is inch mode. 1000 mils in an inch
            elif gc['g'] == 90.0:
                absolute_mode = True
            elif gc['g'] == 91.0:
                absolute_mode = False
            elif gc['g'] == 94.0:
                # Feed Rate in Inches / Minute
                feed_scale = (1.0 / 25.4) * (1.0 / 60.0)  # inches to mm, seconds to minutes.
        if 'm' in gc:
            v = gc['m']
            if v == 30:
                return
            if v == 3 or v == 4:
                plotter.down()
                is_down = True
            elif v == 5:
                plotter.up()
                is_down = False
        if 'f' in gc:
            v = gc['f']
            feed_rate = feed_scale * v


if __name__ == "__main__":
    import sys

    argv = sys.argv
    from k40nano.NanoPlotter import NanoPlotter

    if len(argv) >= 2:
        filename = argv[1]
        with NanoPlotter() as plotter:
            plotter.enter_concat_mode()
            parse_gcode(filename, plotter)
