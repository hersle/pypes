import curses
import game
import log

def get_menu_selection(win, menu):
    # Center menu vertically in window
    win_height, win_width = win.getmaxyx()
    cursor_y = int(win_height / 2) - int(len(menu) / 2)
    
    selection = 0
    while True:
        # Display menu
        for i, menuitem in enumerate(menu):
            # Center menu horizontally in window
            cursor_x = int(win_width / 2) - int(len(menuitem) / 2)
            attrs = curses.A_REVERSE if i == selection else curses.A_NORMAL
            win.addstr(cursor_y + i, cursor_x, menuitem, attrs)

        # Get input
        ch = win.getch()
        if ch == curses.KEY_UP: # move selection up
            selection = (selection - 1) % len(menu)
        elif ch == curses.KEY_DOWN: # move selection down
            selection = (selection + 1) % len(menu)
        elif ch == ord("\n"): # enter
            win.erase()
            win.refresh()
            return selection

def main_menu(win):
    while True:
        menu = ["Play game", "Create level", "Settings", "Exit"]
        selection = get_menu_selection(win, menu)
        if selection == 0:
            game.play()
        elif selection == 1:
            pass
        elif selection == 2:
            pass
        elif selection == 3:
            return
