# Cell identifiers
CELL_EMPTY = 0
CELL_PIPE_DRY = 1
CELL_PIPE_WET = 2
CELL_PIPE_ACTIVE = 3
CELL_START = 4
CELL_CHECKPOINT = 5
CELL_FINISH = 6
CELLS_FILLABLE = (CELL_PIPE_DRY, CELL_START, CELL_CHECKPOINT, CELL_FINISH)

# Characters associated with each cell. Used when reading levels from files.
CELL_MAP = {
    ".": CELL_EMPTY,
    "p": CELL_PIPE_DRY,
    "s": CELL_START,
    "c": CELL_CHECKPOINT,
    "f": CELL_FINISH
}

# Pipes
class Pipe:
    def __init__(self, _id, char, coordinates):
        self._id = _id
        self.char = char
        self.coordinates = coordinates

    def place(self, board, board_x, board_y, r):
        if board[board_y + 1][board_x + 1] == CELL_EMPTY:
            for x, y in self.coordinates[r]:
                board[board_y + y][board_x + x] = CELL_PIPE_DRY
            self.quantity -= 1

PIPE_STRAIGHT = Pipe(0, "I", (
    ((0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (1, 2))
))
PIPE_TURN = Pipe(1, "L", (
    ((1, 0), (1, 1), (2, 1)),
    ((2, 1), (1, 1), (1, 2)),
    ((0, 1), (1, 1), (1, 2)),
    ((1, 0), (1, 1), (0, 1))
))
PIPE_T = Pipe(2, "T", (
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (1, 1), (2, 1), (1, 2)),
    ((0, 1), (1, 1), (2, 1), (1, 2)),
    ((1, 0), (0, 1), (1, 1), (1, 2))
))
PIPE_X = Pipe(3, "X", (
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
))
PIPE_CLOSED = Pipe(4, "i", (
    ((1, 0), (1, 1)),
    ((2, 1), (1, 1)),
    ((1, 2), (1, 1)),
    ((0, 1), (1, 1)),
))
pipe_list = (PIPE_STRAIGHT, PIPE_TURN, PIPE_T, PIPE_X, PIPE_CLOSED)
