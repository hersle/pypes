import pipes
import log
import re

def load_board(levelnumber):
    # Dictionary for holding level board and information
    level = {}

    # Separate into boardlines and metalines
    filelines = open("levels/level%d" % levelnumber).read().splitlines()
    metalines = []
    boardlines = []
    for line in filelines:
        if "meta" in line: metalines.append(line)
        else: boardlines.append(line)
    log.log("boardlines=%s" % boardlines)
    log.log("metalines=%s" % list(metalines))
    
    # Parse board
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
                level["start_x"] = x
                level["start_y"] = y
                #start_x, start_y = x, y
            elif char == "f":
                row.append(pipes.CELL_FINISH)
                level["finish_x"] = x
                level["finish_y"] = y
                #finish_x, finish_y = x, y
        board.append(row)
    level["board"] = board

    # Parse meta information
    for metaline in metalines:
        if metaline.startswith("Pipes: "):
            pass

    return level
    #return board, start_x, start_y, finish_x, finish_y
