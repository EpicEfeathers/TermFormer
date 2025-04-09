from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser

from config import termColours, keyboard_event_number_conversion

dimensions = (150, 31)

class Pen:
    def __init__(self):
        self.pen_colour = termColours.white

class PopupScreen:
    def __init__(self):
        self.popup_dimensions = (40, 9)
        self.dimensions = dimensions
        self.popup_colour = termColours.popup_gray
        self.text_colour = termColours.black

        self.input_dimensions = (4, 1)
        self.input_text = ""


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
        top_left = (int((dimensions[0]-self.popup_dimensions[0])/2), int((dimensions[1]-self.popup_dimensions[1])/2))

        screen.clear_buffer(x=top_left[0], y=top_left[1], w=self.popup_dimensions[0], h=self.popup_dimensions[1], fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        
        # recreate every pixel covered by the popup
        i = 0
        for h in range(self.popup_dimensions[1]):
            for w in range(self.popup_dimensions[0]):
                screen.print_at(self.saved_pixels[i], 0, 0)
                screen.print_at(chr(self.saved_pixels[i][0]), top_left[0] + w, top_left[1] + h, self.saved_pixels[i][1], self.saved_pixels[i][2], self.saved_pixels[i][3]) # char converts ASCII number (e.g. 32) to it's character (e.g. " ")
                i += 1

    def show_input_text(self, screen):
        input_text = self.input_text + (" " * (4 - len(self.input_text)))
        screen.print_at(input_text, int((dimensions[0] - self.input_dimensions[0])/2), int(dimensions[1]/2) + 1, self.text_colour, Screen.A_NORMAL, termColours.white)

    def show_popup(self, screen):
        # create rectangle
        start_pos = (int((dimensions[0]-self.popup_dimensions[0])/2), int((dimensions[1]-self.popup_dimensions[1])/2))
        top_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1])
        bottom_left = (start_pos[0], start_pos[1] + self.popup_dimensions[1])
        bottom_right = (start_pos[0] + self.popup_dimensions[0], start_pos[1] + self.popup_dimensions[1])
        screen.fill_polygon([[(start_pos), (top_right), (bottom_right), (bottom_left)]], colour=self.popup_colour)

        # add text
        text = "Input terminal colour (0-255):"
        screen.print_at(text, int((dimensions[0] - len(text))/2), int(dimensions[1]/2) - 3, self.text_colour, Screen.A_NORMAL, self.popup_colour)
        text2 = "Type numbers 0-9, Del to delete"
        screen.print_at(text2, int((dimensions[0] - len(text2))/2), int(dimensions[1]/2) - 2, self.text_colour, Screen.A_NORMAL, self.popup_colour)
        text3 = "Press Enter again to confirm"
        screen.print_at(text3, int((dimensions[0] - len(text3))/2), int(dimensions[1]/2) - 1, self.text_colour, Screen.A_NORMAL, self.popup_colour)

        # add input box
        self.show_input_text(screen)

        # add button
        button_text = " Colour diagram (click me!) "
        screen.print_at(button_text, int((dimensions[0] - len(button_text))/2), int(dimensions[1]/2) + 3, self.text_colour, Screen.A_NORMAL, termColours.white)

    def edit_popup_text(self, screen, digit):
        if len(self.input_text) <= 2:
            self.input_text += str(keyboard_event_number_conversion[digit])
            
            self.show_input_text(screen)

    def delete_popup_text(self, screen):
        if len(self.input_text) >= 1:
            self.input_text = self.input_text[:-1]
            
            self.show_input_text(screen)

    def check_if_valid(self, screen, pen):
        if 0 <= int(self.input_text) <= 255:
            pen.pen_colour = int(self.input_text)

            screen.print_at("Current pen colour: ", 0, dimensions[1] - 1)
            screen.print_at("████", len("Current pen colour: "), dimensions[1] - 1, pen.pen_colour)
            screen.refresh()




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

    popup = PopupScreen()
    pen = Pen()

    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        screen.print_at("Current pen colour: ", 0, dimensions[1] - 1)
        screen.print_at("████", len("Current pen colour: "), dimensions[1] - 1, pen.pen_colour)
        screen.refresh()
        while not screen.has_resized(): # if screen is correct size

            event = screen.get_event()
            if isinstance(event, MouseEvent):
                if not showing_popup_screen:
                    if event.buttons == 0: # mouse up
                        mouse_up = [event.x, event.y]
                    elif event.buttons == 1: # mouse down
                        mouse_down = [event.x, event.y]
                        mouse_up = None

                    screen.print_at(mouse_down, 0, 0)
                    screen.print_at(mouse_up, 0, 1)

                    if mouse_up and mouse_down:
                        mouse_up[1] = min((dimensions[1] - 2), mouse_up[1]) # make sure can't draw off bottom of screen
                        mouse_down[1] = min((dimensions[1] - 2), mouse_down[1])

                        screen.move(*mouse_down) # * unpacks tuple
                        screen.draw(*mouse_up, char="█", colour=pen.pen_colour, thin=True)

                    if event.y < dimensions[1] - 1: # prevent drawing at bottom of screen
                        screen.print_at("█", event.x, event.y, pen.pen_colour) # print at cursor
                    screen.refresh()
                else: # if click on button
                    if event.buttons == 1:
                        if event.y == 18 and 61 <= event.x <= 89:
                            webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser

            elif isinstance(event, KeyboardEvent):
                if event.key_code == 10:
                    if showing_popup_screen:
                        showing_popup_screen = False # WORK ON THIS
                        popup.check_if_valid(screen, pen)
                        popup.recreate_under_popup(screen)
                    else:
                        popup.save_under_popup(screen)
                        popup.show_popup(screen)
                        showing_popup_screen = True
                    screen.refresh()
                else:
                    if showing_popup_screen:
                        if 48 <= event.key_code <= 57:
                            popup.edit_popup_text(screen, event.key_code)
                            screen.refresh()
                        elif event.key_code == -300:
                            popup.delete_popup_text(screen)
                            screen.refresh()
while True:
    Screen.wrapper(demo)