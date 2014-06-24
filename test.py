#!/usr/bin/env python

import time
import serial


ser = serial.Serial('/dev/ttyACM0', 9600)

class Led:
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    def get_msg(self):
        return "".join([chr(getattr(self, c)) for c in "xyrgb"])

class Sprite:
    def __init__(self, *leds):
        self.leds = []
        for led in leds:
            self.add(leds)

    def add(self, led):
        self.leds.append(led)

    def draw(self):
        for led in self.leds:
            ser.write(led.get_msg())
        self.flush()

    def flush(self):
        ser.write('FLUSH')


space_invader_0 = (
    (0, 0, 1, 0, 0, 1, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1),
    (1, 1, 0, 1, 1, 0, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 1, 0, 0, 1, 0, 0),
    (0, 1, 0, 0, 0, 0, 1, 0)
)

space_invader_1 = (
    (0, 0, 1, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 0, 0),
    (1, 1, 0, 1, 1, 0, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 1, 0, 0, 1, 0, 1),
    (0, 0, 0, 1, 1, 0, 0, 0)
)

def get_sprite(t, r, g, b):
    sprite = Sprite()
    for i in range(8):
        for j in range(8):
            if t[i][j] == 1:
                sprite.add(Led(i, j, r, g, b))
            else:
                sprite.add(Led(i, j, 0, 0, 0))
    return sprite

sprite0 = get_sprite(space_invader_0, 0, 255, 255)
sprite1 = get_sprite(space_invader_1, 255, 0, 255)

while True:
    sprite0.draw()
    time.sleep(1)
    sprite1.draw()
    time.sleep(1)

