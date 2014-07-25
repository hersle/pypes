#!/usr/bin/python

import curses
import pipes
import menu
import levelio
from time import time
import log

TILE_SIZE = 3

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    # Place the pipe if the tile's center cell is free.
    if board[pipe_y + 1][pipe_x + 1] == pipes.CELL_EMPTY:
        for x, y in pipe[pipe_r]:
            board[pipe_y + y][pipe_x + x] = pipes.CELL_PIPE

def flow_water(board, flow_endpoints):
    new_flow_endpoints = []
    for x, y in flow_endpoints:
        if board[y][x] == pipes.CELL_EMPTY:
            log.log("game lost")
        offx = -1 + x % 3
        offy = -1 + y % 3
        log.log("offx=%d, offy=%d" % (offx, offy))

        # Fill cell
        board[y][x] = pipes.CELL_PIPE_WATER

        # Flow water into any adjacent pipes
        moved_endpoint = False
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)): 
            if (dx, dy) == (offx, offy):
                log.log("(%d, %d) is in same direction" % (dx + x, dy + y))
            #if board[y + dy][x + dx] not in (pipes.CELL_EMPTY, pipes.CELL_PIPE_WATER):
            if board[y + dy][x + dx] != pipes.CELL_PIPE_WATER and (board[y+dy][x+dx] != pipes.CELL_EMPTY or (dx, dy) == (offx, offy)):
                new_flow_endpoints.append((x + dx, y + dy))
                moved_endpoint = True
        if not moved_endpoint: # Add original endpoint if it did not change
            new_flow_endpoints.append((x, y))
    return new_flow_endpoints

def game_is_lost(board, flow_endpoints):
    for x, y in flow_endpoints:
        if board[y][x] == pipes.CELL_EMPTY:
            return True
    return False

def game_is_won(board, flow_endpoints, finish_x, finish_y):
    # TODO: check whole board
    if board[finish_y][finish_x] == pipes.CELL_PIPE_WATER:
        return True
    return False

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    for y in range(0, len(board)):
        win.move(1 + y, 1)  # +1 to compensate for border
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe[pipe_r]:
                win.addstr("  ", curses.color_pair(pipes.CELL_PIPE_ACTIVE))
            elif board[y][x] == pipes.CELL_EMPTY:
                win.addstr("  ")
            else:
                win.addstr("  ", curses.color_pair(board[y][x]))
    win.refresh()

def on_game_end(win, game_won):
    win.erase()
    menu.post_game_menu(win, game_won)

def init_colors():
    curses.init_pair(pipes.CELL_PIPE, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(pipes.CELL_PIPE_WATER, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(pipes.CELL_PIPE_ACTIVE, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(pipes.CELL_START, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(pipes.CELL_FINISH, curses.COLOR_BLACK, curses.COLOR_RED)

def play():
    init_colors()

    board, start_x, start_y, finish_x, finish_y = levelio.load_board(1)
    board_width = len(board[0])  # assume board is rectangular
    board_height = len(board)
    flow_endpoints = [(start_x, start_y)]

    board_win = curses.newwin(board_height + 2, board_width * 2 + 2)
    board_win.keypad(True)  # interpret special key presses (e.g. arrow keys)
    board_win.border()

    pipe = None  # currently selected pipe
    x = 0  # blocks from board's left
    y = 0  # blocks from board's top
    r = 0  # steps rotated
    flow_speed = 1  # seconds till flow flows
    flow_start_delay = 2  # seconds till flow starts
    flow_time = time() + flow_start_delay # timestamp at which flow flows
    while True:
        board_win.timeout(int((flow_time - time()) * 1000))  # s to ms
        print_board(board_win, board, pipe, x, y, r)
        ch = board_win.getch() # get key press

        # TODO: change order of operations (give player opportunity to place pipe before overflow)
        # Check whether game is won or lost after getch() timeouts
        game_lost = game_is_lost(board, flow_endpoints)
        game_won = game_is_won(board, flow_endpoints, finish_x, finish_y)
        if game_lost or game_won:  # game over
            on_game_end(board_win, game_won)
            return
        elif ch == -1:  # keypress timeout
            flow_endpoints = flow_water(board, flow_endpoints)
            flow_time = time() + flow_speed
        elif chr(ch).isdigit() and int(chr(ch)) in range(1, len(pipes.PIPES) + 1):
            number = int(chr(ch)) - 1  # key n should select pipe at index n - 1
            pipe = pipes.PIPES[number]
            r = 0  # reset rotation
        elif ch == curses.KEY_UP:
            y = max(0, y - TILE_SIZE)
        elif ch == curses.KEY_RIGHT:
            x = min(board_width - TILE_SIZE, x + TILE_SIZE)
        elif ch == curses.KEY_DOWN:
            y = min(board_height - TILE_SIZE, y + TILE_SIZE)
        elif ch == curses.KEY_LEFT:
            x = max(0, x - TILE_SIZE)
        elif ch == ord("r") and pipe:
            r = (r + 1) % len(pipe)
        elif ch == ord(" "):
            place_pipe(pipe, x, y, r, board)
        elif ch == ord("f"):
            flow_speed /= 2  # double flow speed
        elif ch == ord("q"):
            on_game_end(board_win, False)
            return

if __name__ == "__main__":
    exit()
