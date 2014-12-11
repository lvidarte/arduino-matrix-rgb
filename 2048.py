#!/bin/python

import random

class Arduino2048:

    def __init__(self):
        self.start()

    def start(self):
        self.reset()

    def reset(self):
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    def move(self):
        self.added = False
        self.move_left()
        if self.added == False:
            self.add()

    def move_left(self):
        for i, _ in enumerate(self.board):
            self.board[i] = self.row_to_left(self.board[i])

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
                self.added = True
        return row

    def add(self):
        empty = []
        for x, row in enumerate(self.board):
            for y, val in enumerate(row):
                if val == 0:
                    empty.append((x, y))
        if len(empty):
            x, y = random.choice(empty)
            self.board[x][y] = 1


if __name__ == '__main__':

    game = Arduino2048()

