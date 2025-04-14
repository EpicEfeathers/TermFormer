from config import termColours
from level_scripts.popups.popup_handling import PopupCreator

class ColourInputPopup:
    def __init__(self, dimensions):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (4, 1)
        self.input_text = ""

        self.showing_colour_input_popup = False

        self.popup_creator = PopupCreator(self.dimensions, self.popup_dimensions, self.text_colour, self.popup_colour, self.input_dimensions)


    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Input terminal colour (0-255):"
        self.popup_creator.add_text(text, screen, y=int(self.dimensions[1]/2) - 3)
        text2 = "Type numbers 0-9, Del to delete"
        self.popup_creator.add_text(text2, screen, y=int(self.dimensions[1]/2) - 2)
        text3 = "Press Enter again to confirm"
        self.popup_creator.add_text(text3, screen, y=int(self.dimensions[1]/2) - 1)

        # add input box
        self.popup_creator.show_input_text(screen, termColours.white, self.input_text, self.input_dimensions, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2) + 1)

        # add button
        button_text = " Colour diagram (click me!) "
        self.popup_creator.add_button(screen, button_text, x=int((self.dimensions[0] - len(button_text))/2), y=int(self.dimensions[1]/2) + 3)

        screen.refresh()
        self.showing_colour_input_popup = True

    def handle_inputs(self, event, screen):
        if 48 <= event.key_code <= 57: # keys 0-9
            self.popup_creator.input_field.edit_input_text(screen, event.key_code, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2) + 1, maximum_text_length=3)
            screen.refresh()
        elif event.key_code == -300: # del key
            self.popup_creator.input_field.delete_input_text(screen, x=int((self.dimensions[0] - self.input_dimensions[0])/2), y=int(self.dimensions[1]/2) + 1)
            screen.refresh()

    def check_valid_input(self, screen, pen):
        self.showing_colour_input_popup = self.popup_creator.input_field.check_if_valid(screen, pen, self.popup_creator)