from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser
import json

from config import termColours, keyboard_event_number_conversion

dimensions = (150, 31)

def create_colour_list(text, words_to_change: list, base_text_colour: int, background_color:int, highlight_text_colour: int):
    colour_list = [(base_text_colour, Screen.A_NORMAL, background_color)] * len(text)
    for word in words_to_change:
        start = (text.find(word))
        length = len(word)
        for i in range(start, start + length): # start pos, end pos
            colour_list[i] = (highlight_text_colour, Screen.A_NORMAL, background_color)
    return colour_list
           

class HelpPopup:
    def __init__(self):
        self.popup_dimensions = (40, 11)
        self.text_colour = termColours.black
        self.popup_colour = termColours.popup_gray

        self.showing_help_popup = False

        self.popup_creator = PopupCreator(self.popup_dimensions, self.text_colour, self.popup_colour)

    def print_help_tip_text(self, screen):
        global dimensions
        text = "Press H for help"

        position = (int((dimensions[0] - len(text))/2), dimensions[1] - 1)
        colour_list = create_colour_list(text, ["H"], Screen.COLOUR_WHITE, background_color=Screen.COLOUR_BLACK, highlight_text_colour=termColours.white)
        screen.paint(text, *position, colour_map=colour_list)

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Click or drag to draw"
        self.popup_creator.add_coloured_text(text, ["Click", "drag"], screen, y=int(dimensions[1]/2) - 4)
        text2 = "Press S to save"
        self.popup_creator.add_coloured_text(text2, ["S"], screen, y=int(dimensions[1]/2) - 2)
        text3 = "Press Enter to change colour"
        self.popup_creator.add_coloured_text(text3, ["Enter"], screen, y=int(dimensions[1]/2))
        text4 = "Press Space to change tool"
        self.popup_creator.add_coloured_text(text4, ["Space"], screen, y=int(dimensions[1]/2) + 2)
        text5 = "Press H again to close"
        self.popup_creator.add_coloured_text(text5, ["H"], screen, y=int(dimensions[1]/2) + 4)

        screen.refresh()
        self.showing_help_popup = True

    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_help_popup = False

class Pen:
    def __init__(self):
        self.pen_colour = termColours.white

    def print_pen_colour(self, screen):
        global dimensions

        screen.clear_buffer(x=0, y=dimensions[1] - 1, w=35, h=1, fg=termColours.white, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK)

        screen.print_at("Current pen colour: ", 0, dimensions[1] - 1)
        screen.print_at(f"████ ({self.pen_colour})", len("Current pen colour: "), dimensions[1] - 1, self.pen_colour)

class Tool:
    def __init__(self):
        self.tool_type = "pen"

    def change_tool_type(self):
        if self.tool_type == "pen":
            self.tool_type = "dropper"
        else:
            self.tool_type = "pen"
    
    def print_tool_type(self, screen):
        global dimensions

        screen.clear_buffer(x=dimensions[0] - 35, y=dimensions[1] - 1, w=35, h=1, fg=termColours.white, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK)

        text = f"Tool: {self.tool_type.capitalize()}"
        colour_list = create_colour_list(text, [self.tool_type.capitalize()], Screen.COLOUR_WHITE, background_color=Screen.COLOUR_BLACK, highlight_text_colour=termColours.white)
        screen.paint(text, dimensions[0] - len(text), dimensions[1] - 1, colour_map=colour_list)

