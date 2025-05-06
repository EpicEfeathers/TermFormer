from pynput.keyboard import Key, KeyCode
from asciimatics.event import KeyboardEvent
import json

from scripts.popups.popup_handling import PopupCreator
from config import termColours, keys

# shows a popup when the game is paused
class HelpPopup:
    def __init__(self, dimensions, main_menu):
        self.showing_help_popup = False

        self.popup_dimensions = (45, 13)

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)

        self.main_menu = main_menu

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):
        self.popup_creator.create_background(screen)

        x_pos = int((150-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text("Help", screen, y=15 - 5)
        self.popup_creator.add_text("• Get to the door to escape the level", screen, x=x_pos, y=15 - 3)
        self.popup_creator.add_text("• Avoid spikes", screen, x=x_pos, y=15 - 1)

        self.popup_creator.add_text("Controls", screen, y=15 + 1)
        self.popup_creator.add_coloured_text(screen, "• Use WASD / Space to move", termColours.black, background_colour=termColours.popup_gray, coloured_words=["WASD", "Space"], x=x_pos, y=15 + 3)
        self.popup_creator.add_coloured_text(screen, "• Press Q or ESC to pause / close popups", termColours.black, background_colour=termColours.popup_gray, coloured_words=["Q", "ESC"], x=x_pos, y=15 + 5)


        screen.refresh()



    #INPUT: Event
    #RETURN: None
    #PURPOSE: Handle inputs for the help menu
    def handle_inputs(self, event, screen):
        if isinstance(event, KeyboardEvent):
            if (event.key_code == keys.ESC) or (event.key_code == keys.q):
                self.showing_help_popup = False
                self.main_menu.main_menu = True
                screen.clear() # clear screen, efffectively removing popup