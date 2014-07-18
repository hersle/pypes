#!/usr/bin/python

import curses
import menu

def main(screen):
    curses.curs_set(False) # hide cursor
    menu.main_menu(screen)

if __name__ == "__main__":
    curses.wrapper(main)