class PopupCreator:
    def __init__(self, popup_dimensions:tuple, text_colour, popup_colour, input_dimensions:tuple=None):
        self.popup_dimensions = popup_dimensions
        self.text_colour = text_colour
        self.popup_colour  = popup_colour

        if input_dimensions: # if argument is passed (if we need an input field)
            self.input_field = InputField(input_dimensions=input_dimensions, text_colour=self.text_colour, background_colour=termColours.white)

    def save_under_popup(self, screen):
        '''
        Creates list of tuples (first index ASCII char, second Screen colour)
        '''
        self.saved_pixels = []
        top_left = (int((dimensions[0]-self.popup_dimensions[0])/2), int((dimensions[1]-self.popup_dimensions[1])/2))
        for h in range(self.popup_dimensions[1]):
            #row = []
            for w in range(self.popup_dimensions[0]):
                pixel = screen.get_from(top_left[0] + w, top_left[1] + h) # just need foreground and background, not other attributes
                #row.append(pixel)
                self.saved_pixels.append(pixel)

    def recreate_under_popup(self, screen):
        '''
        Recreates what was hidden by popup
        '''
        top_left = (int((dimensions[0]-self.popup_dimensions[0])/2), int((dimensions[1]-self.popup_dimensions[1])/2))

        screen.clear_buffer(x=top_left[0], y=top_left[1], w=self.popup_dimensions[0], h=self.popup_dimensions[1], fg=termColours.sky_blue, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        
        # recreate every pixel covered by the popup
        i = 0
        for h in range(self.popup_dimensions[1]):
            for w in range(self.popup_dimensions[0]):
                screen.print_at(chr(self.saved_pixels[i][0]), top_left[0] + w, top_left[1] + h, self.saved_pixels[i][1], self.saved_pixels[i][2], self.saved_pixels[i][3]) # char converts ASCII number (e.g. 32) to it's character (e.g. " ")
                i += 1

    def create_background(self, screen):
        # create rectangle
        start_pos = (int((dimensions[0]-self.popup_dimensions[0])/2), int((dimensions[1]-self.popup_dimensions[1])/2))
        top_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1])
        bottom_left = (start_pos[0], start_pos[1] + self.popup_dimensions[1])
        bottom_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1] + self.popup_dimensions[1])
        screen.fill_polygon([[(start_pos), (top_right), (bottom_right), (bottom_left)]], colour=self.popup_colour)

    def add_text(self, text, screen, y, x=None):
        if x is None: # if x is not specified, centre it
            x = int((dimensions[0] - len(text))/2)

        screen.print_at(text, x, y, self.text_colour, Screen.A_NORMAL, self.popup_colour)

    def add_coloured_text(self, text, coloured_words:list, screen, y, x=None):
        if x is None: # if x is not specified, centre it
            x = int((dimensions[0] - len(text))/2)

        # create colour list to allow for multi-colour string        
        colour_list = create_colour_list(text, coloured_words, Screen.COLOUR_BLACK, background_color=self.popup_colour, highlight_text_colour=termColours.white)
        
        screen.paint(text, x, y, colour_map=colour_list)

        

    def add_button(self, screen, button_text, x, y):
        screen.print_at(button_text, x, y, self.text_colour, Screen.A_NORMAL, termColours.white)

    def show_input_text(self, screen, background_color, input_text, input_dimensions, x, y):
        input_text = input_text + (" " * (input_dimensions[0] - len(input_text)))
        screen.print_at(input_text, x, y, self.text_colour, Screen.A_NORMAL, background_color)

class InputField():
    def __init__(self, input_dimensions, text_colour, background_colour):
        self.input_dimensions = input_dimensions
        self.text_colour = text_colour
        self.background_colour  = background_colour
        
        self.input_text = ""
        self.input_position = tuple()

    def show_input_text(self, screen, x, y, background_colour=None):
        self.input_position = (x, y)
        if not background_colour: # if not specified, set to predefined
            background_colour = self.background_colour

        input_text = self.input_text + (" " * (self.input_dimensions[0] - len(self.input_text)))

        screen.print_at(input_text, x, y, self.text_colour, Screen.A_NORMAL, background_colour)

    def edit_input_text(self, screen, digit, x, y, maximum_text_length):
        if len(self.input_text) < maximum_text_length:
            self.input_text += chr(digit)#str(keyboard_event_number_conversion[digit])
            
            self.show_input_text(screen, x, y)

    def delete_input_text(self, screen, x, y):
        if len(self.input_text) >= 1:
            self.input_text = self.input_text[:-1]
            
            self.show_input_text(screen, x, y)

    def return_input_text(self):
        return self.input_text

    def check_if_valid(self, screen, pen, popup_creator):
        if self.input_text == "": # if user provides no colour, set the colour to the current colour
            self.input_text = pen.pen_colour
        if 0 <= int(self.input_text) <= 255:
            pen.pen_colour = int(self.input_text)

            pen.print_pen_colour(screen)

            # recreate the covered pixels under the popup
            popup_creator.recreate_under_popup(screen)
            screen.refresh()

            self.input_text = "" # set the input field to empty for next time

            return False
        else:
            self.show_input_text(screen, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1, background_colour=termColours.red)
            screen.refresh()

            return True

