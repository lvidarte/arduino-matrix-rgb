import random


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


class Matrix(object):

    def __init__(self, serial):
        self.serial = serial
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
            value &= MASK_POS
            if self._x != value:
                self._x = value
                self._send(CMD_SET_X, value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value is not None:
            value &= MASK_POS
            if self._y != value:
                self._y = value
                self._send(CMD_SET_Y, value)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if value is not None:
            value &= MASK_COLOR
            if self._r != value:
                self._r = value
                self._send(CMD_SET_R, value)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value is not None:
            value &= MASK_COLOR
            if self._g != value:
                self._g = value
                self._send(CMD_SET_G, value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value is not None:
            value &= MASK_COLOR
            if self._b != value:
                self._b = value
                self._send(CMD_SET_B, value)

    def set_obj_led(self):
        """Sets the actual object to 'led'"""
        self._obj = PARAM_OBJ_LED

    def set_obj_row(self):
        """Sets the actual object to 'row'"""
        self._obj = PARAM_OBJ_ROW

    def set_obj_col(self):
        """Sets the actual object to 'col'"""
        self._obj = PARAM_OBJ_COL

    def set_obj_all(self):
        """Sets the actual object to 'all'"""
        self._obj = PARAM_OBJ_ALL

    def set_page_fg(self):
        """Sets the writing on page foreground"""
        self._page = PARAM_PAGE_FG

    def set_page_bg(self):
        """Sets the writing on page background"""
        self._page = PARAM_PAGE_BG

    def set_reset_on(self):
        """Sets the reset mode on
           for put on 0 the arduino xyrgb state
           after fill or clear action"""
        self._reset = PARAM_RESET_ON

    def set_reset_off(self):
        """Sets the reset mode off.
           See set_reset_on help"""
        self._reset = PARAM_RESET_OFF

    def flip(self):
        """Flip the page to change background by foreground"""
        self._send(CMD_FLIP, 0)

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
        self._send(CMD_FILL, param)

    def fill_led(self):
        """Fill the object led on the actual page
           with the actual xyrgb state"""
        self.fill(PARAM_OBJ_LED,
                  self._page)

    def fill_led_bg(self):
        """Fill the object led on the background page
           with the actual xyrgb state"""
        self.fill(PARAM_OBJ_LED,
                  PARAM_PAGE_BG)

    def fill_led_fg(self):
        """Fill the object led on the foreground page
           with the actual xyrgb state"""
        self.fill(PARAM_OBJ_LED,
                  PARAM_PAGE_FG)

    def fill_col(self):
        """Fill the object col on the actual page
           with the actual xrgb state"""
        self.fill(PARAM_OBJ_COL,
                  self._page)

    def fill_col_bg(self):
        """Fill the object col on the background page
           with the actual xrgb state"""
        self.fill(PARAM_OBJ_COL,
                  PARAM_PAGE_BG)

    def fill_col_fg(self):
        """Fill the object col on the foreground page
           with the actual xrgb state"""
        self.fill(PARAM_OBJ_COL,
                  PARAM_PAGE_FG)

    def fill_row(self):
        """Fill the object row on the actual page
           with the actual yrgb state"""
        self.fill(PARAM_OBJ_ROW,
                  self._page)

    def fill_row_bg(self):
        """Fill the object row on the background page
           with the actual yrgb state"""
        self.fill(PARAM_OBJ_ROW,
                  PARAM_PAGE_BG)

    def fill_row_fg(self):
        """Fill the object row on the foreground page
           with the actual yrgb state"""
        self.fill(PARAM_OBJ_ROW,
                  PARAM_PAGE_FG)

    def fill_all(self):
        """Fill the object all on the actual page
           with the actual rgb state"""
        self.fill(PARAM_OBJ_ALL,
                  self._page)

    def fill_all_bg(self):
        """Fill the object all on the background page
           with the actual rgb state"""
        self.fill(PARAM_OBJ_ALL,
                  PARAM_PAGE_BG)

    def fill_all_fg(self):
        """Fill the object all on the foreground page
           with the actual rgb state"""
        self.fill(PARAM_OBJ_ALL,
                  PARAM_PAGE_FG)

    def clear(self, obj=None, page=None, reset=None):
        """Clear the object"""
        param = self._get_param(obj, page, reset)
        self._send(CMD_CLEAR, param)

    def clear_led(self):
        """Clear the object led on the actual page"""
        self.clear(PARAM_OBJ_LED,
                   self._page)

    def clear_led_bg(self):
        """Clear the object led on the background page"""
        self.clear(PARAM_OBJ_LED,
                   PARAM_PAGE_BG)

    def clear_led_fg(self):
        """Clear the object led on the foreground page"""
        self.clear(PARAM_OBJ_LED,
                   PARAM_PAGE_FG)

    def clear_col(self):
        """Clear the object col on the actual page"""
        self.clear(PARAM_OBJ_COL,
                   self._page)

    def clear_col_bg(self):
        """Clear the object col on the background page"""
        self.clear(PARAM_OBJ_COL,
                   PARAM_PAGE_BG)

    def clear_col_fg(self):
        """Clear the object col on the foreground page"""
        self.clear(PARAM_OBJ_COL,
                   PARAM_PAGE_FG)

    def clear_row(self):
        """Clear the object row on the actual page"""
        self.clear(PARAM_OBJ_ROW,
                   self._page)

    def clear_row_bg(self):
        """Clear the object row on the background page"""
        self.clear(PARAM_OBJ_ROW,
                   PARAM_PAGE_BG)

    def clear_row_fg(self):
        """Clear the object row on the foreground page"""
        self.clear(PARAM_OBJ_ROW,
                   PARAM_PAGE_FG)

    def clear_all(self):
        """Clear the object all on the actual page"""
        self.clear(PARAM_OBJ_ALL,
                   self._page)

    def clear_all_bg(self):
        """Clear the object all on the background page"""
        self.clear(PARAM_OBJ_ALL,
                   PARAM_PAGE_BG)

    def clear_all_fg(self):
        """Clear the object all on the foreground page"""
        self.clear(PARAM_OBJ_ALL,
                   PARAM_PAGE_FG)

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
        self._send(CMD_DEBUG, PARAM_DEBUG_ON)

    def set_debug_off(self):
        """Set off verbosity on arduino"""
        self._send(CMD_DEBUG, PARAM_DEBUG_OFF)

    def _send(self, command, param):
        self.msg = chr((command << 4) + param)
        self.serial.write(self.msg)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "xy(%s, %s) rgb(%s, %s, %s) obj:%s page:%s reset:%s" % (
                self.x, self.y, self.r, self.g, self.b, 
                PARAM_OBJ_NAMES[self._obj],
                PARAM_PAGE_NAMES[self._page],
                PARAM_RESET_NAMES[self._reset])

