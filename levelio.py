import pipes
import log
import re

def load_level(levelnumber):
    # Dictionary for holding level board and information
    level = {}
    filelines = open("levels/level%d" % levelnumber).read().splitlines()
    load_metainfo(level, filter(lambda l: "meta" in l, filelines))
    load_board(level, filter(lambda l: "meta" not in l, filelines))
    return level

def load_board(level, boardlines):
    board = []
    for y, boardline in enumerate(boardlines):
        row = []
        for x, char in enumerate(boardline): 
            cell = get_cell_int(char)
            row.append(cell)
            if cell == pipes.CELL_START:
                level["start_x"], level["start_y"] = x, y
            elif cell == pipes.CELL_FINISH:
                level["finish_x"], level["finish_y"] = x, y
        board.append(row)
    level["board"] = board

def load_metainfo(level, metalines):
    metaregex = re.compile(r"[a-z_]+=[0-9]+")
    pipes = []
    for metaline in metalines:
        #pipes.append( {"amount" : 9, "pipe" : } ) 
        s = metaregex.search(metaline).group()

def get_cell_int(string):
    return pipes.CELL_MAP[pipes.CELL_MAP.index(string) + 1]

def get_pipe_int(string):
    return pipes.PIPE_MAP[pipes.PIPE_MAP.index(string) + 1]
