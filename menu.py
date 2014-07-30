import curses
import game
import os

def get_menu_selection(win, title_lines, menu):
    win.erase()
    win_height, win_width = win.getmaxyx()
    menu_max_width = max(len(menuitem) for menuitem in menu + title_lines)
    menu_titled = title_lines + ["-" * menu_max_width] + menu
    cursor_y = int(win_height / 2) - int(len(menu_titled) / 2)  # center

    selection = 0
    while True:
        # Display menu
        for i, menuitem in enumerate(menu_titled, start=-len(title_lines)-1):
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
            return selection

def main_menu(screen):

    title_lines = [
        "████████  ██    ██  ████████  ████████  ████████",
        "██    ██  ██    ██  ██    ██  ██        ██      ",
        "████████  ████████  ████████  ██████    ████████",
        "██           ██     ██        ██              ██",
        "██           ██     ██        ████████  ████████",
    ]   
    menu = ["Play game", "Exit"]
    while True:
        selection = get_menu_selection(screen, title_lines, menu)
        if selection == 0:
            select_level(screen)
        elif selection == 1:
            break

def post_game_menu(win, game_won, level_number):
    if game_won:
        title_lines = [
            "████████  ████████  ████████  ████████    ██ ██ ██  ████████  ███   ██",
            "██        ██    ██  ██ ██ ██  ██          ██ ██ ██  ██    ██  ████  ██",
            "██  ████  ████████  ██ ██ ██  ██████      ██ ██ ██  ██    ██  ██ ██ ██",
            "██    ██  ██    ██  ██ ██ ██  ██          ██ ██ ██  ██    ██  ██  ████",
            "████████  ██    ██  ██ ██ ██  ████████    ████████  ████████  ██   ███",
        ]
    else:
        title_lines = [
            "████████  ████████  ████████  ████████    ████████  ██    ██  ████████  ████████",
            "██        ██    ██  ██ ██ ██  ██          ██    ██  ██    ██  ██        ██    ██",
            "██  ████  ████████  ██ ██ ██  ██████      ██    ██  ██    ██  ██████    ████████",
            "██    ██  ██    ██  ██ ██ ██  ██          ██    ██  ██    ██  ██        ██  ██  ",
            "████████  ██    ██  ██ ██ ██  ████████    ████████    ████    ████████  ██    ██",
        ]
    menu = ["Main menu"]
    get_menu_selection(win, title_lines, menu)

def select_level(win):
    title_lines = [
        "████████  ████████  ██        ████████  ████████  ████████    ██        ████████ ██    ██  ████████  ██      ",
        "██        ██        ██        ██        ██           ██       ██        ██       ██    ██  ██        ██      ",
        "████████  ██████    ██        ██████    ██           ██       ██        ██████   ██    ██  ██████    ██      ",
        "      ██  ██        ██        ██        ██           ██       ██        ██       ██    ██  ██        ██      ",
        "████████  ████████  ████████  ████████  ████████     ██       ████████  ████████   ████    ████████  ████████"
    ]
    menu = ["Level " + l for l in os.listdir("levels") if l.isdigit()] + ["Back"]
    selection = get_menu_selection(win, title_lines, menu)
    if selection == len(menu) - 1:
        return
    else:
        level_number = selection + 1
        game.play(win, level_number)
