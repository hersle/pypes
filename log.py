def log(msg, level=0):
    open("log", "a").write("  " * level + msg + "\n")
