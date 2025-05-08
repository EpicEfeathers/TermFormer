from asciimatics.event import KeyboardEvent
import json

from scripts.popups.popup_handling import PopupCreator
from config import termColours, keys

# shows a popup when the game is paused
class SaveSlotPopup:
    def __init__(self, dimensions, game_controls):
        self.showing_save_slot_popup = False

        self.popup_dimensions = (33, 13)

        self.popup_creator = PopupCreator(dimensions, self.popup_dimensions, termColours.black, termColours.popup_gray)
        self.game_controls = game_controls

        self.selected_index = 1

        self.slot1_name, self.slot2_name, self.slot3_name = self.get_file_times()

    #INPUT: None
    #RETURN: None
    #PURPOSE: Opens files and gets their most recent edit times
    def get_file_times(self):
        with open(f"data/playermade/level1.json", "r") as file:
            level_1_data = json.load(file)
            slot1 = f"Edited: {level_1_data["edited"]}" if level_1_data["edited"] != "" else "Empty"

        with open(f"data/playermade/level2.json", "r") as file:
            level_2_data = json.load(file)
            slot2 = f"Edited: {level_2_data["edited"]}" if level_2_data["edited"] != "" else "Empty"

        with open(f"data/playermade/level3.json", "r") as file:
            level_3_data = json.load(file)
            slot3 = f"Edited: {level_3_data["edited"]}" if level_3_data["edited"] != "" else "Empty"

        return slot1, slot2, slot3

    #INPUT: screen (asciimatics class)
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def show_popup(self, screen):
        self.popup_creator.create_background(screen)

        x_pos = int((150-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text("Save Slots", screen, y=15 - 4)
        self.popup_creator.add_text(f"Slot 1 – {self.slot1_name}", screen, x=x_pos, y=15 - 2, background_colour=(termColours.white if self.selected_index % 3 == 1 else None))
        self.popup_creator.add_text(f"Slot 2 – {self.slot2_name}", screen, x=x_pos, y=15 - 0, background_colour=(termColours.white if self.selected_index % 3 == 2 else None))
        self.popup_creator.add_text(f"Slot 3 – {self.slot3_name}", screen, x=x_pos, y=15 + 2, background_colour=(termColours.white if self.selected_index % 3 == 0 else None))
        self.popup_creator.add_text("↑/↓ to move | ⏎ to select", screen, y=15 + 4)

        screen.refresh()

    #INPUT: Event
    #RETURN: None
    #PURPOSE: Handle inputs for the slot
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
                if (self.selected_index % 3 == 1) and (self.slot1_name != "Empty"):
                    self.game_controls.level_renderer.file_path = "data/playermade/level1.json"
                    self.showing_save_slot_popup = False
                elif (self.selected_index % 3 == 2) and (self.slot2_name != "Empty"):
                    self.game_controls.level_renderer.file_path = "data/playermade/level2.json"
                    self.showing_save_slot_popup = False
                elif (self.selected_index % 3 == 0) and (self.slot3_name != "Empty"):
                    self.game_controls.level_renderer.file_path = "data/playermade/level3.json"
                    self.showing_save_slot_popup = False
                self.game_controls.level_renderer.get_data()