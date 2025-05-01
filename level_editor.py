from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser
from datetime import datetime
import json

from level_scripts.create_colour_list import create_colour_list

from level_scripts.popups.save_popup import SavePopup
from level_scripts.popups.colour_input_popup import ColourInputPopup
from level_scripts.popups.help_popup import HelpPopup
from level_scripts.popups.background_popup import BackgroundPopup
from level_scripts.tool import Tool
from level_scripts.pen import Pen
from level_scripts.popups.save_slot_popup import SaveSlotPopup

from level_scripts.handle_drawing import HandleDrawing
from level_scripts.open_file import LevelRenderer

from config import termColours, keys

dimensions = (150, 31)


def demo(screen):
    def check_dimensions(screen, dimensions):
        colour_list = create_colour_list(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", [f"{dimensions[0]}x{dimensions[1]}", f"{screen.width}x{screen.height}."], Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, [Screen.COLOUR_YELLOW, Screen.COLOUR_RED])
        screen.paint(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", 0, 0, colour_map=colour_list)

        screen.refresh() 
        while not screen.has_resized():
            pass

    global dimensions

    # class instances
    colour_input_popup = ColourInputPopup(dimensions)
    help_popup = HelpPopup(dimensions)
    save_popup = SavePopup(dimensions)
    background_popup = BackgroundPopup(dimensions)
    pen = Pen(dimensions)
    tool = Tool(dimensions)

    save_slot_popup = SaveSlotPopup(dimensions)

    handle_drawing = HandleDrawing()
    level_renderer = LevelRenderer()


    # checking screen dimensions
    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        # set up the screen
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=background_popup.background_colour, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        pen.print_pen_colour(screen)
        tool.print_tool_type(screen)
        help_popup.print_help_tip_text(screen)
        save_slot_popup.show_popup(screen)

        screen.refresh()


        while not screen.has_resized(): # if screen is correct size
            if save_slot_popup.showing_save_slot_popup:
                event = screen.get_event()

                if isinstance(event, KeyboardEvent):
                    if event.key_code == keys.enter:
                        level_renderer.render_level(dimensions, save_slot_popup.selected_item, screen) # render level

                        save_slot_popup.showing_save_slot_popup = False
                    elif event.key_code == keys.up or event.key_code == keys.down:
                        save_slot_popup.handle_arrow_keys(event.key_code, screen)
            else:
                # get input events (mouse and keyboard)
                event = screen.get_event()
                if isinstance(event, MouseEvent):
                    # drawing
                    if not colour_input_popup.showing_colour_input_popup and not help_popup.showing_help_popup and not save_popup.showing_save_popup and not background_popup.showing_background_colour_popup: # if no popups open
                        if tool.tool_type == "pen": # if using pen tool
                            handle_drawing.handle_drawing(dimensions, screen, event, pen.pen_colour, character_to_draw="█", screen_background_colour=background_popup.background_colour)

                        elif tool.tool_type == "dropper": # if using dropper tool
                            if event.buttons == 1: # mouse down
                                pixel = screen.get_from(event.x, event.y)
                                pen.pen_colour = pixel[1] # get colour from pixel
                                pen.print_pen_colour(screen)
                                screen.refresh()

                        elif tool.tool_type == "spike": # if adding spikes
                            handle_drawing.handle_drawing(dimensions, screen, event, pen.pen_colour, character_to_draw="▲", underlined=4) # 4 is underlined

                    elif colour_input_popup.showing_colour_input_popup or background_popup.showing_background_colour_popup: # if click on popup button
                        if event.buttons == 1:
                            if event.y == 18 and 61 <= event.x <= 89:
                                webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser
                    else:
                        if event.buttons == 1:
                            if event.y == 17 and 67 <= event.x <= 81:
                                save_popup.save_button_clicked(screen)
                
                # keyboard events
                elif isinstance(event, KeyboardEvent):
                    # if colour input open
                    if colour_input_popup.showing_colour_input_popup:
                        if event.key_code == keys.enter: # enter key
                            colour_input_popup.check_valid_input(screen, pen) # check if input is valid
                        elif event.key_code == keys.ESC: # ESC key
                            colour_input_popup.hide_popup(screen)
                        else:
                            colour_input_popup.handle_inputs(event, screen)
                        screen.refresh()
                    # if help popup open
                    elif help_popup.showing_help_popup:
                        if event.key_code == keys.h or event.key_code == keys.ESC: # h key or ESC
                            help_popup.hide_popup(screen)
                    # if save popup up
                    elif save_popup.showing_save_popup:
                        if event.key_code == keys.s or event.key_code == keys.ESC: # s key or ESC
                            save_popup.hide_popup(screen)
                        else:
                            save_popup.handle_inputs(event, screen)
                    elif background_popup.showing_background_colour_popup:
                        if event.key_code == keys.enter: # enter key
                            background_popup.check_valid_input(screen)
                        if event.key_code == keys.b or event.key_code == keys.ESC: # b key or ESC
                            background_popup.hide_popup(screen)
                        else:
                            background_popup.handle_inputs(event, screen)

                    # else
                    else:
                        # show colour input popup
                        if event.key_code == keys.enter: # enter key to open colour input
                            colour_input_popup.show_popup(screen)
                        # switch to tool type (pen <-> dropper)
                        elif event.key_code == keys.space: # space key
                            tool.change_tool_type()
                            tool.print_tool_type(screen)
                            screen.refresh()
                        elif event.key_code == keys.b:
                            background_popup.show_popup(screen)
                            #change_bg_colour(dimensions, screen)
                        # show help popup
                        elif event.key_code == keys.h: # h key
                            help_popup.show_popup(screen)
                        # show save popup menu
                        elif event.key_code == keys.s: # s key
                            save_slot_popup.save_screen(screen)

while True:
    Screen.wrapper(demo)