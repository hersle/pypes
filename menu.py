import curses
import game
import log

def get_menu_selection(win, menu_title, menu):
    win.border()
    menu_titled = [menu_title, "-" * len(menu_title)] + menu
    # Center menu vertically in window
    win_height, win_width = win.getmaxyx()
    cursor_y = int(win_height / 2) - int(len(menu_titled) / 2)

    selection = 0
    while True:
        # Display menu
        for i, menuitem in enumerate(menu_titled, start=-2):
            # Center menu horizontally in window
            cursor_x = int(win_width / 2) - int(len(menuitem) / 2)
            attrs = curses.A_REVERSE if i == selection else curses.A_NORMAL
            win.addstr(cursor_y + i + 2, cursor_x, menuitem, attrs)

        # Get input
        ch = win.getch()
        if ch == curses.KEY_UP: # move selection up
            selection = (selection - 1) % len(menu)
        elif ch == curses.KEY_DOWN: # move selection down
            selection = (selection + 1) % len(menu)
        elif ch in (ord("\n"), ord(" ")): # enter
            win.erase()
            win.refresh()
            return selection

def main_menu(win):
    menu_title = "Main menu"
    menu = ["Play game", "Create level", "Controls", "Exit"]
    while True:
        selection = get_menu_selection(win, menu_title, menu)
        if selection == 0:
            game.play()
        elif selection == 1:
            pass
        elif selection == 2:
            settings_menu(win)
        elif selection == 3:
            return

def post_game_menu(win, game_won):
    menu_title = "Game won" if game_won else "Game lost"
    menu = ["OK"]
    selection = get_menu_selection(win, menu_title, menu)

def settings_menu(win):
    menu_title = "Controls"
    menu = ["Move up", "Move right", "Move down", "Move left", "Back"]
    while True:
        selection = get_menu_selection(win, menu_title, menu)
        if selection == 0:
            pass
        elif selection == 1:
            pass
        elif selection == 2:
            return
