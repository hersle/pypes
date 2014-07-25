import curses
import pipes
import menu
import levelio
import settings
from time import time
import log

TILE_SIZE = 3

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    # Place pipe if tile's center cell is free
    if pipe and board[pipe_y + 1][pipe_x + 1] == pipes.CELL_EMPTY:
        for x, y in pipe[pipe_r]:
            board[pipe_y + y][pipe_x + x] = pipes.CELL_PIPE

def flow_water(board, flow_endpoints):
    # TODO: write good documentation
    # Wet each endpoint and its adjacent cells that (1) are dry AND (2a) 
    # contains a pipe OR (2b) is in the same direction from the endpoint 
    # as the endpoint is from the tile center.
    new_flow_endpoints = []
    for x, y in flow_endpoints:
        board[y][x] = pipes.CELL_PIPE_WATER
        offx = -1 + x % TILE_SIZE  # cells left/right of tile center
        offy = -1 + y % TILE_SIZE  # cells above/below tile center

        # Loop through adjacent cells
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if (board[y + dy][x + dx] != pipes.CELL_PIPE_WATER  # (1)
                and (board[y + dy][x + dx] != pipes.CELL_EMPTY  # (2a)
                or (dx, dy) == (offx, offy))):  # (2b)
                new_flow_endpoints.append((x + dx, y + dy))
    return new_flow_endpoints

def game_is_lost(board, flow_endpoints):
    for x, y in flow_endpoints:
        if board[y][x] == pipes.CELL_EMPTY: return True
    return False

def game_is_won(flow_endpoints):
    return len(flow_endpoints) == 0

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

def print_pipes(win, pipelist):
    for p, pipe in enumerate(pipelist):
        base_x = 1 + p * 12
        win.addstr(1, base_x, "[%d]" % (p + 1))
        win.addstr(2, base_x, "99x")
        base_x += 4
        for x, y in pipe[0]:
            win.addstr(1 + y, base_x + x * 2, "  ", curses.color_pair(pipes.CELL_PIPE))
    win.refresh()

def print_stat(win, stats):
    win.addstr(1, 1, "Speed: %dx" % stats["speed_multiplier"])
    win.refresh()

def on_game_end(win, game_won):
    win.erase()
    menu.post_game_menu(win, game_won)

def init_windows(screen, board_width, board_height):
    screen_height, screen_width = screen.getmaxyx()
    left, top = 0, 0

    pipe_win = curses.newwin(4 + 2, screen_width, top, left)
    pipe_win.border()
    pipe_win.refresh()

    top += pipe_win.getmaxyx()[0]
    board_win = curses.newwin(board_height + 2, board_width * 2 + 2, top, left)
    board_win.keypad(True)  # interpret special key presses (e.g. arrow keys)
    board_win.border()

    board_win_height, board_win_width = board_win.getmaxyx()
    stat_win = curses.newwin(board_win_height, screen_width - board_win_width, top, board_win_width)
    stat_win.border()
    stat_win.refresh()

    return pipe_win, board_win, stat_win

def init_colors():
    curses.init_pair(pipes.CELL_PIPE, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(pipes.CELL_PIPE_WATER, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(pipes.CELL_PIPE_ACTIVE, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(pipes.CELL_START, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(pipes.CELL_FINISH, curses.COLOR_BLACK, curses.COLOR_RED)

def play(screen):
    init_colors()

    # Load config/settings
    config = {}
    exec(open("settings.py").read(), config)

    stats = {
        "speed_multiplier" : 1
    }

    level = levelio.load_board(1)
    board = level["board"]
    start_x, start_y = level["start_x"], level["start_y"]
    finish_x, finish_y = level["finish_x"], level["finish_y"]
    board_width = len(board[0])  # assume board is rectangular
    board_height = len(board)
    flow_endpoints = [(start_x, start_y)]

    pipe_win, board_win, stat_win = init_windows(screen, board_width, board_height)

    pipe = None  # currently selected pipe
    x = 0  # blocks from board's left
    y = 0  # blocks from board's top
    r = 0  # steps rotated
    flow_speed = 0.5  # seconds till flow flows TODO: more meaningful name?
    flow_start_delay = 2  # seconds till flow starts
    flow_time = time() + flow_start_delay # timestamp at which flow flows
    while True:
        game_lost = game_is_lost(board, flow_endpoints)
        game_won = game_is_won(flow_endpoints)
        board_win.timeout(int((flow_time - time()) * 1000))  # s to ms

        print_board(board_win, board, pipe, x, y, r)
        print_pipes(pipe_win, pipes.PIPES)
        print_stat(stat_win, stats)

        ch = board_win.getch() # get key press

        # Order of operations below matter
        if ch != -1 and chr(ch).isdigit():  # select new pipe
            pipe = pipes.PIPES[int(chr(ch)) - 1]
            r = 0  # reset rotation
        elif ch in config["place_pipe"]:
            place_pipe(pipe, x, y, r, board)
        elif ch in config["move_up"]:
            y = max(0, y - TILE_SIZE)
        elif ch in config["move_right"]:
            x = min(board_width - TILE_SIZE, x + TILE_SIZE)
        elif ch in config["move_down"]:
            y = min(board_height - TILE_SIZE, y + TILE_SIZE)
        elif ch in config["move_left"]:
            x = max(0, x - TILE_SIZE)
        elif ch in config["rotate"] and pipe:
            r = (r + 1) % len(pipe)
        elif ch in config["increase_flow_speed"]:
            flow_speed /= 10
            stats["speed_multiplier"] *= 10
        elif ch == ord("q") or game_lost or game_won:
            on_game_end(board_win, False)
            return
        elif game_lost or game_won:
            on_game_end(board_win, game_won)
            return
        elif ch == -1:  # keypress timeout
            flow_endpoints = flow_water(board, flow_endpoints)
            flow_time = time() + flow_speed  # update flow time
