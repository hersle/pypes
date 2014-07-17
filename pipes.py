#!/usr/bin/python

import curses

BOARD_HEIGHT = 0 # set by load_level()
BOARD_WIDTH = 0 # set by load_level()
TILE_SIZE = 3 # every tile is actually a 3x3 grid

CELL_EMPTY = 0
CELL_PIPE = 1
CELL_PIPE_WATER = 2
CELL_START = 3
CELL_FINISH = 4

PIPE_CLOSED = ( # dead end
    ((1, 0), (1, 1)),
    ((2, 1), (1, 1)),
    ((1, 2), (1, 1)),
    ((0, 1), (1, 1)),
)
PIPE_STRAIGHT = (
    ((0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (1, 2))
)
PIPE_TURN = (
    ((1, 0), (1, 1), (2, 1)),
    ((2, 1), (1, 1), (1, 2)),
    ((0, 1), (1, 1), (1, 2)),
    ((1, 0), (1, 1), (0, 1))
)
PIPE_T = (
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (2, 1), (1, 2)),
    ((0, 1), (1, 1), (2, 1), (1, 2)),
    ((1, 0), (0, 1), (1, 1), (1, 2))
)
PIPE_X = (
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
)
PIPES = (PIPE_STRAIGHT, PIPE_TURN, PIPE_T, PIPE_X, PIPE_CLOSED)

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    for row in board[pipe_y : pipe_y + 3]:
        for cell in row[pipe_x : pipe_x + 3]:
            if cell != CELL_EMPTY:
                return # refuse placement if tile occupied
    for x, y in pipe[pipe_r]:
        board[pipe_y + y][pipe_x + x] = CELL_PIPE

def start_flow(board, start_x, start_y):
    log("starting water flow on (%d, %d)" % (start_x, start_y))
    board[start_y][start_x] = CELL_PIPE_WATER

def flow_water(board):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            if board[y][x] == CELL_PIPE_WATER:
                if board[y-1][x] not in (CELL_EMPTY, CELL_PIPE_WATER):
                    log("flowing from (%d, %d) to (%d, %d)" % (x, y, x, y-1))
                    board[y-1][x] = CELL_PIPE_WATER
                    return
                if board[y][x+1] not in (CELL_EMPTY, CELL_PIPE_WATER):
                    log("flowing from (%d, %d) to (%d, %d)" % (x, y, x+1, y))
                    board[y][x+1] = CELL_PIPE_WATER
                    return
                if board[y+1][x] not in (CELL_EMPTY, CELL_PIPE_WATER):
                    log("flowing from (%d, %d) to (%d, %d)" % (x, y, x, y+1))
                    board[y+1][x] = CELL_PIPE_WATER
                    return
                if board[y][x-1] not in (CELL_EMPTY, CELL_PIPE_WATER):
                    log("flowing from (%d, %d) to (%d, %d)" % (x, y, x-1, y))
                    board[y][x-1] = CELL_PIPE_WATER
                    return

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    for y in range(0, len(board)):
        win.move(1 + y, 1) # avoid border
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe[pipe_r]:
                win.addstr("██")
            elif board[y][x] == CELL_PIPE:
                win.addstr("██")
            elif board[y][x] == CELL_PIPE_WATER:
                win.addstr("██", curses.color_pair(CELL_PIPE_WATER))
            elif board[y][x] == CELL_START:
                win.addstr("██", curses.color_pair(CELL_START))
            elif board[y][x] == CELL_FINISH:
                win.addstr("██", curses.color_pair(CELL_FINISH))
            else:
                win.addstr("░░")
    win.refresh()

def load_board(level):
    global BOARD_HEIGHT, BOARD_WIDTH
    board = []
    start_x, start_y, finish_x, finish_y = None, None, None, None
    lines = open("levels/level%d" % level).read().splitlines()
    for y in range(0, len(lines)):
        BOARD_HEIGHT += 1
        row = []
        for x in range(0, len(lines[y])):
            BOARD_WIDTH = x + 1 if x + 1 > BOARD_WIDTH else BOARD_WIDTH
            char = lines[y][x]
            if char == ".":
                row.append(CELL_EMPTY)
            elif char == "S" or char == "s":
                if char == "S": # cap S denotes flow starting point
                    start_x, start_y = x, y
                row.append(CELL_START)
            elif char == "F" or char == "f": # cap F denotes flow ending point
                row.append(CELL_FINISH)
                if char == "F":
                    finish_x, finish_y = x, y
        board.append(row)
    return board, start_x, start_y, finish_x, finish_y

def init_colors():
    curses.init_pair(CELL_PIPE_WATER, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(CELL_START, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(CELL_FINISH, curses.COLOR_RED, curses.COLOR_BLACK)

def main(screen):
    curses.curs_set(False) # disable cursor
    init_colors()

    board, start_x, start_y, finish_x, finish_y = load_board(1)
    board_win = curses.newwin(BOARD_HEIGHT + 2, BOARD_WIDTH * 2 + 2)
    board_win.keypad(True) # interpret special key presses (e.g. arrow keys)
    board_win.border()

    log("Start=(%d, %d), finish=(%d, %d)" % (start_x, start_y, finish_x, finish_y))
    pipe = None
    x, y, r = 0, 0, 0
    while True:
        print_board(board_win, board, pipe, x, y, r)

        ch = board_win.getch() # get key press
        if chr(ch).isdigit() and int(chr(ch)) in range(1, len(PIPES) + 1):
            pipe = PIPES[int(chr(ch)) - 1] # key "1" should select pipe #0
            r = 0 # reset rotation
        elif ch == curses.KEY_UP:
            y = max(0, y - TILE_SIZE)
        elif ch == curses.KEY_RIGHT:
            x = min(BOARD_WIDTH - TILE_SIZE, x + TILE_SIZE)
        elif ch == curses.KEY_DOWN:
            y = min(BOARD_HEIGHT - TILE_SIZE, y + TILE_SIZE)
        elif ch == curses.KEY_LEFT:
            x = max(0, x - TILE_SIZE)
        elif ch == ord("r") and pipe:
            r = (r + 1) % len(pipe)
        elif ch == ord(" "):
            place_pipe(pipe, x, y, r, board)
        elif ch == ord("F"):
            start_flow(board, start_x, start_y)
        elif ch == ord("f"):
            flow_water(board)
        elif ch == ord("q"):
            return

def log(msg):
    open("log.txt", "a").write(msg + "\n")

if __name__ == "__main__":
    curses.wrapper(main)
