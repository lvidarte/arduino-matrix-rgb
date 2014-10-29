import time
import random
from functools import wraps
from matrix import PARAM_PAGE_FG, PARAM_PAGE_BG


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
            if page == PARAM_PAGE_BG:
                self.matrix.flip()
                time.sleep(sec * 8)

    def chessboard(self, sec=.1, page=None):
        """Draw a chessboard with random color cells"""
        self.matrix.reset()
        self._chessboard(sec, PARAM_PAGE_FG)

    @_interruptible
    def chessboard_forever_fg(self, sec=.1):
        """Draw forever a chessboard on foreground
           with random color cells"""
        self.matrix.reset()
        while True:
            self._chessboard(sec, PARAM_PAGE_FG)

    @_interruptible
    def chessboard_forever_bg(self, sec=.1):
        """Draw forever a chessboard on background
           with random color cells"""
        self.matrix.reset()
        while True:
            self._chessboard(sec, page=PARAM_PAGE_BG)

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
            if page == PARAM_PAGE_BG:
                self.matrix.flip()

    def degree(self, sec=.1):
        """Draw lines of degree colors"""
        self.matrix.reset()
        self._degree(sec, page=PARAM_PAGE_FG)

    @_interruptible
    def degree_forever_fg(self, sec=.1):
        """Draw forever lines of degree colors on foreground"""
        self.matrix.reset()
        while True:
            self._degree(sec, page=PARAM_PAGE_FG)

    @_interruptible
    def degree_forever_bg(self, sec=.1):
        """Draw forever lines of degree colors on background"""
        self.matrix.reset()
        while True:
            self._degree(sec, page=PARAM_PAGE_BG)

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

