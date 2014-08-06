#!/usr/bin/env python

import serial

LED_MODE = 0
COMMAND_MODE = 1


conn = serial.Serial('/dev/ttyACM0', 9600)

class Led:
    def __init__(self, x, y=0, r=0, g=0, b=0, mode=LED_MODE):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.m = mode

    def get_msg(self):
        s = ""
        for c in "xyrgbm":
            b = bin(getattr(self, c)).replace('0b', '').zfill(3)
            s = b + s

        n = int(s[-8:], 2)
        m = int(s[2:10], 2)
        msg = chr(n) + chr(m)
        return msg

    def draw(self):
        conn.write(self.get_msg())


if __name__ == '__main__':

    import sys

    if len(sys.argv) == 2:
        command = int(sys.argv[1])
        led = Led(command, mode=COMMAND_MODE)
        led.draw();

    elif len(sys.argv) == 6:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        red = int(sys.argv[3])
        green = int(sys.argv[4])
        blue = int(sys.argv[5])
        led = Led(x, y, red, green, blue)
        led.draw();

    else:
        print "Usage: %s x y red green blue" % sys.argv[0]
        print "       %s [COMMAND]" % sys.argv[0]

