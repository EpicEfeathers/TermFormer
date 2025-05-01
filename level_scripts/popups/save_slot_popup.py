import json
from datetime import datetime

from config import termColours, keys
from level_scripts.popups.popup_handling import PopupCreator
from level_scripts.popups.save_deletion_popup import SaveDeletionPopup

class SaveSlotPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (43, 11)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (30, 1)
        self.input_text = ""

        self.showing_save_slot_popup = True

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.text_colour, self.popup_colour, self.input_dimensions)
        self.save_deletion_popup = SaveDeletionPopup(dimensions)

        self.selected_item = 1

        self.slot1_name, self.slot2_name, self.slot3_name = self.get_file_names()

    
    def get_file_names(self):
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

    def show_popup(self, screen):

        # create rectangle
        self.popup_creator.create_background(screen)

        self.popup_creator.add_text("Save Slots", screen, y=int(self.dimensions[1]/2) - 4)

        x_pos = int((self.dimensions[0]-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text(f"Slot 1 – {self.slot1_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) -2, background_colour=termColours.white)
        self.popup_creator.add_text(f"Slot 2 – {self.slot2_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 0)
        self.popup_creator.add_text(f"Slot 3 – {self.slot3_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 2)

        self.popup_creator.add_text("↑/↓ to move | ⏎ to select | ⌫ to delete", screen, y=int(self.dimensions[1]/2) + 4)

        #self.popup_creator.input_field.show_input_text(screen, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2), background_colour=termColours.white)

        #button_text = " Click to save "
        #self.popup_creator.add_button(screen, button_text, x=int((self.dimensions[0] - len(button_text))/2), y=int(self.dimensions[1]/2) + 2)

        screen.refresh()

    def handle_input(self, key_code, screen, level_renderer=None, dimensions=None): 
        '''
        Handle input
        (Arrow keys / Level Deletion)
        '''
        if key_code == keys.DEL: # delete level
            self.save_deletion_popup.show_popup(screen)
        elif key_code == keys.enter:
            if self.save_deletion_popup.showing_save_deletion_popup:
                self.save_screen(screen, reset=True) # reset (basically delete data)

                self.slot1_name, self.slot2_name, self.slot3_name = self.get_file_names() # reset file names (as they have changed)
                self.show_popup(screen) # reshow popup to show these changes

                self.save_deletion_popup.hide_popup(screen) # hide save deletion popup
                self.save_deletion_popup.showing_save_deletion_popup = False
            else:
                level_renderer.render_level(dimensions, self.selected_item, screen) # render level
                self.showing_save_slot_popup = False
        else: # switch highlighted level
            if key_code == keys.up:
                self.selected_item -= 1
            else:
                self.selected_item += 1

            if self.selected_item < 1:
                self.selected_item = 3
            elif self.selected_item > 3:
                self.selected_item = 1

            x_pos = int((self.dimensions[0]-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
            self.popup_creator.add_text(f"Slot 1 – {self.slot1_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) -2, background_colour=(termColours.white if self.selected_item == 1 else None))
            self.popup_creator.add_text(f"Slot 2 – {self.slot2_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 0, background_colour=(termColours.white if self.selected_item == 2 else None))
            self.popup_creator.add_text(f"Slot 3 – {self.slot3_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 2, background_colour=(termColours.white if self.selected_item == 3 else None))

            screen.refresh()

    def save_button_clicked(self, screen, reset=False):
        self.input_text = self.popup_creator.input_field.return_input_text()
        self.hide_popup(screen)
        self.save_screen(screen, self.input_text)

    def save_screen(self, screen, reset=False):
        if reset: # resetting file, basically deleting all data
            data = {"edited": "", "background_colour": 75, "tiles": []}
        else:
            now = datetime.now()

            data = {"edited": now.strftime("%Y-%m-%d"), "background_colour": 75}
            tiles = []
            for h in range(self.dimensions[1] - 1): # don't add the bottom tool bar part
                row = []
                for w in range(self.dimensions[0]):
                    row.append(screen.get_from(w, h))
                tiles.append(row)

            data["tiles"] = tiles

        with open(f"data/playermade/level{self.selected_item}.json", "w") as file:
            json.dump(data, file) 