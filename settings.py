import curses

# Controls
move_up = (curses.KEY_UP, ord("k"))
move_right = (curses.KEY_RIGHT, ord("l"))
move_down = (curses.KEY_DOWN, ord("j"))
move_left = (curses.KEY_LEFT, ord("h"))
increase_flow_speed = (ord("f"),)
increase_flow_speed_more = (ord("F"),)
place_pipe = (ord(" "),)
rotate = (ord("r"),)
quit = (ord("q"), )
