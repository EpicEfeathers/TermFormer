from asciimatics.screen import Screen

from level_scripts.popups.popup_handling import PopupCreator
from config import termColours

class HelpPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (48, 15)
        self.dimensions = dimensions
        self.popup_text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_help_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.popup_text_colour, self.popup_colour)

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Prints the help text at the bottom of the screen
    def print_help_tip_text(self, screen):
        text = "[H] for help"

        position = (int((self.dimensions[0]/4 - len(text)/2)), self.dimensions[1] - 1)

        self.popup_creator.add_coloured_text(screen=screen, text=text, text_colour=Screen.COLOUR_WHITE, background_colour=Screen.COLOUR_BLACK, coloured_words=["[H]"], y=position[1], x=position[0]) # backwards as function requires it to be like this

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Shows the help popup
    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        self.popup_creator.add_text("CONTROLS", screen, y=int(self.dimensions[1]/2) - 6)
        self.popup_creator.add_coloured_text(screen, "Click or drag to draw", self.popup_text_colour, self.popup_colour, ["Click", "drag"], y=int(self.dimensions[1]/2) - 4)
        self.popup_creator.add_coloured_text(screen, "Press S to save", self.popup_text_colour, self.popup_colour, ["S"], y=int(self.dimensions[1]/2) - 2)
        self.popup_creator.add_coloured_text(screen, "Press Enter to change colour", self.popup_text_colour, self.popup_colour, ["Enter"], y=int(self.dimensions[1]/2) - 0)
        self.popup_creator.add_coloured_text(screen, "Press B to change background colour", self.popup_text_colour, self.popup_colour, ["B"], y=int(self.dimensions[1]/2) + 2)
        self.popup_creator.add_coloured_text(screen, "Press Space (or use keys 1-4) to change tool", self.popup_text_colour, self.popup_colour, ["Space", "1-4"], y=int(self.dimensions[1]/2) + 4)
        self.popup_creator.add_coloured_text(screen, "Press H again (or ESC) to close", self.popup_text_colour, self.popup_colour, ["H", "ESC"], y=int(self.dimensions[1]/2) + 6)

        screen.refresh()
        self.showing_help_popup = True

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Hides the help popup
    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_help_popup = False