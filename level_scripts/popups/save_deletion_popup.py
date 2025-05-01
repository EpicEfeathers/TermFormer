from asciimatics.screen import Screen

from level_scripts.popups.popup_handling import PopupCreator
from config import termColours

class SaveDeletionPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (29, 6)
        self.dimensions = dimensions
        self.popup_text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_save_deletion_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.popup_text_colour, self.popup_colour)

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen, -10)

        # add text
        text = "Are you sure you want"
        self.popup_creator.add_text(text, screen, y=int(self.dimensions[1]/2) - 12)
        text = "to delete this level?"
        self.popup_creator.add_text(text, screen, y=int(self.dimensions[1]/2) - 11)

        text = "Press Enter to delete"
        self.popup_creator.add_text(text, screen, y=int(self.dimensions[1]/2) - 9)

        screen.refresh()
        self.showing_save_deletion_popup = True

    def hide_popup(self, screen):
        screen.clear_buffer(x=int((self.dimensions[0]-self.popup_dimensions[0])/2), y=int((self.dimensions[1] - self.popup_dimensions[1])/2 - 10), w=self.popup_dimensions[0], h=self.popup_dimensions[1], fg=0, attr=Screen.A_NORMAL, bg=75) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer
        screen.refresh()