from asciimatics.screen import Screen

from level_scripts.popups.popup_handling import PopupCreator
from config import termColours

# popup that shows, confirming if you want to delete
class SaveDeletionPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (29, 8)
        self.dimensions = dimensions
        self.popup_text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_save_deletion_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.popup_text_colour, self.popup_colour)

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Shows the popup
    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen, -10)

        # add text
        self.popup_creator.add_text("Are you sure you want", screen, y=int(self.dimensions[1]/2) - 13)
        self.popup_creator.add_text("to delete this level?", screen, y=int(self.dimensions[1]/2) - 12)

        self.popup_creator.add_coloured_text(screen, "Enter to delete", text_colour=termColours.black, background_colour=termColours.popup_gray, coloured_words=["Enter"], y=int(self.dimensions[1]/2) - 10)

        self.popup_creator.add_coloured_text(screen, "Press Q or ESC to close", text_colour=termColours.black, background_colour=termColours.popup_gray, coloured_words=["Q", "ESC"], y=int(self.dimensions[1]/2) - 8)


        screen.refresh()
        self.showing_save_deletion_popup = True

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Clears the screen where the popup was, resetting the popup
    def hide_popup(self, screen):
        self.showing_save_deletion_popup = False
        screen.clear_buffer(x=int((self.dimensions[0]-self.popup_dimensions[0])/2), y=int((self.dimensions[1] - self.popup_dimensions[1])/2 - 10), w=self.popup_dimensions[0], h=self.popup_dimensions[1], fg=0, attr=Screen.A_NORMAL, bg=75) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer
        screen.refresh()