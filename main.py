# docs: https://asciimatics.readthedocs.io/en/stable/io.html

from asciimatics.screen import Screen
from asciimatics.screen import ManagedScreen

from time import sleep
import time
import random

FPS = 60

def fill_screen(screen):
    random_num = (random.randint(0, screen.width - 1), random.randint(0, screen.height - 1))
    for y in range(screen.height):
        for w in range(screen.width):
            if (w,y) == random_num:
                screen.print_at("X", w, y, colour=Screen.COLOUR_BLUE)
            else:
                screen.print_at("0", w, y, colour=Screen.COLOUR_RED)
    return screen

def demo(screen):
    while True:
        start = time.time() # start time to calculate delta time

        random_num = (random.randint(0, screen.width - 1), random.randint(0, screen.height - 1))
        screen = fill_screen(screen)


        screen.refresh()

        # calculate delta time
        delta_time = time.time() - start


Screen.wrapper(demo)