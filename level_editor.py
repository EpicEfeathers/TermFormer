from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser

from level_scripts.create_colour_list import create_colour_list

from level_scripts.popups.save_popup import SavePopup
from level_scripts.popups.colour_input_popup import ColourInputPopup
from level_scripts.popups.help_popup import HelpPopup
from level_scripts.tool import Tool
from level_scripts.pen import Pen

from config import termColours

dimensions = (150, 31)


def demo(screen):
    def check_dimensions(screen, dimensions):
        colour_list = create_colour_list(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", [f"{dimensions[0]}x{dimensions[1]}", f"{screen.width}x{screen.height}."], Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, [Screen.COLOUR_YELLOW, Screen.COLOUR_RED])
        screen.paint(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", 0, 0, colour_map=colour_list)

        screen.refresh() 
        while not screen.has_resized():
            pass

    mouse_down = None
    mouse_up = None
    global dimensions

    colour_input_popup = ColourInputPopup(dimensions)
    help_popup = HelpPopup(dimensions)
    save_popup = SavePopup(dimensions)
    pen = Pen(dimensions)
    tool = Tool(dimensions)

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