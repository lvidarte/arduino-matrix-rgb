"""
Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

"""

from serial import Serial
from matrix import Matrix
from arduino2048 import Arduino2048
import time

serial = Serial('/dev/ttyACM0', 9600)
matrix = Matrix(serial)
game = Arduino2048(matrix)
time.sleep(2)
game.play()
