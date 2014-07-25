# Cell identifiers
CELL_EMPTY = 0
CELL_PIPE = 1
CELL_PIPE_WATER = 2
CELL_PIPE_ACTIVE = 3
CELL_START = 4
CELL_CHECKPOINT = 5
CELL_FINISH = 6

# Pipe IDs
PIPE_STRAIGHT = 0
PIPE_TURN = 1
PIPE_T = 2
PIPE_X = 3
PIPE_CLOSED = 4

# Lists with (x, y) coordinates for each pipe's rotated variations in a 3x3 grid
# All coordinates are relative to grid's top-left corner
PIPES = (
    (  # straight
        ((0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (1, 2))
    ),
    (  # turn
        ((1, 0), (1, 1), (2, 1)),
        ((2, 1), (1, 1), (1, 2)),
        ((0, 1), (1, 1), (1, 2)),
        ((1, 0), (1, 1), (0, 1))
    ),
    (  # T
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (1, 2)),
        ((1, 0), (0, 1), (1, 1), (1, 2))
    ),
    (  # X
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ),
    (  # closed
        ((1, 0), (1, 1)),
        ((2, 1), (1, 1)),
        ((1, 2), (1, 1)),
        ((0, 1), (1, 1)),
    )
)

PIPE_MAP = (
    "straight", PIPE_STRAIGHT,
    "turn", PIPE_TURN,
    "t", PIPE_T,
    "x", PIPE_X,
    "c", PIPE_CLOSED
)

# Strings on even indexes (0, 2, 4, etc.)
# Integers on odd indexes (1, 3, 5, etc.)
CELL_MAP = (
    ".", CELL_EMPTY,
    "p", CELL_PIPE,
    "s", CELL_START,
    "c", CELL_CHECKPOINT,
    "f", CELL_FINISH
)
