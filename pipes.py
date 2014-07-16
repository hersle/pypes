#!/usr/bin/python

import curses

PIPE_STRAIGHT = (
    ((0, 1), (1, 1), (2, 1))
)
PIPE_TURN = (
    ((1, 0), (1, 1), (2, 1))
)
PIPES = (PIPE_STRAIGHT, PIPE_TURN)

def print_board(win, board, pipe, pipe_x, pipe_y):
    for y in range(0, len(board)):
        win.move(y, 0)
        for x in range(0, len(board[y])):
            if (pipe_x - x, pipe_y - y) in pipe:
                win.addstr("██")
            else:
                win.addstr("--")
    win.refresh()

def main(screen):
    curses.curs_set(False) # disable cursor

if __name__ == "__main__":
    curses.wrapper(main)
