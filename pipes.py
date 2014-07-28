# Cell identifiers
CELL_EMPTY = 0
CELL_PIPE_DRY = 1
CELL_PIPE_WET = 2
CELL_PIPE_ACTIVE = 3
CELL_START = 4
CELL_CHECKPOINT = 5
CELL_FINISH = 6

CELL_MAP = (
    ".", CELL_EMPTY,
    "p", CELL_PIPE_DRY,
    "s", CELL_START,
    "c", CELL_CHECKPOINT,
    "f", CELL_FINISH
)

# Pipes
PIPE_STRAIGHT = {
    "id" : 0,
    "char" : "I",
    "qty" : 0,
    "coords" : (
        ((0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (1, 2))
    )
}
PIPE_TURN = {
    "id" : 1,
    "char" : "L",
    "qty" : 0,
    "coords" : (
        ((1, 0), (1, 1), (2, 1)),
        ((2, 1), (1, 1), (1, 2)),
        ((0, 1), (1, 1), (1, 2)),
        ((1, 0), (1, 1), (0, 1))
    )
}
PIPE_T = {
    "id" : 2,
    "char" : "T",
    "qty" : 0,
    "coords" : (
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (1, 2)),
        ((1, 0), (0, 1), (1, 1), (1, 2))
    )
}
PIPE_X = {
    "id" : 3,
    "char" : "X",
    "qty" : 0,
    "coords" : (
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    )
}
PIPE_CLOSED = {
    "id" : 4,
    "char" : "i",
    "qty" : 0,
    "coords" : (
        ((1, 0), (1, 1)),
        ((2, 1), (1, 1)),
        ((1, 2), (1, 1)),
        ((0, 1), (1, 1)),
    )
}
PIPES = (PIPE_STRAIGHT, PIPE_TURN, PIPE_T, PIPE_X, PIPE_CLOSED)
