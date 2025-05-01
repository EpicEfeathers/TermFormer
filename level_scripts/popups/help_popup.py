from asciimatics.screen import Screen

from level_scripts.popups.popup_handling import PopupCreator
from config import termColours

class HelpPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (40, 13)
        self.dimensions = dimensions
        self.popup_text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_help_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.popup_text_colour, self.popup_colour)

    def print_help_tip_text(self, screen):
        text = "[H] for help"
        #text = "[Space] Change Tool | [Enter] Change Colour | [B] Change Background Colour | [S] Save"

        position = (int((self.dimensions[0] - len(text))/2), self.dimensions[1] - 1)
        #self.popup_creator.add_coloured_text(screen=screen, text=text, text_colour=Screen.COLOUR_WHITE, background_colour=Screen.COLOUR_BLACK, coloured_words=["[Space]", "[Enter]", "[B]", "[S]"], y=position[1], x=position[0]) # backwards as function requires it to be like this
        self.popup_creator.add_coloured_text(screen=screen, text=text, text_colour=Screen.COLOUR_WHITE, background_colour=Screen.COLOUR_BLACK, coloured_words=["[H]"], y=position[1], x=position[0]) # backwards as function requires it to be like this

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Click or drag to draw"
        self.popup_creator.add_coloured_text(screen, text, self.popup_text_colour, self.popup_colour, ["Click", "drag"], y=int(self.dimensions[1]/2) - 5)
        text2 = "Press S to save"
        self.popup_creator.add_coloured_text(screen, text2, self.popup_text_colour, self.popup_colour, ["S"], y=int(self.dimensions[1]/2) - 3)
        text3 = "Press Enter to change colour"
        self.popup_creator.add_coloured_text(screen, text3, self.popup_text_colour, self.popup_colour, ["Enter"], y=int(self.dimensions[1]/2) - 1)
        text3 = "Press B to change background colour"
        self.popup_creator.add_coloured_text(screen, text3, self.popup_text_colour, self.popup_colour, ["B"], y=int(self.dimensions[1]/2) + 1)
        text4 = "Press Space to change tool"
        self.popup_creator.add_coloured_text(screen, text4, self.popup_text_colour, self.popup_colour, ["Space"], y=int(self.dimensions[1]/2) + 3)
        text5 = "Press H again (or ESC) to close"
        self.popup_creator.add_coloured_text(screen, text5, self.popup_text_colour, self.popup_colour, ["H", "ESC"], y=int(self.dimensions[1]/2) + 5)

        screen.refresh()
        self.showing_help_popup = True

    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_help_popup = False