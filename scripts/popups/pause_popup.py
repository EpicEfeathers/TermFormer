from scripts.popups.popup_handling import PopupCreator
from asciimatics.event import KeyboardEvent

from config import termColours, keys

# shows a popup when the game is paused
class PausePopup:
    def __init__(self, dimensions, game_controls):
        self.showing_pause_popup = False

        self.popup_dimensions = (28, 9)

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)
        self.game_controls = game_controls

        self.selected_index = 1

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):
        self.showing_pause_popup = True

        self.popup_creator.create_background(screen)

        x_pos = int((150-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text("PAUSE MENU", screen, y=15 - 3)
        self.popup_creator.add_text("Resume", screen, x=x_pos, y=15 - 1, background_colour=(termColours.white if (self.selected_index % 2) == 1 else None))
        self.popup_creator.add_text("Main Menu", screen, x=x_pos, y=15 + 1, background_colour=(termColours.white if (self.selected_index % 2) == 0 else None))

        self.popup_creator.add_text("↑/↓ to move | ⏎ to select", screen, y=15 + 3)

        screen.refresh()

    #INPUT: Event
    #RETURN: None
    #PURPOSE: Handle inputs for the slot
    def handle_inputs(self, event, screen):
        if isinstance(event, KeyboardEvent):
            # up key
            if event.key_code == keys.up:
                self.selected_index -= 1
            # down key
            elif event.key_code == keys.down:
                self.selected_index += 1
            # enter key
            elif event.key_code == keys.enter:
                if (self.selected_index % 2) == 1:
                    self.showing_pause_popup = False
                else:
                    # go to main menu
                    screen.clear()
                    self.game_controls.main_menu.main_menu = True
        