#!/usr/bin/python -i

import sys
import time
import random
import serial

try:
    conn = serial.Serial('/dev/ttyACM0', 9600)
except OSError:
    try:
        conn = serial.Serial('/dev/ttyACM1', 9600)
    except OSError:
        print "Can't connect to serial device"
        sys.exit(1)

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
                self._send(self.CMD_SET_X, value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value is not None:
            value &= self.MASK_POS
            if self._y != value:
                self._y = value
                self._send(self.CMD_SET_Y, value)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._r != value:
                self._r = value
                self._send(self.CMD_SET_R, value)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._g != value:
                self._g = value
                self._send(self.CMD_SET_G, value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value is not None:
            value &= self.MASK_COLOR
            if self._b != value:
                self._b = value
                self._send(self.CMD_SET_B, value)

    def set_obj_led(self):
        """Sets the actual object to 'led'"""
        self._obj = self.PARAM_OBJ_LED

    def set_obj_row(self):
        """Sets the actual object to 'row'"""
        self._obj = self.PARAM_OBJ_ROW

    def set_obj_col(self):
        """Sets the actual object to 'col'"""
        self._obj = self.PARAM_OBJ_COL

    def set_obj_all(self):
        """Sets the actual object to 'all'"""
        self._obj = self.PARAM_OBJ_ALL

    def set_page_fg(self):
        """Sets the writing on page foreground"""
        self._page = self.PARAM_PAGE_FG

    def set_page_bg(self):
        """Sets the writing on page background"""
        self._page = self.PARAM_PAGE_BG

    def set_reset_on(self):
        """Sets the reset mode on
           for put on 0 the arduino xyrgb state
           after fill or clear action"""
        self._reset = self.PARAM_RESET_ON

    def set_reset_off(self):
        """Sets the reset mode off.
           See set_reset_on help"""
        self._reset = self.PARAM_RESET_OFF

    def flip(self):
        """Flip the page to change background by foreground"""
        self._send(self.CMD_FLIP, 0)

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

    def fill(self, obj=None, page=None, reset=None):
        """Fill the object with the actual state (xyrgb)"""
        param = self._get_param(obj, page, reset)
        self._send(self.CMD_FILL, param)

    def fill_led(self):
        """Fill the object led on the actual page
           with the actual xyrgb state"""
        self.fill(self.PARAM_OBJ_LED,
                  self._page)

    def fill_led_bg(self):
        """Fill the object led on the background page
           with the actual xyrgb state"""
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_BG)

    def fill_led_fg(self):
        """Fill the object led on the foreground page
           with the actual xyrgb state"""
        self.fill(self.PARAM_OBJ_LED,
                  self.PARAM_PAGE_FG)

    def fill_col(self):
        """Fill the object col on the actual page
           with the actual xrgb state"""
        self.fill(self.PARAM_OBJ_COL,
                  self._page)

    def fill_col_bg(self):
        """Fill the object col on the background page
           with the actual xrgb state"""
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_BG)

    def fill_col_fg(self):
        """Fill the object col on the foreground page
           with the actual xrgb state"""
        self.fill(self.PARAM_OBJ_COL,
                  self.PARAM_PAGE_FG)

    def fill_row(self):
        """Fill the object row on the actual page
           with the actual yrgb state"""
        self.fill(self.PARAM_OBJ_ROW,
                  self._page)

    def fill_row_bg(self):
        """Fill the object row on the background page
           with the actual yrgb state"""
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_BG)

    def fill_row_fg(self):
        """Fill the object row on the foreground page
           with the actual yrgb state"""
        self.fill(self.PARAM_OBJ_ROW,
                  self.PARAM_PAGE_FG)

    def fill_all(self):
        """Fill the object all on the actual page
           with the actual rgb state"""
        self.fill(self.PARAM_OBJ_ALL,
                  self._page)

    def fill_all_bg(self):
        """Fill the object all on the background page
           with the actual rgb state"""
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_BG)

    def fill_all_fg(self):
        """Fill the object all on the foreground page
           with the actual rgb state"""
        self.fill(self.PARAM_OBJ_ALL,
                  self.PARAM_PAGE_FG)

    def clear(self, obj=None, page=None, reset=None):
        """Clear the object"""
        param = self._get_param(obj, page, reset)
        self._send(self.CMD_CLEAR, param)

    def clear_led(self):
        """Clear the object led on the actual page"""
        self.clear(self.PARAM_OBJ_LED,
                   self._page)

    def clear_led_bg(self):
        """Clear the object led on the background page"""
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_BG)

    def clear_led_fg(self):
        """Clear the object led on the foreground page"""
        self.clear(self.PARAM_OBJ_LED,
                   self.PARAM_PAGE_FG)

    def clear_col(self):
        """Clear the object col on the actual page"""
        self.clear(self.PARAM_OBJ_COL,
                   self._page)

    def clear_col_bg(self):
        """Clear the object col on the background page"""
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_BG)

    def clear_col_fg(self):
        """Clear the object col on the foreground page"""
        self.clear(self.PARAM_OBJ_COL,
                   self.PARAM_PAGE_FG)

    def clear_row(self):
        """Clear the object row on the actual page"""
        self.clear(self.PARAM_OBJ_ROW,
                   self._page)

    def clear_row_bg(self):
        """Clear the object row on the background page"""
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_BG)

    def clear_row_fg(self):
        """Clear the object row on the foreground page"""
        self.clear(self.PARAM_OBJ_ROW,
                   self.PARAM_PAGE_FG)

    def clear_all(self):
        """Clear the object all on the actual page"""
        self.clear(self.PARAM_OBJ_ALL,
                   self._page)

    def clear_all_bg(self):
        """Clear the object all on the background page"""
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_BG)

    def clear_all_fg(self):
        """Clear the object all on the foreground page"""
        self.clear(self.PARAM_OBJ_ALL,
                   self.PARAM_PAGE_FG)

    def rect(self, x=None, y=None, width=3, height=3):
        """Draw a rectangle"""
        if x is None:
            x = self._x
        if y is None:
            y = self._y
        for n in range(width):
            _x = x + n
            _y = y + height - 1
            self.set(x=_x, y=y)
            if y != _y:
                self.set(x=_x, y=_y)
        for m in range(height - 2):
            _x = x + width - 1
            _y = y + m + 1
            self.set(x=x, y=_y)
            if x != _x:
                self.set(x=_x, y=_y) 
        self.x, self.y = x, y

    def square(self, x=None, y=None, size=3):
        """Draw a square"""
        self.rect(x, y, size, size)

    def line_horizontal(self, x=None, y=None, size=5):
        """Draw a horizontal line"""
        self.rect(x=x, y=y, width=size, height=1)

    def line_vertical(self, x=None, y=None, size=5):
        """Draw a vertical line"""
        self.rect(x=x, y=y, width=1, height=size)

    def _get_param(self, obj, page, reset):
        obj   = self._get_obj(obj)
        page  = self._get_page(page)
        reset = self._get_reset(reset)
        param = obj | page | reset
        return param

    def _get_obj(self, obj=None):
        return self._get_value('obj', obj)

    def _get_page(self, page=None):
        return self._get_value('page', page)

    def _get_reset(self, reset=None):
        return self._get_value('reset', reset)

    def _get_value(self, name, value=None):
        if value is None:
            return getattr(self, '_%s' % name)
        else:
            return value

    def reset(self):
        """Reset the matrix to initial status"""
        self.x = 0
        self.y = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.set_obj_led()
        self.set_page_fg()
        self.set_reset_off()
        self.clear_all_bg()
        self.clear_all_fg()

    def set_debug_on(self):
        """Set on verbosity on arduino"""
        self._send(self.CMD_DEBUG, self.PARAM_DEBUG_ON)

    def set_debug_off(self):
        """Set off verbosity on arduino"""
        self._send(self.CMD_DEBUG, self.PARAM_DEBUG_OFF)

    def _send(self, command, param):
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


    from functools import wraps

    class Demo:

        def __init__(self, matrix):
            self.matrix = matrix

        def _interruptible(f):
            @wraps(f)
            def wrapped(self, *args, **kwargs):
                try:
                    f(self, *args, **kwargs)
                except KeyboardInterrupt:
                    self.matrix.reset()
                    print ""
            return wrapped

        def _rand_dots(self, sec, times):
            for i in range(times):
                self.matrix.set_rand_x()
                self.matrix.set_rand_y()
                self.matrix.set_rand_rgb()
                self.matrix.fill_led()
                time.sleep(sec)

        def rand_dots(self, sec=.1, times=10):
            """Draw dots on random position, random color"""
            self.matrix.reset()
            self._rand_dots(sec, times)

        @_interruptible
        def rand_dots_forever_fg(self, sec=.1, times=10):
            """Draw forever dots on random position on foreground,
               random color"""
            self.matrix.reset()
            while True:
                self.matrix.clear_all()
                self._rand_dots(sec, times)

        @_interruptible
        def rand_dots_forever_bg(self, sec=.1, times=10):
            """Draw forever dots on random position on background,
               random color"""
            self.matrix.reset()
            self.matrix.set_page_bg()
            while True:
                self.matrix.clear_all()
                self._rand_dots(sec, times)
                self.matrix.flip()

        def _squares(self, sec):
            self.matrix.x, self.matrix.y = 0, 0
            for i in range(4):
                self.matrix.set_rand_rgb()
                self.matrix.square(x=i, y=i, size=8-i*2)
                time.sleep(sec)

        def squares(self, sec=.1):
            """Draw concentric squares, random color"""
            self.matrix.reset()
            self._squares(sec)

        @_interruptible
        def squares_forever_fg(self, sec=.1):
            """Draw forever concentric squares on foreground,
               random color"""
            self.matrix.reset()
            while True:
                self.matrix.clear_all()
                self._squares(sec)

        @_interruptible
        def squares_forever_bg(self, sec=.1):
            """Draw forever concentric squares on background,
               random color"""
            self.matrix.reset()
            self.matrix.set_page_bg()
            while True:
                self.matrix.clear_all_bg()
                self._squares(sec)
                self.matrix.flip()

        def _rows(self, sec):
            self.matrix.x = 0
            for i in range(8):
                self.matrix.y = i
                self.matrix.set_rand_rgb()
                self.matrix.fill_row()
                time.sleep(sec)

        def rows(self, sec=.1):
            """Draw all rows, random color"""
            self.matrix.reset()
            self._rows(sec)

        @_interruptible
        def rows_forever_fg(self, sec=.1):
            """Draw forever all rows on foreground,
               random color"""
            self.matrix.reset()
            while True:
                self._rows(sec)

        @_interruptible
        def rows_forever_bg(self, sec=.1):
            """Draw forever all rows on background,
               random color"""
            self.matrix.reset()
            self.matrix.set_page_bg()
            while True:
                self._rows(sec)
                self.matrix.flip()

        def _cols(self, sec):
            self.matrix.y = 0
            for i in range(8):
                self.matrix.x = i
                self.matrix.set_rand_rgb()
                self.matrix.fill_col()
                time.sleep(sec)

        def cols(self, sec=.1):
            """Draw all cols, random color"""
            self.matrix.reset()
            self._cols(sec)

        @_interruptible
        def cols_forever_fg(self, sec=.1):
            """Draw forever all cols on foreground"""
            self.matrix.reset()
            while True:
                self.matrix.clear_all()
                self._cols(sec)

        @_interruptible
        def cols_forever_bg(self, sec=.1):
            """Draw forever all cols on background,
               random color"""
            self.matrix.reset()
            self.matrix.set_page_bg()
            while True:
                self._cols(sec)
                self.matrix.flip()

        def _rand_lines(self, sec, times):
            for i in range(times):
                self.matrix.set_rand_x()
                self.matrix.set_rand_y()
                self.matrix.set_rand_rgb()
                if random.randint(0, 1):
                    self.matrix.fill_col()
                else:
                    self.matrix.fill_row()
                time.sleep(sec)

        def rand_lines(self, sec=.1, times=5):
            """Draw rows and cols on random position,
               random color"""
            self.matrix.reset()
            self._rand_lines(sec, times)

        @_interruptible
        def rand_lines_forever_fg(self, sec=.1, times=5):
            """Draw forever rows and cols on random position,
               on foreground, random color"""
            self.matrix.reset()
            while True:
                self.matrix.clear_all()
                self._rand_lines(sec, times)

        @_interruptible
        def rand_lines_forever_bg(self, sec=.1, times=5):
            """Draw forever rows and cols on random position,
               on background, random color"""
            self.matrix.reset()
            self.matrix.set_page_bg()
            while True:
                self.matrix.clear_all()
                self._rand_lines(sec, times)
                self.matrix.flip()

        def _tunnel(self, sec):
            self.matrix.set_page_bg()
            self.matrix.set_rand_rgb()
            for i in range(4):
                self.matrix.clear_all_bg()
                self.matrix.x = 3 - i
                self.matrix.y = 3 - i
                self.matrix.square(size=(i+1)*2)
                self.matrix.flip()
                time.sleep(sec)

        def tunnel(self, sec=.1):
            """Draw a tunnel, random color"""
            self.matrix.reset()
            self._tunnel(sec)

        @_interruptible
        def tunnel_forever(self, sec=.1):
            """Draw a tunnel forever, random color"""
            self.matrix.reset()
            while True:
                self._tunnel(sec)

        def _chessboard(self, sec, page):
            self.matrix._page = page
            chessboards = [
                [0, 2, 5, 7, 8, 10, 13, 15],
                [1, 3, 4, 6, 9, 11, 12, 14],
            ]
            for i in (0, 1):
                self.matrix.clear_all()
                random.shuffle(chessboards[i])
                for s in chessboards[i]:
                    x = (s % 4) * 2
                    y = (s / 4) * 2
                    self.matrix.set_rand_rgb()
                    self.matrix.square(x, y, 2)
                    time.sleep(sec)
                if page == self.matrix.PARAM_PAGE_BG:
                    self.matrix.flip()
                    time.sleep(sec * 8)

        def chessboard(self, sec=.1, page=None):
            """Draw a chessboard with random color cells"""
            self.matrix.reset()
            self._chessboard(sec, self.matrix.PARAM_PAGE_FG)

        @_interruptible
        def chessboard_forever_fg(self, sec=.1):
            """Draw forever a chessboard on foreground
               with random color cells"""
            self.matrix.reset()
            while True:
                self._chessboard(sec, self.matrix.PARAM_PAGE_FG)

        @_interruptible
        def chessboard_forever_bg(self, sec=.1):
            """Draw forever a chessboard on background
               with random color cells"""
            self.matrix.reset()
            while True:
                self._chessboard(sec, page=self.matrix.PARAM_PAGE_BG)

        def _degree(self, sec, page):
            self.matrix._page = page
            self.matrix.set_obj_row()
            self.matrix.x = 0
            for i in range(1, 8):
                for y, n in enumerate(range(1, 16, 2)):
                    r = i & 1 and n or 0
                    g = i & 2 and n or 0
                    b = i & 4 and n or 0
                    self.matrix.set(y=y, r=r, g=g, b=b)
                    time.sleep(sec)
                if page == self.matrix.PARAM_PAGE_BG:
                    self.matrix.flip()

        def degree(self, sec=.1):
            """Draw lines of degree colors"""
            self.matrix.reset()
            self._degree(sec, page=self.matrix.PARAM_PAGE_FG)

        @_interruptible
        def degree_forever_fg(self, sec=.1):
            """Draw forever lines of degree colors on foreground"""
            self.matrix.reset()
            while True:
                self._degree(sec, page=self.matrix.PARAM_PAGE_FG)

        @_interruptible
        def degree_forever_bg(self, sec=.1):
            """Draw forever lines of degree colors on background"""
            self.matrix.reset()
            while True:
                self._degree(sec, page=self.matrix.PARAM_PAGE_BG)

        @_interruptible
        def start(self, sec=.1):
            """Run all demos in random order"""
            from itertools import cycle
            times = 5
            demos = [
                (self.rand_dots, times),
                (self.squares, times),
                (self.rows, times),
                (self.cols, times),
                (self.rand_lines, times),
                (self.tunnel, times),
                (self.chessboard, times),
                (self.degree, 1),
            ]
            random.shuffle(demos)
            for f, times in cycle(demos):
                print "%s(sec=%s) " % (f.__name__, sec)
                for i in range(times):
                    f(sec)

    matrix = Matrix(conn)
    demo = Demo(matrix)

