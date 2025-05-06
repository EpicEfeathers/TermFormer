import json
from datetime import datetime

from config import termColours, keys
from level_scripts.popups.popup_handling import PopupCreator
from level_scripts.popups.save_deletion_popup import SaveDeletionPopup
import create_colour_list

# popup that shows, allowing user to choose a save
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
        self.save_deletion_popup = SaveDeletionPopup(self.dimensions)

        self.selected_item = 1

        self.slot1_name, self.slot2_name, self.slot3_name = self.get_file_times()


        self.currently_saved = True # start off as saved, as when you open, it is saved

    #INPUT: None
    #RETURN: str, str, str
    #PURPOSE: Gets the files last edited times from the playermade files.
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

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Shows the popup
    def show_popup(self, screen):

        # create rectangle
        self.popup_creator.create_background(screen)

        self.popup_creator.add_text("Save Slots", screen, y=int(self.dimensions[1]/2) - 4)

        x_pos = int((self.dimensions[0]-self.popup_dimensions[0])/2) + 2 # align 2 px from the left of the popup
        self.popup_creator.add_text(f"Slot 1 – {self.slot1_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) -2, background_colour=termColours.white)
        self.popup_creator.add_text(f"Slot 2 – {self.slot2_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 0)
        self.popup_creator.add_text(f"Slot 3 – {self.slot3_name}", screen, x=x_pos, y=int(self.dimensions[1]/2) + 2)

        self.popup_creator.add_text("↑/↓ to move | ⏎ to select | ⌫ to delete", screen, y=int(self.dimensions[1]/2) + 4)

        screen.refresh()

    #INPUT: int, screen, class, dict
    #RETURN: None
    #PURPOSE: Handles the users inputs, doing the correct code
    def handle_input(self, key_code, screen, level_renderer=None, level_data=None): 
        '''
        Handle input
        (Arrow keys / Level Deletion / Level Selection)
        '''
        screen.refresh()
        if key_code == keys.DEL: # show deletion popup
            self.save_deletion_popup.show_popup(screen)

        # if trying to close deletion popup
        elif ((key_code == keys.q) or (key_code == keys.ESC)):# and self.save_deletion_popup.showing_save_deletion_popup:
            self.save_deletion_popup.hide_popup(screen)
            #self.showing_save_slot_popup = False

        elif key_code == keys.enter:
            if self.save_deletion_popup.showing_save_deletion_popup: # if showing deletion popup
                self.delete_level() # reset (basically delete data)

                self.slot1_name, self.slot2_name, self.slot3_name = self.get_file_times() # reset file names (as they have changed)
                self.show_popup(screen) # reshow popup to show these changes

                self.save_deletion_popup.hide_popup(screen) # hide save deletion popup
                self.save_deletion_popup.showing_save_deletion_popup = False
            else:
                level_renderer.render_level(self.dimensions, screen, level_data) # render level
                self.showing_save_slot_popup = False

        else: # switch highlighted level
            # if not in deletion popup
            if not self.save_deletion_popup.showing_save_deletion_popup:
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

    #INPUT: None
    #RETURN: None
    #PURPOSE: Delete a level (resets it back to a basic state)
    def delete_level(self):
        data = {"edited": "", "background_colour": 75, "spawn_point": [0, 0], "tiles": []}

        with open(f"data/playermade/level{self.selected_item}.json", "w") as file:
            json.dump(data, file) 

    #INPUT: screen, int, list
    #RETURN: None
    #PURPOSE: Handles saving the screen (and all other necessary data) to the correct file
    def save_screen(self, screen, bg_colour, spawn_point:list):
        self.currently_saved = True # show that file is currently properly saved
        self.show_saved_state(screen)

        now = datetime.now()

        data = {"edited": now.strftime("%Y-%m-%d"), "background_colour": bg_colour, "spawn_point": spawn_point}
        tiles = []
        for h in range(self.dimensions[1] - 1): # don't add the bottom tool bar part
            row = []
            for w in range(self.dimensions[0]):
                if screen.get_from(w,h)[0] == 42: # if spawn point (42 == *), ignore it
                    row.append([32, bg_colour, 0, bg_colour])
                else:
                    row.append(screen.get_from(w, h))
            tiles.append(row)

        data["tiles"] = tiles

        with open(f"data/playermade/level{self.selected_item}.json", "w") as file:
            json.dump(data, file) 


    #INPUT: screen
    #RETURN: None
    #PURPOSE: Shows if the screen is saved or not through a little indicator at the bottom of the editor.
    def show_saved_state(self, screen): # print text at bottom to show if saved or not
        if self.currently_saved:
            highlight_text_colour = termColours.save_green
        else:
            highlight_text_colour = termColours.red
        colour_list = create_colour_list.create_colour_list("Saved: ████", ["████"], base_text_colour=termColours.popup_gray, background_color=termColours.black, highlight_text_colour=[highlight_text_colour])
        screen.paint("Saved: ████", 100, self.dimensions[1] - 1, colour_map=colour_list)

        screen.refresh()