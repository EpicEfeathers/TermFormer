from asciimatics.screen import Screen

from level_scripts.popups.popup_handling import PopupCreator
from config import termColours

class HelpPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (40, 11)
        self.dimensions = dimensions
        self.popup_text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_help_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.popup_text_colour, self.popup_colour)

    def print_help_tip_text(self, screen):
        text = "Press H for help"

        position = (int((self.dimensions[0] - len(text))/2), self.dimensions[1] - 1)
        self.popup_creator.add_coloured_text(screen=screen, text=text, text_colour=Screen.COLOUR_WHITE, background_colour=Screen.COLOUR_BLACK, coloured_words=["H"], y=position[1], x=position[0]) # backwards as function requires it to be like this
        #colour_list = create_colour_list(text, ["H"], Screen.COLOUR_WHITE, background_color=Screen.COLOUR_BLACK, highlight_popup_text_colour=[termColours.white])
        #screen.paint(text, *position, colour_map=colour_list)

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Click or drag to draw"
        self.popup_creator.add_coloured_text(screen, text, self.popup_text_colour, self.popup_colour, ["Click", "drag"], y=int(self.dimensions[1]/2) - 4)
        text2 = "Press S to save"
        self.popup_creator.add_coloured_text(screen, text2, self.popup_text_colour, self.popup_colour, ["S"], y=int(self.dimensions[1]/2) - 2)
        text3 = "Press Enter to change colour"
        self.popup_creator.add_coloured_text(screen, text3, self.popup_text_colour, self.popup_colour, ["Enter"], y=int(self.dimensions[1]/2))
        text4 = "Press Space to change tool"
        self.popup_creator.add_coloured_text(screen, text4, self.popup_text_colour, self.popup_colour, ["Space"], y=int(self.dimensions[1]/2) + 2)
        text5 = "Press H again to close"
        self.popup_creator.add_coloured_text(screen, text5, self.popup_text_colour, self.popup_colour, ["H"], y=int(self.dimensions[1]/2) + 4)

        screen.refresh()
        self.showing_help_popup = True

    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_help_popup = False