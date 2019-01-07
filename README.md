# K40Tools
Tools for the K40 Laser Cutter using K40Nano API


# Code Examples

Parsers
---

There are two premade parser classes these take a filename or fileobject and a plotter. 

`parse_png` within the `PngParser` class parses a png file scanline by scanline and plots that information. It does this by reading the PNG directly, and making plotter calls while reading the file. There's very little memory footprint and even a tiny device can process a huge file without delay.

`parse_egv` within the `EgvParser` class reads the egv file and plots that data. The `NanoPlotter` would then turn these commands back into .egv data and send that to the laser. In the parser the .EGV files do not have any special priority. They are simply treated as containing vector data. This allows the `NanoPlotter` to optimize some things. If we wanted to just send the EGV data as is, we would use the a NanoConnection ourselves and feed the EGV data in, and then call `wait()` on the NanoConnection (with the assumption the EGV data has the F command in it already). 

Several other parsers could be added along these same lines. Load a file, interact with the API based on what the file says. But these should not be assumed to be a limit to the utility. If you wanted to, for example, rig up joystick to control the K40, you could do that with a few lines of code and the API, parsers are only a typical uses case example.

Keyburn
---

Controls the K40 Laser Cutter with your keyboard.

* Default movement is WASD keys. 
* Pressing `space` fires the laser.
* Hitting `e` toggles the laser.
* Number 1-9 set the speed in compact mode.
    * Do note because this is compact mode it doesn't send the packets until they are full, or you hit escape to finish. So it will seem weird.
* Hitting `escape` ends compact mode, if in compact mode. Or quits keyburn if not in compact mode.
* Hitting `home` homes the device.


CLI (Command Line Interface)
---
The `Nano` CLI. This is not intended to be exclusive or definitive, but go ahead and ask more to be built on it (raise an issue). It is built on the concept of a stack. Namely you have a list of commands you can list them with (-l), you can load files with a wildcard "-i \*.EGV" and it should load those files.
 
* -i [\<input-\*\>]\*, loads egv/png files
* -o [<egv/png/svg>|"print"|"mock"]?, sets output method
* -p [n], sets the number of passes
* -m ([dx] [dy])+, relative move command
* -M ([x] [y])+, absolute move command
* -c ([dx] [dy])+, relative cut command
* -C ([x] [y])+, absolute cut command
* -s [+/-]?<speed> [step]*, sets the speed
* -w [seconds], wait_time
* -e, executes stack
* -l, lists stack
* -r, resets to home position
* -u, unlock rail
* -U, lock rail
* -v, verbose mode (default)
* -q, quiet mode
* -h, display this message

Nano uses the PNG parser. Calling the input on a PNG file will perform the raster-engrave commands of the scanlines of the PNG file. As defined in that parser. 

The CLI will also accept units: in, mm, cm, ft. There cannot be a space between the number and the unit. `-m 2in 2in` or `-c 33mm 7mm` 

Usually this would be:
`python2 ./Nano.py <commands>`

Example #1:
If you wanted to run a series of 25 jobs, with 30 seconds between each.

Nano `-m 2in 2in -e -i my_job.egv -w 30 -p 25 -e`

* -m: Add a move to the stack
* -e: execute the stack (move command)
* -i my_job.egv: add my_job.egv to the stack
* -w: add a 30 second wait to the stack.
* -p 25: duplicate the stack (my_job.egv, wait) 25 times.
* (default -e) executes stack.

Example #2:
If you wanted to make 25 copies of a file in a 5x5 grid.

Nano `-r -m 2000 2000 -e -i *.EGV -m 750 0 -p 5 -m -3750 750 -p 5`

* -r: Adds a home position command to the stack.
* -m 2000 2000: moves +2 inches +2 inches
* -e: executes stack (home position, move command)
* -i adds each found file matching wildcard \*.EGV to the stack.
    * In my case this only matched test_engrave.EGV which was about 0.5 x 0.5 inches wide.
* -m 750 0: moves +0.75 inches right.
* -p 5: duplicate stack 5 times (files, move command)
* -m -3750 750: adds move -3.75 inches left, and 0.75 inches down to the stack.
* -p 5: duplicates stack 5 times. (files, move command, files, move command, files, move command, files, move command, files, move command, move to next row position)
* (default -e) executes stack.


HomeK40
---

Simple program sends "IPP" to the device, which homes the device.

```python
from k40nano import NanoConnection

with NanoConnection() as stream:
    stream.write("IPP")
```

