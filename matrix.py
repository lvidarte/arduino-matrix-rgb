#!/usr/bin/python -i

import time
import random
import serial

try:
    conn = serial.Serial('/dev/ttyACM0', 9600)
except:
    conn = serial.Serial('/dev/ttyACM1', 9600)

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
        PARAM_OBJ_ROW: 'row',
        PARAM_OBJ_ALL: 'all',
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
        self.reset()

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

    def set_obj_led(self):
        """Sets the actual object to LED"""
        self._obj = self.PARAM_OBJ_LED

    def set_obj_row(self):
        """Sets the actual object to ROW"""
        self._obj = self.PARAM_OBJ_ROW

    def set_obj_col(self):
        """Sets the actual object to COL"""
        self._obj = self.PARAM_OBJ_COL

    def set_obj_all(self):
        """Sets the actual object to ALL"""
        self._obj = self.PARAM_OBJ_ALL

    def set_page_fg(self):
        """Sets the writing on page foreground"""
        self._page = self.PARAM_PAGE_FG

    def set_page_bg(self):
        """Sets the writing on page background"""
        self._page = self.PARAM_PAGE_BG

    def set_reset_on(self):
        """Sets the reset mode ON to put on 0
           all arduino state (xyrgb) after writing"""
        self._reset = self.PARAM_RESET_ON

    def set_reset_off(self):
        """Sets the reset mode OFF.
           Look help on set_reset_on"""
        self._reset = self.PARAM_RESET_OFF

    def flip(self):
        """Flip the page to change background by foreground"""
        self.send(self.CMD_FLIP, 0)

    def set_rgb(self, r=None, g=None, b=None):
        """Sets the rgb state"""
        self.r = r
        self.g = g
        self.b = b

    def set_rgb0(self, r=0, g=0, b=0):
        """Sets the rgb state, 0 by default"""
        self.set_rgb(r, g, b)

    def set_rand_rgb(self):
        """Sets randomly the rgb state"""
        self.r = random.randint(0, 15)
        self.g = random.randint(0, 15)
        self.b = random.randint(0, 15)

    def set_rand_x(self):
        """Sets randomly the x position"""
        self.x = random.randint(0, 7)

    def set_rand_y(self):
        """Sets randomly the y position"""
        self.y = random.randint(0, 7)

    def fill(self, obj=None, page=None, reset=None):
        """Fill the object with the actual state (xyrgb)"""
        obj   = self._get_obj(obj)
        page  = self._get_page(page)
        reset = self._get_reset(reset)
        param = obj | page | reset
        self.send(self.CMD_FILL, param)

    def set(self, x=None, y=None, r=None, g=None, b=None):
        """Sets the state (xyrgb) and fill the actual object"""
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fill()

    def set0(self, x=0, y=0, r=0, g=0, b=0):
        """Sets the state (xyrgb) and fill the actual object,
           0 by default"""
        self.fill(x, y, r, g, b)

    def set_led(self):
        self.fill(self.PARAM_OBJ_LED,
                  self._page,
                  self.PARAM_RESET_OFF)

    def set_led_bg(self):
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def set_led_fg(self):
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def set_col(self):
        self.fill(self.PARAM_OBJ_COL,
                  self._page,
                  self.PARAM_RESET_OFF)

    def set_col_bg(self):
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def set_col_fg(self):
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def set_row(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self._page,
                  self.PARAM_RESET_OFF)

    def set_row_bg(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def set_row_fg(self):
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def set_all(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self._page,
                  self.PARAM_RESET_OFF)

    def set_all_bg(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_BG,
                  self.PARAM_RESET_OFF)

    def set_all_fg(self):
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_FG,
                  self.PARAM_RESET_OFF)

    def clear(self, obj=None, page=None, reset=None):
        obj   = self._get_obj(obj)
        page  = self._get_page(page)
        reset = self._get_reset(reset)
        param = obj | page | reset
        self.send(self.CMD_CLEAR, param)

    def off(self):
        self.clear()

    def off_led(self):
        self.clear(self.PARAM_OBJ_LED,
                   self._page,
                   self.PARAM_RESET_OFF)

    def off_led_bg(self):
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def off_led_fg(self):
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def off_col(self):
        self.clear(self.PARAM_OBJ_COL,
                   self._page,
                   self.PARAM_RESET_OFF)

    def off_col_bg(self):
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def off_col_fg(self):
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def off_row(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self._page,
                   self.PARAM_RESET_OFF)

    def off_row_bg(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def off_row_fg(self):
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def off_all(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self._page,
                   self.PARAM_RESET_OFF)

    def off_all_bg(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_BG,
                   self.PARAM_RESET_OFF)

    def off_all_fg(self):
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_FG,
                   self.PARAM_RESET_OFF)

    def rect(self, x=None, y=None, w=3, h=3):
        x = x or self._x
        y = y or self._y
        for n in range(w):
            _x = x + n
            _y = y + h - 1
            self.set(x=_x, y=y)
            if y != _y:
                self.set(x=_x, y=_y)
        for m in range(h-2):
            _x = x + w - 1
            _y = y + m + 1
            self.set(x=x, y=_y)
            if x != _x:
                self.set(x=_x, y=_y) 
        self.x, self.y = x, y

    def square(self, x=None, y=None, size=3):
        self.rect(x, y, size, size)

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

    def reset(self):
        self.x = 0
        self.y = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.set_obj_led()
        self.set_page_fg()
        self.set_reset_off()
        self.off_all_bg()
        self.off_all_fg()

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
                self.PARAM_OBJ_NAMES[self._obj],
                self.PARAM_PAGE_NAMES[self._page],
                self.PARAM_RESET_NAMES[self._reset])


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

    #
    # Matrix !!
    #
    m = Matrix(conn)

    #
    # Examples !!
    #
    def random_dots(sec=.1, amount=10):
        """Draw dots on random position, random color"""
        m.reset()
        for i in range(amount):
            m.set_rand_x()
            m.set_rand_y()
            m.set_rand_rgb()
            m.fill()
            time.sleep(sec)

    def random_dots_forever_fg(sec=.1, amount=10):
        """Draw forever dots on random position on foreground, random color"""
        m.set_page_fg()
        while True:
            m.off_all()
            random_dots(sec, amount)

    def random_dots_forever_bg(sec=.1, amount=10):
        """Draw forever dots on random position on background, random color"""
        m.set_page_bg()
        while True:
            m.off_all_bg()
            random_dots(sec, amount)
            m.flip();

    def squares(sec=0):
        """Draw concentric squares, random color"""
        m.reset()
        m.x, m.y = 0, 0
        for i in range(4):
            m.set_rand_rgb()
            m.square(x=i, y=i, size=8-i*2)
            time.sleep(sec)

    def squares_forever_fg(sec=.1):
        """Draw forever concentric squares on foreground, random color"""
        m.set_page_fg()
        while True:
            squares(sec)

    def squares_forever_bg(sec=.1):
        """Draw forever concentric squares on background, random color"""
        m.set_page_bg()
        while True:
            squares(sec)
            m.flip()

    def rows(sec=.1):
        """Draw all rows, random color"""
        m.reset()
        m.set_obj_row()
        m.x = 0
        for i in range(8):
            m.y = i
            m.set_rand_rgb()
            m.fill()
            time.sleep(sec)

    def rows_forever_fg(sec=.1):
        """Draw forever all rows on foreground, random color"""
        m.set_page_fg()
        while True:
            rows()

    def rows_forever_bg(sec=.1):
        """Draw forever all rows on background, random color"""
        m.set_page_bg()
        while True:
            rows()
            m.flip()

    def cols(sec=.1):
        """Draw all cols, random color"""
        m.reset()
        m.set_obj_col()
        m.y = 0
        for i in range(8):
            m.x = i
            m.set_rand_rgb()
            m.fill()
            time.sleep(sec)

    def cols_forever_fg(sec=.1):
        """Draw forever all cols on foreground, random color"""
        m.set_page_fg()
        while True:
            cols()

    def cols_forever_bg(sec=.1):
        """Draw forever all cols on background, random color"""
        m.set_page_bg()
        while True:
            cols()
            m.flip()

    def random_lines(sec=.1, amount=5):
        """Draw rows and cols on random position, random color"""
        m.reset()
        for i in range(amount):
            m.set_rand_x()
            m.set_rand_y()
            m.set_rand_rgb()
            if random.randint(0, 1):
                m.set_col()
            else:
                m.set_row()
            time.sleep(sec)

    def random_lines_forever_fg(sec=.1, amount=5):
        """Draw forever rows and cols on random position,
           on foreground, random color"""
        m.set_page_fg()
        while True:
            random_lines(sec, amount)

    def random_lines_forever_bg(sec=.1, amount=5):
        """Draw forever rows and cols on random position,
           on background, random color"""
        m.set_page_bg()
        while True:
            random_lines(sec, amount)
            m.flip()

    def tunnel(sec=.1):
        m.reset()
        m.set_page_bg()
        m.set_rand_rgb()
        for i in range(4):
            m.off_all_bg()
            m.x = 3 - i
            m.y = 3 - i
            m.square(size=(i+1)*2)
            m.flip()
            time.sleep(sec)

    def tunnel_forever(sec=.1):
        while True:
            tunnel(sec)

    def demo(sec=.1):
        examples = (
            random_dots,
            squares,
            rows,
            cols,
            random_lines,
            tunnel,
        )
        while True:
            e = random.randint(0, len(examples) - 1)
            print e
            for i in range(random.randint(1, 10)):
                examples[e](sec)

