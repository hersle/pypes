import curses
import pipes
import menu
from time import time
import log


class Level:

    TILE_SIZE = 3

    def __init__(self, level_number):
        self.load_level(level_number)
        self.lost = False
        self.won = False

    def load_level(self, level_number):
        level_file = open("levels/" + str(level_number))
        lines = level_file.read().splitlines()
        level_file.close()
        lines_pipes = [line for line in lines if "=" in line]
        lines_board = [line for line in lines if "=" not in line]

        self.load_pipes(lines_pipes)
        starts, checkpoints, finishes = self.load_board(lines_board)
        self.flow = Flow(starts, checkpoints, finishes)

    def load_pipes(self, lines_pipes):
        pipe_quantities = dict(line.split("=") for line in lines_pipes)
        for pipe in pipes.pipe_list:
            # Set pipe quantity as specified or 0 if unspecified
            pipe.quantity = int(pipe_quantities.get(pipe.char, 0))
        self.pipes = pipes.pipe_list

    def load_board(self, lines_board):
        self.board = []
        starts = []
        checkpoints = []
        finishes = []

        for y, line in enumerate(lines_board):
            row = []
            for x, char in enumerate(line):
                cell = pipes.CELL_MAP[char]
                row.append(cell)
                if cell == pipes.CELL_START:
                    starts.append((x, y))
                elif cell == pipes.CELL_CHECKPOINT:
                    checkpoints.append((x, y))
                elif cell == pipes.CELL_FINISH:
                    finishes.append((x, y))
            self.board.append(row)

        self.height = len(self.board)
        self.width = max(len(row) for row in self.board)
        return starts, checkpoints, finishes

    def select_pipe(self, number, current_pipe):
        index = number - 1  # pressing 1 should select pipe at index 0, etc
        if index in range(0, len(self.pipes)):
            return self.pipes[index]
        return current_pipe

    def advance_flow(self):
        return_code = self.flow.advance(self.board)
        self.lost = return_code == self.flow.RETURN_CODE_GAME_LOST
        self.won = return_code == self.flow.RETURN_CODE_GAME_WON

class Flow:

    # Returned by advance() to inform its caller if the game is lost or won
    RETURN_CODE_GAME_LOST = 0
    RETURN_CODE_GAME_WON = 1

    def __init__(self, starts, checkpoints, finishes):
        self.starts = starts
        self.checkpoints = checkpoints
        self.finishes = finishes
        self.started = False

    def start(self, board):
        self.endpoints = []
        for start_x, start_y in self.starts:
            board[start_y][start_x] = pipes.CELL_PIPE_WET
            self.endpoints.append((start_x, start_y))
        self.started = True
        self.targets_wet = 0

    def advance(self, board):
        if not self.started:
            self.start(board)
        else:
            new_endpoints = []
            for x, y in self.endpoints:
                # Game over if endpoint is at board edge
                if y in (0, len(board) - 1) or x in (0, len(board[y]) - 1):
                    return self.RETURN_CODE_GAME_LOST
                offx, offy = -1 + x % 3, -1 + y % 3  # offset from tile center
                for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    cell = board[y + dy][x + dx]
                    if cell != pipes.CELL_PIPE_WET:  # do not wet a cell twice
                        if cell != pipes.CELL_EMPTY:  # i.e. is a pipe
                            board[y + dy][x + dx] = pipes.CELL_PIPE_WET
                            if not self.is_dead_end(board, x + dx, y + dy):
                                new_endpoints.append((x + dx, y + dy))
                        elif (dx, dy) == (offx, offy):
                            # Lost if attempting to fill a cell in the same 
                            # direction from the tile center as the direction
                            # this endpoint itself is from tile center.
                            return self.RETURN_CODE_GAME_LOST
            self.endpoints = new_endpoints
            log.log("endpoints: %s" % str(self.endpoints))

            # Check whether game is lost or won if the flow has stopped
            if len(self.endpoints) == 0:
                # Won if all checkpoints and finishes are wet, otherwise lost
                for x, y in self.checkpoints + self.finishes:
                    if board[y][x] != pipes.CELL_PIPE_WET:
                        return self.RETURN_CODE_GAME_LOST
                return self.RETURN_CODE_GAME_WON

    def is_dead_end(self, board, x, y):
        offx = -1 + x % 3
        offy = -1 + y % 3
        if offx == 0 and offy == 0:
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if board[y + dy][x + dx] in pipes.CELLS_FILLABLE:
                    return False
            return True
        return False

# End of classes

def print_board(win, board, pipe, pipe_x, pipe_y, pipe_r):
    for y in range(0, len(board)):
        win.move(1 + y, 1)  # +1 to compensate for window border
        for x in range(0, len(board[y])):
            if pipe and (x - pipe_x, y - pipe_y) in pipe.coordinates[pipe_r]:
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
        win.addstr(2, base_x, "%02dx" % pipe.quantity)
        base_x += 4
        for x, y in pipe.coordinates[0]:
            string = "░░" if pipe.quantity == 0 else "██"
            win.addstr(1 + y, base_x + x * 2, string, curses.color_pair(pipes.CELL_PIPE_DRY))
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
    curses.init_pair(pipes.CELL_PIPE_DRY, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_PIPE_WET, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_PIPE_ACTIVE, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_START, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_CHECKPOINT, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(pipes.CELL_FINISH, curses.COLOR_RED, curses.COLOR_BLACK)

def play(screen, level_number):
    init_colors()

    # Load config/settings (controls)
    controls = {}
    exec(open("controls.py").read(), controls)

    level = Level(level_number)

    pipe_win, board_win, misc_win = init_windows(screen, level.width, level.height)

    # Select first pipe with a quantity above 0
    pipe = next(pipe for pipe in level.pipes if pipe.quantity > 0)  # current pipe
    x = 0  # blocks from board's left
    y = 0  # blocks from board's top
    r = 0  # steps rotated
    flow_speed = 0.5  # seconds between each time flow advances
    flow_start_delay = 2  # seconds till flow starts
    flow_time = time() + flow_start_delay  # timestamp at which flow flows
    while True:
        # Timeout when flow should advance
        board_win.timeout(int((flow_time - time()) * 1000))  # s to ms

        print_board(board_win, level.board, pipe, x, y, r)
        print_pipes(pipe_win, level.pipes)
        #print_misc(misc_win)

        ch = board_win.getch() # get key press
        # Order of operations below does matter
        if ch != -1 and chr(ch).isdigit():  # select new pipe
            pipe = level.select_pipe(int(chr(ch)), pipe)
            r = 0  # reset rotation
        elif ch in controls["place_pipe"] and pipe:
            pipe.place(x, y, r, level.board)
            if pipe.quantity == 0:
                pipe = None  # deselect pipe if depleted
        elif ch in controls["move_up"]:
            y = max(0, y - level.TILE_SIZE)
        elif ch in controls["move_right"]:
            x = min(level.width - level.TILE_SIZE, x + level.TILE_SIZE)
        elif ch in controls["move_down"]:
            y = min(level.height - level.TILE_SIZE, y + level.TILE_SIZE)
        elif ch in controls["move_left"]:
            x = max(0, x - level.TILE_SIZE)
        elif ch in controls["rotate"] and pipe:
            r = (r + 1) % len(pipe.coordinates)
        elif ch in controls["increase_flow_speed"]:
            flow_speed /= 10
        elif ch == ord("q"):
            return
        elif ch == -1: #ord("f"):
            level.advance_flow()
            flow_time = time() + flow_speed  # update flow time

        if level.won or level.lost:
            on_game_end(board_win, level.won, level_number)
            return
