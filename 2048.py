#!/bin/python

import random
import time


class Getch:

    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class Arduino2048:

    def __init__(self, size=4):
        self.size = 4
        self.start()

    def start(self):
        self.reset()
        self.add()
        self.add()
        commands = {'h': 'left', 'j': 'bottom', 'k': 'top', 'l': 'right'}
        getch = Getch()
        while True:
            print '-' * 10
            print self
            c = getch()
            self.move(commands[c])

    def reset(self):
        self.board = [[0 for i in range(self.size)]
                      for j in range(self.size)]

    def move(self, direction):
        moves = {
            'left'  : self.move_left,
            'right' : self.move_right,
            'top'   : self.move_top,
            'bottom': self.move_bottom,
        }
        board = moves[direction]()
        if board != self.board:
            self.board = board
            print '-' * 10
            print self
            time.sleep(.25)
            self.add()
            print '-' * 10
            print self

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
        for i in range(3):
            for _ in range(3 - i):
                if row[i] == 0:
                    row.pop(i)
                    row.append(0)
                else:
                    break
            for _ in range(2 - i):
                if row[i + 1] == 0:
                    row.pop(i + 1)
                    row.append(0)
                else:
                    break
            if row[i] != 0 and row[i] == row[i + 1]:
                row.pop(i)
                row[i] *= 2
                row.append(0)
        return row

    def add(self):
        empty = []
        for x, row in enumerate(self.board):
            for y, val in enumerate(row):
                if val == 0:
                    empty.append((x, y))
        if len(empty):
            x, y = random.choice(empty)
            self.board[x][y] = 2

    def __str__(self):
        return "\n".join(["".join(["% 5s" % v for v in row]) 
                         for row in self.board]).replace('0', '_')

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':

    game = Arduino2048()

