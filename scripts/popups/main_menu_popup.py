from asciimatics.event import KeyboardEvent

from scripts.popups.popup_handling import PopupCreator
from scripts.popups.save_slot_popup import SaveSlotPopup
from scripts.popups.help_popup import HelpPopup
from config import termColours, keys

# shows a popup when the game is paused
class MainMenu:
    def __init__(self, dimensions, game_controls):
        self.main_menu = True

        self.popup_dimensions = (31, 13)
        self.game_controls = game_controls

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)
        self.save_slot_popup = SaveSlotPopup(dimensions, game_controls)
        self.help_popup = HelpPopup(dimensions, self)

        self.selected_index = 1

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):

        self.popup_creator.create_background(screen)

        x_pos = int((150-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text("MAIN MENU", screen, y=15 - 5)
        self.popup_creator.add_text("Play", screen, x=x_pos, y=15 - 3, background_colour=(termColours.white if self.selected_index % 4 == 1 else None))
        self.popup_creator.add_text("Play Custom Level", screen, x=x_pos, y=15 - 1, background_colour=(termColours.white if self.selected_index % 4 == 2 else None))
        self.popup_creator.add_text("Help", screen, x=x_pos, y=15 + 1, background_colour=(termColours.white if self.selected_index % 4 == 3 else None))
        self.popup_creator.add_text("Close Game", screen, x=x_pos, y=15 + 3, background_colour=(termColours.white if self.selected_index % 4 == 0 else None))

        self.popup_creator.add_text("↑/↓ to move | ⏎ to select", screen, y=15 + 5)

        screen.refresh()

    #INPUT: Event
    #RETURN: None
    #PURPOSE: Handle inputs on the main menu
    def handle_inputs(self, event):
        if isinstance(event, KeyboardEvent):
            # if up key
            if event.key_code == keys.up:
                self.selected_index -= 1
            # if down key
            elif event.key_code == keys.down:
                self.selected_index += 1
            # if enter key
            elif event.key_code == keys.enter:
                self.main_menu = False
                if self.selected_index % 4 == 1: # if option 1 (play game)
                    self.game_controls.level_renderer.get_data()
                    #self.main_menu = False
                elif self.selected_index % 4 == 2:
                    self.save_slot_popup.showing_save_slot_popup = True
                elif self.selected_index % 4 == 3:
                    self.help_popup.showing_help_popup = True
                elif self.selected_index % 4 == 0: # if close game highlighted
                    self.game_controls.running = False