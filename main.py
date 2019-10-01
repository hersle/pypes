#!/usr/bin/python3

import curses
import menu

def main(screen):
    try:
        curses.curs_set(False) # hide cursor
        menu.main_menu(screen)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
