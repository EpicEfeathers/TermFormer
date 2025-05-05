from scripts.popups.popup_handling import PopupCreator

from config import termColours

# shows a popup when the game is paused
class PausePopup:
    def __init__(self, dimensions):
        self.showing_pause_popup = False

        self.popup_dimensions = (50, 30)

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):
        self.showing_pause_popup = True

        self.popup_creator.create_background(screen)

        screen.print_at(self.showing_pause_popup, 0, 0)
        screen.refresh()