class SavePopup:
    def __init__(self):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (30, 1)
        self.input_text = ""

        self.showing_save_popup = False

        self.popup_creator = PopupCreator(self.popup_dimensions, self.text_colour, self.popup_colour, self.input_dimensions)

    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)

        # create rectangle
        self.popup_creator.create_background(screen)

        self.popup_creator.add_text("Save level as:", screen, y=int(dimensions[1]/2) - 2)

        self.popup_creator.show_input_text(screen, termColours.white, self.input_text, self.input_dimensions, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2))

        button_text = " Click to save "
        self.popup_creator.add_button(screen, button_text, x=int((dimensions[0] - len(button_text))/2), y=int(dimensions[1]/2) + 2)

        screen.refresh()
        self.showing_save_popup = True

    def hide_popup(self, screen):
        self.popup_creator.recreate_under_popup(screen)

        screen.refresh()
        self.showing_save_popup = False

    def handle_inputs(self, event, screen): 
        if 33 <= event.key_code <= 126:
            self.popup_creator.input_field.edit_input_text(screen, event.key_code, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2), maximum_text_length=30)
            screen.refresh()
        elif event.key_code == -300: # del key
            self.popup_creator.input_field.delete_input_text(screen, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2))
            screen.refresh()

    def save_button_clicked(self, screen):
        self.input_text = self.popup_creator.input_field.return_input_text()
        self.hide_popup(screen)
        self.save_screen(screen, self.input_text)

    def save_screen(self, screen, file_name):
        global dimensions

        data = []
        for h in range(dimensions[1] - 1): # don't add the bottom tool bar part
            row = []
            for w in range(dimensions[0]):
                row.append(screen.get_from(w, h))
            data.append(row)

        with open(f"data/playermade/{file_name}.json", "w") as file:
            json.dump(data, file) 

class ColourInputPopup:
    def __init__(self):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (4, 1)
        self.input_text = ""

        self.showing_colour_input_popup = False

        self.popup_creator = PopupCreator(self.popup_dimensions, self.text_colour, self.popup_colour, self.input_dimensions)


    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Input terminal colour (0-255):"
        self.popup_creator.add_text(text, screen, y=int(dimensions[1]/2) - 3)
        text2 = "Type numbers 0-9, Del to delete"
        self.popup_creator.add_text(text2, screen, y=int(dimensions[1]/2) - 2)
        text3 = "Press Enter again to confirm"
        self.popup_creator.add_text(text3, screen, y=int(dimensions[1]/2) - 1)

        # add input box
        self.popup_creator.show_input_text(screen, termColours.white, self.input_text, self.input_dimensions, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1)

        # add button
        button_text = " Colour diagram (click me!) "
        self.popup_creator.add_button(screen, button_text, x=int((dimensions[0] - len(button_text))/2), y=int(dimensions[1]/2) + 3)

        screen.refresh()
        self.showing_colour_input_popup = True

    def handle_inputs(self, event, screen):
        if 48 <= event.key_code <= 57: # keys 0-9
            self.popup_creator.input_field.edit_input_text(screen, event.key_code, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1, maximum_text_length=3)
            screen.refresh()
        elif event.key_code == -300: # del key
            self.popup_creator.input_field.delete_input_text(screen, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1)
            screen.refresh()

    def check_valid_input(self, screen, pen):
        self.showing_colour_input_popup = self.popup_creator.input_field.check_if_valid(screen, pen, self.popup_creator)



