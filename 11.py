#!/bin/python

import sys
import random
import time
import curses


class Awesome11:

    KEYS = {
        'h': 'left',
        'j': 'bottom',
        'k': 'top',
        'l': 'right'
    }

    COLORS = {
         1: (curses.COLOR_YELLOW,  curses.COLOR_BLACK),
         2: (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
         3: (curses.COLOR_RED,     curses.COLOR_BLACK),
         4: (curses.COLOR_GREEN,   curses.COLOR_BLACK),
         5: (curses.COLOR_BLUE,    curses.COLOR_BLACK),
         6: (curses.COLOR_CYAN,    curses.COLOR_BLACK),
         7: (curses.COLOR_BLACK,   curses.COLOR_YELLOW),
         8: (curses.COLOR_WHITE,   curses.COLOR_MAGENTA),
         9: (curses.COLOR_WHITE,   curses.COLOR_RED),
        10: (curses.COLOR_WHITE,   curses.COLOR_GREEN),
        11: (curses.COLOR_WHITE,   curses.COLOR_BLUE),
        12: (curses.COLOR_WHITE,   curses.COLOR_CYAN),
    }

    SLEEP_BEFORE_ADD = .2

    def __init__(self, size=4):
        self.size = size
        self.init_screen()

    def init_screen(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        for val, colors in self.COLORS.items():
            fg, bg = colors
            curses.init_pair(val, fg, bg)

    def init_board(self):
        self.board = [[0 for i in range(self.size)]
                         for j in range(self.size)]

    def play(self):
        self.init_board()
        self.add()
        self.add()
        while True:
            key = self.screen.getkey()
            if key in self.KEYS.keys():
                self.move(self.KEYS[key])
            elif key == 'q':
                self.quit()

    def quit(self):
        curses.endwin()
        sys.exit(0)

    def move(self, direction):
        board = getattr(self, 'move_%s' % direction)()
        if board != self.board:
            self.board = board
            self.draw()
            self.add()

    def move_left(self):
        board = []
        for i, _ in enumerate(self.board):
            row = self.row_to_left(self.board[i][:])
            board.append(row)
        return board

    def move_right(self):
        board = []
        for i, _ in enumerate(self.board):
            row = self.row_to_left(self.board[i][::-1])
            board.append(row[::-1])
        return board

    def move_top(self):
        actual_board = self.get_rotated_ccw(self.board)
        board = []
        for i, _ in enumerate(actual_board):
            row = self.row_to_left(actual_board[i])
            board.append(row)
        return self.get_rotated_cw(board)

    def move_bottom(self):
        actual_board = self.get_rotated_cw(self.board)
        board = []
        for i, _ in enumerate(actual_board):
            row = self.row_to_left(actual_board[i])
            board.append(row)
        return self.get_rotated_ccw(board)

    def get_rotated_cw(self, board):
        return [list(e) for e in zip(*board[::-1])]

    def get_rotated_ccw(self, board):
        return [list(e) for e in zip(*board)[::-1]]

    def row_to_left(self, row):
        for i in range(self.size - 1):
            for _ in range(self.size - 1 - i):
                if row[i] == 0:
                    row.pop(i)
                    row.append(0)
                else:
                    break
            for _ in range(self.size - 2 - i):
                if row[i + 1] == 0:
                    row.pop(i + 1)
                    row.append(0)
                else:
                    break
            if row[i] != 0 and row[i] == row[i + 1]:
                row.pop(i)
                row[i] += 1
                row.append(0)
        return row

    def add(self):
        empty = []
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val == 0:
                    empty.append((x, y))
        if len(empty):
            x, y = random.choice(empty)
            self.board[y][x] = 1
        time.sleep(self.SLEEP_BEFORE_ADD)
        self.draw()

    def draw(self):
        self.screen.clear()
        for row in self.board:
            for val in row:
                self.draw_val(val)
            self.screen.addstr("\n")
        self.screen.refresh()

    def draw_val(self, val):
        if val < 10:
            sep = '  '
        else:
            sep = ' '
        self.screen.addstr(sep)
        self.screen.addstr(str(val or '_'), curses.color_pair(val))

    def __str__(self):
        return "\n".join(["".join(["% 3s" % v for v in row]) 
                         for row in self.board]).replace('0', '_')

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':

    game = Awesome11(size=4)
    game.play()

