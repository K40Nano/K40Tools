#!/usr/bin/env python

from k40nano import NanoConnection, MockUsb


def skip(read, byte, count):
    """Skips forward in the file until we find <count> instances of <byte>"""
    pos = read.tell()
    while count > 0:
        char = read.read(1)
        if char in byte:
            count -= 1
        if char is None or len(char) == 0:
            read.seek(pos, 0)
            # If we didn't skip the right stuff, reset the position.
            break


def send_egv(f, connection=None):
    if connection is None:
        with NanoConnection() as connect:
            send_egv(f, connect)
            connect.flush()
            connect.wait()
        return
    if isinstance(f, str):
        with open(f, "r") as f:
            send_egv(f, connection)
            return
    skip(f, (b'\n', '\n'), 3)
    skip(f, (b'%', '%'), 5)
    while True:
        line = f.readline()
        if line is None:
            break
        if len(line) == 0:
            break
        connection.write(line)


if __name__ == "__main__":
    import sys

    argv = sys.argv
    filename = None
    if len(argv) >= 2:
        filename = argv[1]
        send_egv(filename)
