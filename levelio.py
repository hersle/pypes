import pipes

def load_board(level):
    # Create a new 2D board array by loading a board from a file.
    board = []
    start_x, start_y, finish_x, finish_y = None, None, None, None
    lines = open("levels/level%d" % level).read().splitlines()
    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line): 
            if char == ".":
                row.append(pipes.CELL_EMPTY)
            elif char == "p":
                row.append(pipes.CELL_PIPE)
            elif char == "s":
                row.append(pipes.CELL_START)
                start_x, start_y = x, y
            elif char == "f":
                row.append(pipes.CELL_FINISH)
                finish_x, finish_y = x, y
        board.append(row)
    return board, start_x, start_y, finish_x, finish_y
