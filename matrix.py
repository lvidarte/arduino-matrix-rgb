#!/usr/bin/python -i

import serial

conn = serial.Serial('/dev/ttyACM0', 9600)

CMD_CLEAR = 0b0000
CMD_FLIP  = 0b0001
CMD_SET_X = 0b1000
CMD_SET_Y = 0b1001
CMD_SET_R = 0b1010
CMD_SET_G = 0b1011
CMD_SET_B = 0b1100
CMD_FILL  = 0b1111

PARAM_OBJ_LED =   0b00
PARAM_OBJ_COL =   0b01
PARAM_OBJ_ROW =   0b10
PARAM_OBJ_ALL =   0b11
PARAM_PAGE_BG =  0b000
PARAM_PAGE_FG =  0b100
PARAM_NORST   = 0b0000
PARAM_RESET   = 0b1000

MASK_POS   = 0b111
MASK_COLOR = 0b1111


class Matrix:

    x = None
    y = None
    r = None
    g = None
    b = None

    def __init__(self, conn):
        self.conn = conn
        self.reset_internals()

    def set(self, x=None, y=None, r=None, g=None, b=None):
        if x is not None:
            self.set_x(x)
        if y is not None:
            self.set_y(y)
        if r is not None:
            self.set_r(r)
        if g is not None:
            self.set_g(g)
        if b is not None:
            self.set_b(b)
        self.fill()

    def set_page_fg(self):
        self.page = PARAM_PAGE_FG

    def set_page_bg(self):
        self.page = PARAM_PAGE_BG

    def set_obj_led(self):
        self.obj = PARAM_OBJ_LED

    def set_obj_row(self):
        self.obj = PARAM_OBJ_ROW

    def set_obj_col(self):
        self.obj = PARAM_OBJ_COL

    def set_obj_all(self):
        self.obj = PARAM_OBJ_ALL

    def set_reset_on(self):
        self.reset = PARAM_RESET

    def set_reset_off(self):
        self.reset = PARAM_NORST

    def set_x(self, x):
        x &= MASK_POS
        if x != self.x:
            self.x = x
            self.send(CMD_SET_X, self.x)

    def set_y(self, y):
        y &= MASK_POS
        if y != self.y:
            self.y = y
            self.send(CMD_SET_Y, self.y)

    def set_r(self, r):
        r &= MASK_COLOR
        if r != self.r:
            self.r = r
            self.send(CMD_SET_R, self.r)

    def set_g(self, g):
        g &= MASK_COLOR
        if g != self.g:
            self.g = g
            self.send(CMD_SET_G, self.g)

    def set_b(self, b):
        b &= MASK_COLOR
        if b != self.b:
            self.b = b
            self.send(CMD_SET_B, self.b)

    def flip(self):
        self.send(CMD_FLIP, 0)

    def fill(self, obj=None, page=None, reset=None):
        obj   = self.get_obj(obj)
        page  = self.get_page(page)
        reset = self.get_reset(reset)
        param = obj | page | reset
        self.send(CMD_FILL, param)

    def clear(self, obj=None, page=None, reset=None):
        obj   = self.get_obj(obj)
        page  = self.get_page(page)
        reset = self.get_reset(reset)
        param = obj | page | reset
        self.send(CMD_CLEAR, param)

    def get_obj(self, obj=None):
        if obj is None:
            return self.obj
        else:
            return obj

    def get_reset(self, reset=None):
        if reset is None:
            return self.reset
        else:
            return reset

    def get_page(self, page=None):
        if page is None:
            return self.page
        else:
            return page

    def reset_internals(self):
        self.set_x(0)
        self.set_y(0)
        self.set_r(0)
        self.set_g(0)
        self.set_b(0)
        self.set_obj_led()
        self.set_page_fg()
        self.set_reset_off()

    def reset2(self):
        self.reset_internals()
        self.fill(PARAM_OBJ_ALL, PARAM_PAGE_FG, PARAM_RESET)
        self.fill(PARAM_OBJ_ALL, PARAM_PAGE_BG, PARAM_NORST)

    def send(self, command, param):
        self.msg = chr((command << 4) + param)
        self.conn.write(self.msg)

    def __str__(self):
        s = "xy(%s, %s) rgb(%s, %s, %s) obj=%s page=%s reset=%s"
        return s % (self.x, self.y, self.r, self.g, self.b,
                    self.obj, self.page, self.reset)


class Led:
    def __init__(self, x=0, y=0, r=0, g=0, b=0):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

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
    import atexit
    import os
    import readline
    import rlcompleter

    historyPath = os.path.expanduser("~/.pyhistory")

    #readline.parse_and_bind('tab: menu-complete')
    readline.parse_and_bind('tab: complete')

    def save_history(historyPath=historyPath):
        import readline
        readline.write_history_file(historyPath)

    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)

    atexit.register(save_history)
    del os, atexit, readline, rlcompleter, save_history, historyPath

    m = Matrix(conn)

