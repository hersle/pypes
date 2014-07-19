#!/usr/bin/python

import curses
import menu
from time import time
import log

BOARD_HEIGHT = 0 # set by load_level()
BOARD_WIDTH = 0 # set by load_level()
TILE_SIZE = 3 # every tile is actually a 3x3 grid

# Cell identifiers
CELL_EMPTY = 0
CELL_PIPE = 1
CELL_PIPE_WATER = 2
CELL_PIPE_ACTIVE = 3
CELL_START = 4
CELL_FINISH = 5

# Lists with (x, y) coordinates for each pipe's rotated variations in a 3x3 grid
# All coordinates are relative to grid's top-left corner
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
PIPE_CLOSED = (
    ((1, 0), (1, 1)),
    ((2, 1), (1, 1)),
    ((1, 2), (1, 1)),
    ((0, 1), (1, 1)),
)
PIPES = (PIPE_STRAIGHT, PIPE_TURN, PIPE_T, PIPE_X, PIPE_CLOSED)

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    # Add the pipe to the board if this tile is free.
    if board[pipe_y + 1][pipe_x + 1] == CELL_EMPTY:
        for x, y in pipe[pipe_r]:
            board[pipe_y + y][pipe_x + x] = CELL_PIPE

def flow_water(board, flow_endpoints):
    # TODO: review
    new_flow_endpoints = []
    for x, y in flow_endpoints:
        if board[y][x] == CELL_EMPTY:
            log.log("game lost")
        offx = -1 + x % 3
        offy = -1 + y % 3
        log.log("offx=%d, offy=%d" % (offx, offy))

        # Fill cell
        board[y][x] = CELL_PIPE_WATER

        # Flow water into any adjacent pipes
        moved_endpoint = False
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)): 
            if (dx, dy) == (offx, offy):
                log.log("(%d, %d) is in same direction" % (dx + x, dy + y))
            #if board[y + dy][x + dx] not in (CELL_EMPTY, CELL_PIPE_WATER):
            if board[y + dy][x + dx] != CELL_PIPE_WATER and (board[y+dy][x+dx] != CELL_EMPTY or (dx, dy) == (offx, offy)):
                new_flow_endpoints.append((x + dx, y + dy))
                moved_endpoint = True
        if not moved_endpoint: # Add original endpoint if it did not change
            new_flow_endpoints.append((x, y))
    return new_flow_endpoints

def game_is_lost(board, flow_endpoints):
    # TODO: review
    for x, y in flow_endpoints:
        if board[y][x] == CELL_EMPTY: return True
    return False

def game_is_won(board, flow_endpoints, finish_x, finish_y):
    # TODO: review
    if board[finish_y][finish_x] == CELL_PIPE_WATER:
        return True
    return False
    for x, y in flow_endpoints:
        if board[y][x] == CELL_FINISH: exit()
    return False

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    for y in range(0, len(board)):
        win.move(1 + y, 1)  # +1 to compensate for border
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe[pipe_r]:
                win.addstr("  ", curses.color_pair(CELL_PIPE_ACTIVE))
            elif board[y][x] == CELL_EMPTY:
                win.addstr("  ")
            else:
                win.addstr("  ", curses.color_pair(board[y][x]))
    win.refresh()

def load_board(level):
    global BOARD_HEIGHT, BOARD_WIDTH # modify global variables, not local ones TODO: make local?
    BOARD_HEIGHT, BOARD_WIDTH = 0, 0
    board = []
    start_x, start_y, finish_x, finish_y = None, None, None, None # TODO: make global for consistency?
    lines = open("levels/level%d" % level).read().splitlines()
    for y in range(0, len(lines)):
        BOARD_HEIGHT += 1 # board height increases by 1 for each line
        row = []
        for x in range(0, len(lines[y])):
            if x + 1 > BOARD_WIDTH: # increase board width if exceeded
                BOARD_WIDTH = x + 1
            char = lines[y][x]
            if char == ".":
                row.append(CELL_EMPTY)
            elif char == "S" or char == "s":
                row.append(CELL_START)
                if char == "S": # cap S denotes flow starting point
                    start_x, start_y = x, y
            elif char == "F" or char == "f": # cap F denotes flow ending point
                row.append(CELL_FINISH)
                if char == "F":
                    finish_x, finish_y = x, y
        board.append(row)
    return board, start_x, start_y, finish_x, finish_y

def on_game_end(win):
    menu.post_game_menu(win, True)

def init_colors():
    curses.init_pair(CELL_PIPE, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(CELL_PIPE_WATER, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(CELL_PIPE_ACTIVE, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(CELL_START, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(CELL_FINISH, curses.COLOR_BLACK, curses.COLOR_RED)

def play():
    init_colors()

    board, start_x, start_y, finish_x, finish_y = load_board(1)
    flow_endpoints = [(start_x, start_y)]
    log.log("creating board win (%d, %d)" % (BOARD_HEIGHT + 2, BOARD_WIDTH * 2 + 2))
    board_win = curses.newwin(BOARD_HEIGHT + 2, BOARD_WIDTH * 2 + 2, 0, 0)
    board_win.keypad(True) # interpret special key presses (e.g. arrow keys)
    #board_win.nodelay(True) # TODO: lower CPU usage
    board_win.border()

    pipe = None # currently selected pipe
    x, y, r = 0, 0, 0 # position from right, position from left, steps rotated
    flow_speed = 1 # seconds before flow flows TODO: make var name more meaningful?
    start_delay = 2 # seconds before flow starts
    flow_time = time() + start_delay # timestamp at which the flow will flows
    while True:
        board_win.timeout(int((flow_time - time()) * 1000))

        print_board(board_win, board, pipe, x, y, r)

        ch = board_win.getch() # get key press

        # Check whether game is won or lost after getch() timeouts
        if (game_is_lost(board, flow_endpoints) 
            or game_is_won(board, flow_endpoints, finish_x, finish_y)):
            board_win.erase()
            on_game_end(board_win)
            return
        # Start checking input
        elif ch == -1: # flow
            log.log("%s" % game_is_lost(board, flow_endpoints))
            flow_endpoints = flow_water(board, flow_endpoints)
            flow_time = time() + flow_speed
        elif chr(ch).isdigit() and int(chr(ch)) in range(1, len(PIPES) + 1):
            number = int(chr(ch)) - 1  # key "1" should select pipe #0
            pipe = PIPES[number]
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
        elif ch == ord("f"): # TODO: toggle faster/slower flow speed
            flow_speed /= 5
        elif ch == ord("q"):
            board_win.erase()
            board_win.refresh()
            return

if __name__ == "__main__":
    exit()
