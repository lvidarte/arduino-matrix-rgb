#!/usr/bin/python -i

import sys
import serial
import atexit
import os
import readline
import rlcompleter

import matrix
import demo

try:
    conn = serial.Serial('/dev/ttyACM0', 9600)
except OSError:
    try:
        conn = serial.Serial('/dev/ttyACM1', 9600)
    except OSError:
        print "Can't connect to serial device"
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


matrix = matrix.Matrix(conn)
demo = demo.Demo(matrix)

