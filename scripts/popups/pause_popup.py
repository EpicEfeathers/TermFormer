from scripts.popups.popup_handling import PopupCreator

from config import termColours

# shows a popup when the game is paused
class PausePopup:
    def __init__(self, dimensions):
        self.showing_pause_popup = False

        self.popup_dimensions = (28, 9)

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):
        self.showing_pause_popup = True

        self.popup_creator.create_background(screen)

        x_pos = int((150-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text("PAUSE MENU", screen, y=15 - 3)
        self.popup_creator.add_text("Resume", screen, x=x_pos, y=15 - 1)
        self.popup_creator.add_text("Main Menu", screen, x=x_pos, y=15 + 1)

        self.popup_creator.add_text("↑/↓ to move | ⏎ to select", screen, y=15 + 3)

        screen.refresh()