from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser

from config import termColors

dimensions = (150, 31)

def show_popup(screen):
    popup_colour = termColors.popup_gray
    text_colour = termColors.black
    global dimensions
    popup_dimensions = (40, 7)

    # create rectangle
    start_pos = (int((dimensions[0]-popup_dimensions[0])/2), int((dimensions[1]-popup_dimensions[1])/2))
    top_right = (start_pos[0] + popup_dimensions[0], start_pos[1])
    bottom_left = (start_pos[0], start_pos[1] + popup_dimensions[1])
    bottom_right = (start_pos[0] + popup_dimensions[0], start_pos[1] + popup_dimensions[1])
    screen.fill_polygon([[(start_pos), (top_right), (bottom_right), (bottom_left)]], colour=popup_colour)

    text = "Terminal colour (0-255):"
    screen.print_at(text, int((dimensions[0] - len(text))/2), int(dimensions[1]/2) - 2, text_colour, Screen.A_NORMAL, popup_colour)

    input_dimensions = (4, 1)
    screen.print_at("    ", int((dimensions[0] - input_dimensions[0])/2), int(dimensions[1]/2), text_colour, Screen.A_NORMAL, termColors.white)

    button_text = " Colour diagram (click me!) "
    screen.print_at(button_text, int((dimensions[0] - len(button_text))/2), int(dimensions[1]/2) + 2, text_colour, Screen.A_NORMAL, termColors.white)




def demo(screen):
    def check_dimensions(screen, dimensions):
        x_pos = 0
        def screen_print(text, color=Screen.COLOUR_WHITE):
            nonlocal x_pos # inherit from above
            screen.print_at(text, x_pos, 0, color)
            x_pos += len(str(text))

        screen_print("Please resize the terminal to ")
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

    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=termColors.sky_blue)
        screen.print_at("Current colour: ", 0, dimensions[1] - 1)
        screen.print_at("blue", len("Current colour: "), dimensions[1] - 1, Screen.COLOUR_BLUE)
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
                        screen.draw(*mouse_up, char="█", colour=Screen.COLOUR_BLUE, thin=True)

                    if event.y < dimensions[1] - 1: # prevent drawing at bottom of screen
                        screen.print_at("█", event.x, event.y, Screen.COLOUR_BLUE)
                    screen.refresh()
                else: # if click on button
                    if event.buttons == 1:
                        if event.y == 17 and 61 <= event.x <= 89:
                            webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser

            elif isinstance(event, KeyboardEvent):
                if event.key_code == 10:
                    if showing_popup_screen:
                        showing_popup_screen = False # WORK ON THIS
                    else:
                        show_popup(screen)
                        showing_popup_screen = True
                    screen.refresh()
while True:
    Screen.wrapper(demo)