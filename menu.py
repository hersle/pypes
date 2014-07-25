import curses
import game
import log
import os

def get_menu_selection(win, menu_title, menu):
    menu_titled = [menu_title, "-" * len(menu_title)] + menu
    win.border()
    win_height, win_width = win.getmaxyx()
    cursor_y = int(win_height / 2) - int(len(menu_titled) / 2)  # center

    selection = 0
    while True:
        # Display menu
        for i, menuitem in enumerate(menu_titled, start=-2):
            cursor_x = int(win_width / 2) - int(len(menuitem) / 2)  # center
            attrs = curses.A_REVERSE if i == selection else curses.A_NORMAL
            win.addstr(cursor_y + i + 2, cursor_x, menuitem, attrs)

        # Get input
        ch = win.getch()
        if ch == curses.KEY_UP:  # move selection up
            selection = (selection - 1) % len(menu)  # wrap to bottom
        elif ch == curses.KEY_DOWN:  # move selection down
            selection = (selection + 1) % len(menu)  # wrap to top
        elif ch == ord("\n"):  # enter
            win.erase()
            win.refresh()
            return selection

def main_menu(screen):
    menu_title = "Main menu"
    menu = ["Play game", "Create level", "Controls", "Exit"]
    while True:
        selection = get_menu_selection(screen, menu_title, menu)
        if selection == 0:
            level_select_menu(screen)
            #game.play(screen, 2)
        elif selection == 1:
            pass
        elif selection == 2:
            settings_menu(screen)
        elif selection == 3:
            return

def post_game_menu(win, game_won):
    menu_title = "Game won" if game_won else "Game lost"
    menu = ["OK"]
    get_menu_selection(win, menu_title, menu)

def settings_menu(win):
    menu_title = "Edit settings.py to customize controls"
    menu = ["OK"]
    get_menu_selection(win, menu_title, menu)

def level_select_menu(win):
    menu_title = "Select level"
    menu = ["Level " + l for l in os.listdir("levels") if l.isdigit()]
    game.play(win, get_menu_selection(win, menu_title, menu) + 1)
