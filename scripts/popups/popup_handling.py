# THIS FILE IS DIFFERENT AS METHODS CHANGE BETWEEN THE LEVEL EDITOR AND THE MAIN GAME

from asciimatics.screen import Screen

from create_colour_list import create_colour_list
from config import termColours

# Class to ease creation of popups
class PopupCreator:
    def __init__(self, dimensions, popup_dimensions:tuple, text_colour, popup_colour, input_dimensions:tuple=None):
        self.dimensions = dimensions
        self.popup_dimensions = popup_dimensions
        self.text_colour = text_colour
        self.popup_colour  = popup_colour

        if input_dimensions: # if argument is passed (if we need an input field)
            self.input_field = InputField(dimensions=self.dimensions, input_dimensions=input_dimensions, text_colour=self.text_colour, background_colour=termColours.white)

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Saves the pixels under the popup to be used to recreate afterwards.
    def save_under_popup(self, screen):
        '''
        Creates list of tuples (first index ASCII char, second Screen colour)
        '''
        self.saved_pixels = []
        top_left = (int((self.dimensions[0]-self.popup_dimensions[0])/2), int((self.dimensions[1]-self.popup_dimensions[1])/2))
        for h in range(self.popup_dimensions[1]):
            #row = []
            for w in range(self.popup_dimensions[0]):
                pixel = screen.get_from(top_left[0] + w, top_left[1] + h) # just need foreground and background, not other attributes
                #row.append(pixel)
                self.saved_pixels.append(pixel)

    #INPUT: screen
    #RETURN: None
    #PURPOSE: Recreates pixels under popup.
    def recreate_under_popup(self, screen):
        '''
        Recreates what was hidden by popup
        '''
        top_left = (int((self.dimensions[0]-self.popup_dimensions[0])/2), int((self.dimensions[1]-self.popup_dimensions[1])/2))

        screen.clear_buffer(x=top_left[0], y=top_left[1], w=self.popup_dimensions[0], h=self.popup_dimensions[1], fg=termColours.sky_blue, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        
        # recreate every pixel covered by the popup
        i = 0
        for h in range(self.popup_dimensions[1]):
            for w in range(self.popup_dimensions[0]):
                screen.print_at(chr(self.saved_pixels[i][0]), top_left[0] + w, top_left[1] + h, self.saved_pixels[i][1], self.saved_pixels[i][2], self.saved_pixels[i][3]) # char converts ASCII number (e.g. 32) to it's character (e.g. " ")
                i += 1

    #INPUT: screen, int
    #RETURN: None
    #PURPOSE: Creates the grey background for the popup.
    def create_background(self, screen, y_offset=0):
        # create rectangle
        start_pos = (int((self.dimensions[0]-self.popup_dimensions[0])/2), int((self.dimensions[1]-self.popup_dimensions[1])/2 + y_offset))
        top_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1])
        bottom_left = (start_pos[0], start_pos[1] + self.popup_dimensions[1])
        bottom_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1] + self.popup_dimensions[1])
        screen.fill_polygon([[(start_pos), (top_right), (bottom_right), (bottom_left)]], colour=self.popup_colour)

    #INPUT: str, screen, int, int
    #RETURN: None
    #PURPOSE: Adds text to the popup
    def add_text(self, text, screen, y, x=None, background_colour=None):
        if background_colour is None: # if background colour not specified, set it to popup colour
            background_colour = self.popup_colour
        if x is None: # if x is not specified, centre it
            x = int((self.dimensions[0] - len(text))/2)

        screen.print_at(text, x, y, self.text_colour, Screen.A_NORMAL, background_colour)

    #INPUT: screen, str, int, int, list, int, int
    #RETURN: None
    #PURPOSE: Adds coloured text to the popup
    def add_coloured_text(self, screen, text, text_colour, background_colour, coloured_words:list, y, x=None):
        if x is None: # if x is not specified, centre it
            x = int((self.dimensions[0] - len(text))/2)

        # create colour list to allow for multi-colour string        
        colour_list = create_colour_list(text=text, words_to_change=coloured_words, base_text_colour=text_colour, background_color=background_colour, highlight_text_colour=[termColours.white] * len(coloured_words))
        
        screen.paint(text, x, y, background_colour, colour_map=colour_list)

        
    #INPUT: screen, str, int, int
    #RETURN: None
    #PURPOSE: Adds a button to the screen
    def add_button(self, screen, button_text, x, y):
        screen.print_at(button_text, x, y, self.text_colour, Screen.A_NORMAL, termColours.white)
    




# Class to ease creation and handling of input fields
class InputField:
    def __init__(self, dimensions, input_dimensions, text_colour, background_colour):
        self.dimensions = dimensions
        self.input_dimensions = input_dimensions
        self.text_colour = text_colour
        self.background_colour  = background_colour
        
        self.input_text = ""
        self.input_position = tuple()

    #INPUT: screen, int, int, int
    #RETURN: None
    #PURPOSE: Shows the text in the input field
    def show_input_text(self, screen, x, y, background_colour=None):
        self.input_position = (x, y)
        if not background_colour: # if not specified, set to predefined
            background_colour = self.background_colour

        input_text = self.input_text + (" " * (self.input_dimensions[0] - len(self.input_text)))

        screen.print_at(input_text, x, y, self.text_colour, Screen.A_NORMAL, background_colour)

    #INPUT: screen, int, int, int, int
    #RETURN: None
    #PURPOSE: Edits the text in the input field.
    def edit_input_text(self, screen, digit, x, y, maximum_text_length):
        if len(self.input_text) < maximum_text_length:
            self.input_text += chr(digit)
            
            self.show_input_text(screen, x, y)

    #INPUT: screen, int, int
    #RETURN: None
    #PURPOSE: Deletes the last character in the input field
    def delete_input_text(self, screen, x, y):
        if len(self.input_text) >= 1:
            self.input_text = self.input_text[:-1]
            
            self.show_input_text(screen, x, y)

    #INPUT: None
    #RETURN: int
    #PURPOSE: Returns the text of the input field.
    def return_input_text(self):
        return self.input_text