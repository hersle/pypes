import curses
import pipes
import menu
import levelio
import settings
from time import time
import log

TILE_SIZE = 3

def start_flow(level):
    for start_x, start_y in level["starts"]:
        level["board"][start_y][start_x] = pipes.CELL_PIPE_WATER
        level["flow"].append((start_x, start_y))
    level["flow_started"] = True

def flow_water(level):
    if not level["flow_started"]:
        start_flow(level)
    else:  # expand flow
        new_flow = []
        for x, y in level["flow"]:
            if (y in (0, len(level["board"]) - 1)
                or x in (0, len(level["board"][y]) - 1)):
                level["lost"] = True # game lost if flow is at board edge
                return
            offx = -1 + x % TILE_SIZE  # cells left/right of tile center
            offy = -1 + y % TILE_SIZE  # cells above/below tile center
            # Check cells   above    right   below   left
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                cell = level["board"][y + dy][x + dx]
                if cell != pipes.CELL_PIPE_WATER:  # do not wet a pipe twice
                    if cell != pipes.CELL_EMPTY:
                        level["board"][y + dy][x + dx] = pipes.CELL_PIPE_WATER
                        new_flow.append((x + dx, y + dy))
                    elif (dx, dy) == (offx, offy) and cell == pipes.CELL_EMPTY:
                        level["lost"] = True
                        return
        level["won"] = game_is_won(level, new_flow)
        level["flow"] = new_flow

def place_pipe(pipe, pipe_x, pipe_y, pipe_r, board):
    # Place pipe if tile's center cell is free
    if board[pipe_y + 1][pipe_x + 1] == pipes.CELL_EMPTY:
        for x, y in pipe["coords"][pipe_r]:
            board[pipe_y + y][pipe_x + x] = pipes.CELL_PIPE
        pipe["qty"] -= 1

def game_is_won(level, flow_endpoints):
    # TODO: fix game is won
    return set(level["finishes"]) == set(flow_endpoints)

def select_pipe(number, pipelist, current_pipe):
    index = number - 1
    if index in range(0, len(pipelist)) and pipelist[index]["qty"] > 0:
        return pipelist[index]
    return current_pipe  # return current pipe if selection denied

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    for y in range(0, len(board)):
        win.move(1 + y, 1)  # +1 to compensate for window border
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe["coords"][pipe_r]:
                win.addstr("██", curses.color_pair(pipes.CELL_PIPE_ACTIVE))
            elif board[y][x] == pipes.CELL_EMPTY:
                win.addstr("  ")
            else:
                win.addstr("██", curses.color_pair(board[y][x]))
    win.refresh()

def print_pipes(win, pipelist):
    # TODO: improve readability
    for p, pipe in enumerate(pipelist):
        base_x = 1 + p * 12
        win.addstr(1, base_x, "[%d]" % (p + 1))
        win.addstr(2, base_x, "%02dx" % pipe["qty"])
        base_x += 4
        for x, y in pipe["coords"][0]:
            string = "░░" if pipe["qty"] == 0 else "██"
            win.addstr(1 + y, base_x + x * 2, string, curses.color_pair(pipes.CELL_PIPE))
    win.refresh()

def print_misc(win):
    win.refresh()

def on_game_end(win, game_won, level_number):
    win.erase()
    menu.post_game_menu(win, game_won, level_number)

def init_windows(screen, board_width, board_height):
    screen_height, screen_width = screen.getmaxyx()

    # Window for displaying available pipes
    left, top = 0, 0
    width, height = screen_width, 4 + 2
    pipe_win = curses.newwin(height, width, top, left)
    pipe_win.border()

    # Window for displaying game board
    top = pipe_win.getmaxyx()[0]  # below pipe win
    width, height = board_width * 2 + 2, board_height + 2
    board_win = curses.newwin(height, width, top, left)
    board_win.keypad(True)  # interpret special key presses (e.g. arrow keys)
    board_win.border()

    # Window for displaying misc. stats and info
    left = board_win.getmaxyx()[1]  # right of board_win
    width = screen_width - left  # cover rest of screen width
    misc_win = curses.newwin(height, width, top, left)
    misc_win.border()
    misc_win.refresh()

    return pipe_win, board_win, misc_win

def init_colors():
    curses.init_pair(pipes.CELL_PIPE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_PIPE_WATER, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_PIPE_ACTIVE, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_START, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_CHECKPOINT, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_FINISH, curses.COLOR_RED, curses.COLOR_BLACK)

def play(screen, level_number):
    init_colors()

    # Load config/settings
    config = {}
    exec(open("settings.py").read(), config)

    level = levelio.load_level(level_number)
    board_width = len(level["board"][0])  # assume board is rectangular
    board_height = len(level["board"])

    pipe_win, board_win, misc_win = init_windows(screen, board_width, board_height)

    pipe = next(p for p in level["pipes"] if p["qty"] > 0)  # current pipe
    x = 0  # blocks from board's left
    y = 0  # blocks from board's top
    r = 0  # steps rotated
    flow_speed = 0.5  # seconds till flow flows
    flow_start_delay = 2  # seconds till flow starts
    flow_time = time() + flow_start_delay  # timestamp at which flow flows
    while True:
        board_win.timeout(int((flow_time - time()) * 1000))  # s to ms

        print_board(board_win, level["board"], pipe, x, y, r)
        print_pipes(pipe_win, level["pipes"])
        #print_misc(misc_win)

        ch = board_win.getch() # get key press
        # Order of operations below does matter
        if ch != -1 and chr(ch).isdigit():  # select new pipe
            pipe = select_pipe(int(chr(ch)), level["pipes"], pipe)
            r = 0  # reset rotation
        elif ch in config["place_pipe"] and pipe:
            place_pipe(pipe, x, y, r, level["board"])
            if pipe["qty"] == 0: pipe = None  # deselect if empty
        elif ch in config["move_up"]:
            y = max(0, y - TILE_SIZE)
        elif ch in config["move_right"]:
            x = min(board_width - TILE_SIZE, x + TILE_SIZE)
        elif ch in config["move_down"]:
            y = min(board_height - TILE_SIZE, y + TILE_SIZE)
        elif ch in config["move_left"]:
            x = max(0, x - TILE_SIZE)
        elif ch in config["rotate"] and pipe:
            r = (r + 1) % len(pipe["coords"])
        elif ch in config["increase_flow_speed"]:
            flow_speed /= 10
        elif ch == ord("q"):
            return
        elif ch == -1:  # keypress timeout
            flow_water(level)
            flow_time = time() + flow_speed  # update flow time
        if level["won"] or level["lost"]:
            on_game_end(board_win, level["won"], level_number)
            return
