import pipes
import log

def load_board(level):
    filelines = open("levels/level%d" % level).read().splitlines()
    boardlines = []
    metalines = []
    while filelines:
        if ":" in filelines[0]:
            metalines.append(filelines.pop(0))
        else:
            boardlines.append(filelines.pop(0))
    log.log("boardlines=%s" % boardlines)
    log.log("metalines=%s" % metalines)
    
    board = []
    start_x, start_y, finish_x, finish_y = None, None, None, None
    for y, boardline in enumerate(boardlines):
        row = []
        for x, char in enumerate(boardline): 
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

    for metaline in metalines:
        if metaline.startswith("Pipes: "):
            pass

    return board, start_x, start_y, finish_x, finish_y
