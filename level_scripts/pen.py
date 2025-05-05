from asciimatics.screen import Screen

from config import termColours

# handles anything pen related
class Pen:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.pen_colour = termColours.white

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Prints the pen colour at the bottom left of the screen 
    def print_pen_colour(self, screen):

        screen.clear_buffer(x=0, y=self.dimensions[1] - 1, w=22, h=1, fg=termColours.white, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK)

        screen.print_at("Pen colour: ", 0, self.dimensions[1] - 1)
        screen.print_at(f"████ ({self.pen_colour})", len("Pen colour: "), self.dimensions[1] - 1, self.pen_colour)