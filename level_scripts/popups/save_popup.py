import json
from datetime import datetime

from config import termColours
from level_scripts.popups.popup_handling import PopupCreator

class SavePopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (30, 1)
        self.input_text = ""

        self.showing_save_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.text_colour, self.popup_colour, self.input_dimensions)

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)

        # create rectangle
        self.popup_creator.create_background(screen)

        self.popup_creator.add_text("Save level as:", screen, y=int(self.dimensions[1]/2) - 2)

        self.popup_creator.input_field.show_input_text(screen, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2), background_colour=termColours.white)

        button_text = " Click to save "
        self.popup_creator.add_button(screen, button_text, x=int((self.dimensions[0] - len(button_text))/2), y=int(self.dimensions[1]/2) + 2)

        screen.refresh()
        self.showing_save_popup = True

    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_save_popup = False

    def handle_inputs(self, event, screen): 
        if 33 <= event.key_code <= 126:
            self.popup_creator.input_field.edit_input_text(screen, event.key_code, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2), maximum_text_length=30)
            screen.refresh()
        elif event.key_code == -300: # del key
            self.popup_creator.input_field.delete_input_text(screen, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2))
            screen.refresh()

    def save_button_clicked(self, screen):
        self.input_text = self.popup_creator.input_field.return_input_text()
        self.hide_popup(screen)
        self.save_screen(screen, self.input_text)

    def save_screen(self, screen, file_name):
        now = datetime.now()

        data = {"level_name": "Example level name", "Edited": now.strftime("%Y-%m-%d"), "background_colour": 75}
        tiles = []
        for h in range(self.dimensions[1] - 1): # don't add the bottom tool bar part
            row = []
            for w in range(self.dimensions[0]):
                row.append(screen.get_from(w, h))
            tiles.append(row)

        data["tiles"] = tiles

        with open(f"data/playermade/{file_name}.json", "w") as file:
            json.dump(data, file) 