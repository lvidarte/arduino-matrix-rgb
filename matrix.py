#!/usr/bin/python -i

import serial
conn = serial.Serial('/dev/ttyACM0', 9600)

class Matrix(object):

    CMD_CLEAR = 0b0000
    CMD_FLIP  = 0b0001
    CMD_SET_X = 0b1000
    CMD_SET_Y = 0b1001
    CMD_SET_R = 0b1010
    CMD_SET_G = 0b1011
    CMD_SET_B = 0b1100
    CMD_DEBUG = 0b1110
    CMD_FILL  = 0b1111

    PARAM_OBJ_LED   =   0b00
    PARAM_OBJ_COL   =   0b01
    PARAM_OBJ_ROW   =   0b10
    PARAM_OBJ_ALL   =   0b11
    PARAM_PAGE_BG   =  0b000
    PARAM_PAGE_FG   =  0b100
    PARAM_RESET_OFF = 0b0000
    PARAM_RESET_ON  = 0b1000
    PARAM_DEBUG_OFF =    0b0
    PARAM_DEBUG_ON  =    0b1

    MASK_POS   = 0b0111
    MASK_COLOR = 0b1111

    PARAM_OBJ_NAMES = {
        PARAM_OBJ_LED: 'led',
        PARAM_OBJ_COL: 'col',
    }

    PARAM_PAGE_NAMES = {
        PARAM_PAGE_BG: 'bg',
        PARAM_PAGE_FG: 'fg',
    }

    PARAM_RESET_NAMES = {
        PARAM_RESET_ON : 'on',
        PARAM_RESET_OFF: 'off',
    }

    def __init__(self, conn):
        self.conn = conn
        self._x = None
        self._y = None
        self._r = None
        self._g = None
        self._b = None
        self.reset_all()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value is not None:
            value &= self.MASK_POS
            if self._x != value:
                self._x = value
                self.send(self.CMD_SET_X, value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value is not None:
            value &= self.MASK_POS
            if self._y != value:
                self._y = value
                self.send(self.CMD_SET_Y, value)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._r != value:
                self._r = value
                self.send(self.CMD_SET_R, value)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._g != value:
                self._g = value
                self.send(self.CMD_SET_G, value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._b != value:
                self._b = value
                self.send(self.CMD_SET_B, value)

    def set(self, x=None, y=None, r=None, g=None, b=None):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fill()

    def set0(self, x=0, y=0, r=0, g=0, b=0):
        self.set(x, y, r, g, b)

    @property
    def obj(self):
        return self.PARAM_OBJ_NAMES[self._obj]

    def set_obj_led(self):
        self._obj = self.PARAM_OBJ_LED

    def set_obj_row(self):
        self._obj = self.PARAM_OBJ_ROW

    def set_obj_col(self):
        self._obj = self.PARAM_OBJ_COL

    def set_obj_all(self):
        self._obj = self.PARAM_OBJ_ALL

    @property
    def page(self):
        return self.PARAM_PAGE_NAMES[self._page]

    def set_page_fg(self):
        self._page = self.PARAM_PAGE_FG

    def set_page_bg(self):
        self._page = self.PARAM_PAGE_BG

    @property
    def reset(self):
        return self.PARAM_RESET_NAMES[self._reset]

    def set_reset_on(self):
        self._reset = self.PARAM_RESET_ON

    def set_reset_off(self):
        self._reset = self.PARAM_RESET_OFF

    def flip(self):
        self.send(self.CMD_FLIP, 0)

    def fill(self, obj=None, page=None, reset=None):
        obj   = self._get_obj(obj)
        page  = self._get_page(page)
        reset = self._get_reset(reset)
        param = obj | page | reset
        self.send(self.CMD_FILL, param)

    def fill_led(self):
        self.fill(self.PARAM_OBJ_LED,
                  self._page,
                  self.PARAM_RESET_OFF)

    def fill_led_bg(self):
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def fill_led_fg(self):
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def fill_col(self):
        self.fill(self.PARAM_OBJ_COL,
                  self._page,
                  self.PARAM_RESET_OFF)

    def fill_col_bg(self):
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def fill_col_fg(self):
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def fill_row(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self._page,
                  self.PARAM_RESET_OFF)

    def fill_row_bg(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def fill_row_fg(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def fill_all(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self._page,
                  self.PARAM_RESET_OFF)

    def fill_all_bg(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def fill_all_fg(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def clear(self, obj=None, page=None, reset=None):
        obj   = self._get_obj(obj)
        page  = self._get_page(page)
        reset = self._get_reset(reset)
        param = obj | page | reset
        self.send(self.CMD_CLEAR, param)

    def clear_led(self):
        self.clear(self.PARAM_OBJ_LED,
                   self._page,
                   self.PARAM_RESET_OFF)

    def clear_led_bg(self):
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def clear_led_fg(self):
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def clear_col(self):
        self.clear(self.PARAM_OBJ_COL,
                   self._page,
                   self.PARAM_RESET_OFF)

    def clear_col_bg(self):
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def clear_col_fg(self):
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def clear_row(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self._page,
                   self.PARAM_RESET_OFF)

    def clear_row_bg(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def clear_row_fg(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def clear_all(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self._page,
                   self.PARAM_RESET_OFF)

    def clear_all_bg(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def clear_all_fg(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def _get_value(self, name, value=None):
        if value is None:
            return getattr(self, '_%s' % name)
        else:
            return value

    def _get_obj(self, obj=None):
        return self._get_value('obj', obj)

    def _get_page(self, page=None):
        return self._get_value('page', page)

    def _get_reset(self, reset=None):
        return self._get_value('reset', reset)

    def reset_matrix(self):
        self.x = 0
        self.y = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.set_obj_led()
        self.set_page_fg()
        self.set_reset_off()

    def reset_all(self):
        self.reset_matrix()
        self.clear_all_bg()
        self.clear_all_fg()

    def set_debug_on(self):
        self.send(self.CMD_DEBUG, self.PARAM_DEBUG_ON)

    def set_debug_off(self):
        self.send(self.CMD_DEBUG, self.PARAM_DEBUG_OFF)

    def send(self, command, param):
        self.msg = chr((command << 4) + param)
        self.conn.write(self.msg)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "xy(%s, %s) rgb(%s, %s, %s) obj:%s page:%s reset:%s" % (
                self.x, self.y, self.r, self.g, self.b, 
                self.obj, self.page, self.reset) 


if __name__ == '__main__':

    # Shell mode

    import atexit
    import os
    import readline
    import rlcompleter

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

    m = Matrix(conn)

