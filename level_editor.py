from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser

from config import termColours, keyboard_event_number_conversion

dimensions = (150, 31)

class Help:
    def __init__(self):
        self.showing_help_screen = False



    def print_help_tip_text(self, screen):
        global dimensions
        text = "Press H for help"
        #text = "|Click or drag to draw |Press S to save | Press Enter to change colour | Press Space to change tool"

        position = (int((dimensions[0] - len(text))/2), dimensions[1] - 1)
        screen.print_at(text, *position)


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

        text = "Tool: "
        screen.print_at(f"{text}{self.tool_type.capitalize()}", dimensions[0] - len(self.tool_type) - len(text), dimensions[1] - 1)


class PopupCreator:
    def __init__(self, popup_dimensions, text_colour, popup_colour):
        self.popup_dimensions = popup_dimensions
        self.text_colour = text_colour
        self.popup_colour  = popup_colour
        self.input_field = InputField(input_dimensions=(4, 1), text_colour=self.text_colour, background_colour=termColours.white)

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

    def add_text(self, text, screen, x, y):
        screen.print_at(text, x, y, self.text_colour, Screen.A_NORMAL, self.popup_colour)

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

    def show_input_text(self, screen, x, y, background_colour=None):
        if not background_colour: # if not specified, set to predefined
            background_colour = self.background_colour

        input_text = self.input_text + (" " * (self.input_dimensions[0] - len(self.input_text)))
        screen.print_at(input_text, x, y, self.text_colour, Screen.A_NORMAL, background_colour)

    def edit_input_text(self, screen, digit):
        if len(self.input_text) <= 2:
            self.input_text += str(keyboard_event_number_conversion[digit])
            
            self.show_input_text(screen, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1)

    def delete_input_text(self, screen):
        if len(self.input_text) >= 1:
            self.input_text = self.input_text[:-1]
            
            self.show_input_text(screen, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1)

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


class ColourInputPopup:
    def __init__(self):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (4, 1)
        self.input_text = ""

        self.popup_creator = PopupCreator(self.popup_dimensions, self.text_colour, self.popup_colour)


    def show_popup(self, screen):
        self.popup_creator.save_under_popup(screen)
        # create rectangle
        self.popup_creator.create_background(screen)

        # add text
        text = "Input terminal colour (0-255):"
        self.popup_creator.add_text(text, screen, x=int((dimensions[0] - len(text))/2), y=int(dimensions[1]/2) - 3)
        text2 = "Type numbers 0-9, Del to delete"
        self.popup_creator.add_text(text2, screen, x=int((dimensions[0] - len(text2))/2), y=int(dimensions[1]/2) - 2)
        text3 = "Press Enter again to confirm"
        self.popup_creator.add_text(text3, screen, x=int((dimensions[0] - len(text3))/2), y=int(dimensions[1]/2) - 1)

        # add input box
        self.popup_creator.show_input_text(screen, termColours.white, self.input_text, self.input_dimensions, x=int((dimensions[0] - self.input_dimensions[0])/2), y=int(dimensions[1]/2) + 1)

        # add button
        button_text = " Colour diagram (click me!) "
        self.popup_creator.add_button(screen, button_text, x=int((dimensions[0] - len(button_text))/2), y=int(dimensions[1]/2) + 3)

    def handle_inputs(self, event, screen):
        if 48 <= event.key_code <= 57: # keys 0-9
            self.popup_creator.input_field.edit_input_text(screen, event.key_code)
            screen.refresh()
        elif event.key_code == -300: # del key
            self.popup_creator.input_field.delete_input_text(screen)
            screen.refresh()

    def check_valid_input(self, screen, pen):
        return self.popup_creator.input_field.check_if_valid(screen, pen, self.popup_creator)



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
    showing_popup_screen = False

    colour_input_popup = ColourInputPopup()
    pen = Pen()
    tool = Tool()
    help = Help()

    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=termColours.sky_blue, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        pen.print_pen_colour(screen)
        tool.print_tool_type(screen)
        help.print_help_tip_text(screen)
        screen.refresh()
        while not screen.has_resized(): # if screen is correct size

            event = screen.get_event()
            if isinstance(event, MouseEvent):
                if not showing_popup_screen:
                    if tool.tool_type == "pen": # if using pen tool
                        if event.buttons == 0: # mouse up
                            mouse_up = [event.x, event.y]
                        elif event.buttons == 1: # mouse down
                            mouse_down = [event.x, event.y]
                            mouse_up = None

                        #screen.print_at(mouse_down, 0, 0)
                        #screen.print_at(mouse_up, 0, 1)

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
                else: # if click on popup button
                    if event.buttons == 1:
                        if event.y == 18 and 61 <= event.x <= 89:
                            webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser

            elif isinstance(event, KeyboardEvent):
                if event.key_code == 10: # enter key to open colour input
                    if showing_popup_screen:
                        showing_popup_screen = colour_input_popup.check_valid_input(screen, pen) # check if input is valid
                    else:
                        colour_input_popup.show_popup(screen)
                        showing_popup_screen = True
                    screen.refresh()
                else:
                    if showing_popup_screen:
                        colour_input_popup.handle_inputs(event, screen)
                    else:
                        if event.key_code == 32: # space key
                            tool.change_tool_type()
                            tool.print_tool_type(screen)
                            screen.refresh()
while True:
    Screen.wrapper(demo)