def demo(screen):
    def check_dimensions(screen, dimensions):
        x_pos = 0
        def screen_print(text, colour=Screen.COLOUR_WHITE):
            nonlocal x_pos # inherit from above
            screen.print_at(text, x_pos, 0, colour)
            x_pos += len(str(text))

        screen_print("Please resize the terminaƒl to ")
        screen_print(f"{dimensions[0]}x{dimensions[1]}", Screen.COLOUR_YELLOW)
        screen_print(". Your current size is ")
        screen_print(f"{screen.width}x{screen.height}.", Screen.COLOUR_RED)

        #screen.print_at(f"Please resize to 150x30. Your current size is {screen.width}x{screen.height}.", 0, 0)
        screen.refresh() 
        while not screen.has_resized():
            pass

    mouse_down = None
    mouse_up = None
    global dimensions

    colour_input_popup = ColourInputPopup()
    help_popup = HelpPopup()
    save_popup = SavePopup()
    pen = Pen()
    tool = Tool()

    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=termColours.sky_blue, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        pen.print_pen_colour(screen)
        tool.print_tool_type(screen)
        help_popup.print_help_tip_text(screen)
        screen.refresh()
        while not screen.has_resized(): # if screen is correct size

            event = screen.get_event()
            if isinstance(event, MouseEvent):
                if not colour_input_popup.showing_colour_input_popup and not help_popup.showing_help_popup and not save_popup.showing_save_popup:
                    if tool.tool_type == "pen": # if using pen tool
                        if event.buttons == 0: # mouse up
                            mouse_up = [event.x, event.y]
                        elif event.buttons == 1: # mouse down
                            mouse_down = [event.x, event.y]
                            mouse_up = None

                        if mouse_up and mouse_down:
                            mouse_up[1] = min((dimensions[1] - 2), mouse_up[1]) # make sure can't draw off bottom of screen
                            mouse_down[1] = min((dimensions[1] - 2), mouse_down[1])

                            screen.move(*mouse_down) # * unpacks tuple
                            screen.draw(*mouse_up, char="█", colour=pen.pen_colour, thin=True)

                        if event.y < dimensions[1] - 1: # prevent drawing at bottom of screen
                            screen.print_at("█", event.x, event.y, pen.pen_colour) # print at cursor
                        screen.refresh()
                    else: # if using dropper tool
                        if event.buttons == 1: # mouse down
                            pixel = screen.get_from(event.x, event.y)
                            pen.pen_colour = pixel[1] # get colour from pixel
                            pen.print_pen_colour(screen)
                            screen.refresh()
                elif colour_input_popup.showing_colour_input_popup: # if click on popup button
                    if event.buttons == 1:
                        if event.y == 18 and 61 <= event.x <= 89:
                            webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser
                else:
                    if event.buttons == 1:
                        if event.y == 17 and 67 <= event.x <= 81:
                            save_popup.save_button_clicked(screen)

            elif isinstance(event, KeyboardEvent):
                if colour_input_popup.showing_colour_input_popup:
                    if event.key_code == 10: # enter key to open colour input
                        colour_input_popup.check_valid_input(screen, pen) # check if input is valid
                    else:
                        colour_input_popup.handle_inputs(event, screen)
                    screen.refresh()
                elif help_popup.showing_help_popup:
                    if event.key_code == 104: # h key
                        help_popup.hide_popup(screen)
                elif save_popup.showing_save_popup:
                    if event.key_code == 115: # s key
                        save_popup.hide_popup(screen)
                    else:
                        save_popup.handle_inputs(event, screen)
                else:
                    if event.key_code == 10: # enter key to open colour input
                        colour_input_popup.show_popup(screen)
                    elif event.key_code == 32: # space key
                        tool.change_tool_type()
                        tool.print_tool_type(screen)
                        screen.refresh()
                    elif event.key_code == 104: # h key
                        help_popup.show_popup(screen)
                    elif event.key_code == 115: # s key
                        save_popup.show_popup(screen)

while True:
    Screen.wrapper(demo)