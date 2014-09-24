#!/usr/bin/python -i

import sys
import atexit
import os
import readline
import rlcompleter

from optparse import OptionParser

from serial import Serial
from matrix import Matrix
from demo import Demo


usage = "usage: %prog [options] port"
parser = OptionParser(usage=usage)
parser.add_option('-b', '--baudrate', type=int, default=9600,
                  help="baud rate")
options, args = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    sys.exit(1)

try:
    serial = Serial(args[0], options.baudrate)
except OSError:
    print "Can't connect to serial device on", args.port
    sys.exit(1)


historyPath = os.path.expanduser("~/.matrix-history")

#readline.parse_and_bind('tab: menu-complete')
readline.parse_and_bind('tab: complete')

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath

matrix = Matrix(serial)
demo = Demo(matrix)

print """
Welcome to matrix shell
Autocompletion and history are enabled

Objects:
    serial    (object)  serial = Serial()
    matrix    (object)  matrix = Matrix(serial)
    demo      (object)  demo = Demo(matrix)

Try the demo:
    >>> demo.start()
"""
