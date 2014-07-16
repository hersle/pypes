#!/usr/bin/python

import curses

PIPE_STRAIGHT = (
    ((0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (1, 2))
)
PIPE_TURN = (
    ((1, 0), (1, 1), (2, 1))
)
PIPES = (PIPE_STRAIGHT, PIPE_TURN)

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    for x, y in pipe[pipe_r]:
        log("placing pipe on (%d, %d)" % (pipe_x + x, pipe_y + y))
        board[pipe_y + y][pipe_x + x] = True
    return board

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    if pipe: log("Pipe: %s" % str(pipe[pipe_r]))
    for y in range(0, len(board)):
        win.move(1 + y, 1)
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe[pipe_r]:
                win.addstr("██", curses.color_pair(2))
            elif board[y][x]:
                win.addstr("██", curses.color_pair(1))
            else:
                win.addstr("  ")
    win.refresh()

def init_colors():
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

def main(screen):
    curses.curs_set(False) # disable cursor
    screen.keypad(True) # interpret special key presses (e.g. arrow keys)
    screen.border()
    init_colors()

    board = [[False for x in range(0, 12)] for y in range(0, 18)]
    pipe = None
    x, y, r = 0, 0, 0
    while True:
        print_board(screen, board, pipe, x, y, r)
        ch = screen.getch() # get key press
        if chr(ch).isdigit() and int(chr(ch)) in range(1, len(PIPES) + 1):
            log("selecting pipe %d" % (int(chr(ch)) - 1))
            pipe = PIPES[int(chr(ch)) - 1] # key "1" should select pipe #0
        elif ch == curses.KEY_UP:
            y -= 3
        elif ch == curses.KEY_RIGHT:
            x += 3
        elif ch == curses.KEY_DOWN:
            y += 3
        elif ch == curses.KEY_LEFT:
            x -= 3
        elif ch == ord("r"):
            r = (r + 1) % len(pipe)
        elif ch == ord(" "):
            board = place_pipe(pipe, x, y, r, board)
            pipe = None

def log(msg):
    open("log.txt", "a").write(msg + "\n")

if __name__ == "__main__":
    curses.wrapper(main)
