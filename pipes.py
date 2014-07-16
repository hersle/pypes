#!/usr/bin/python

import curses

def main(screen):
    curses.curs_set(False) # disable cursor

if __name__ == "__main__":
    curses.wrapper(main)
