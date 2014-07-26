import pipes

def load_level(levelnumber):
    level = {} # dictionary for holding level board and info
    filelines = open("levels/%d" % levelnumber).read().splitlines()
    load_pipes(level, (l for l in filelines if "=" in l))
    load_board(level, (l for l in filelines if "=" not in l))
    level["won"], level["lost"] = False, False
    return level

def load_board(level, boardlines):
    level["flow_started"] = False
    level["flow"] = []
    level["board"] = []
    level["starts"] = []
    level["checkpoints"] = []
    level["finishes"] = []
    for y, boardline in enumerate(boardlines):
        row = []
        for x, char in enumerate(boardline): 
            cell = get_cell_int(char)
            row.append(cell)
            if cell == pipes.CELL_START:
                level["starts"].append((x, y))
            elif cell == pipes.CELL_FINISH:
                level["finishes"].append((x, y))
            elif cell == pipes.CELL_CHECKPOINT:
                level["checkpoints"].append((x, y))
        level["board"].append(row)

def load_pipes(level, pipelines):
    level["pipes"] = pipes.PIPES
    for line in pipelines:
        char, qty = line.split("=")
        pipe = next(p for p in level["pipes"] if p["char"] == char)
        pipe["qty"] = int(qty)

def get_cell_int(string):
    return pipes.CELL_MAP[pipes.CELL_MAP.index(string) + 1]
