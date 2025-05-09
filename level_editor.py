#NAME: EpicEfeathers
#ASSIGNMENT: Captstone
#PURPOSE: Level editor for my capstone terminal game

from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
import webbrowser
import json
import pygame # for music

from create_colour_list import create_colour_list

from level_scripts.popups.colour_input_popup import ColourInputPopup
from level_scripts.popups.help_popup import HelpPopup
from level_scripts.popups.background_popup import BackgroundPopup
from level_scripts.tool import Tool
from level_scripts.pen import Pen
from level_scripts.popups.save_slot_popup import SaveSlotPopup

from level_scripts.handle_drawing import HandleDrawing
from level_scripts.level_renderer import LevelRenderer

from level_scripts.spawn_point import SpawnPoint
from level_scripts.flag import Flag

from config import termColours, keys

#INPUT: Screen, tuple
#RETURN: None
#PURPOSE: Checks screen dimensions to see if proper
def check_dimensions(screen, dimensions):
    colour_list = create_colour_list(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", [f"{dimensions[0]}x{dimensions[1]}", f"{screen.width}x{screen.height}."], Screen.COLOUR_WHITE, Screen.COLOUR_BLACK, [Screen.COLOUR_YELLOW, Screen.COLOUR_RED])
    screen.paint(f"Please resize the terminal to {dimensions[0]}x{dimensions[1]}. Your current size is {screen.width}x{screen.height}.", 0, 0, colour_map=colour_list)

    screen.refresh() 
    while not screen.has_resized():
        pass

#INPUT: Screen (the terminal instance)
#RETURN: None
#PURPOSE: Main function to run level editor 
def demo(screen):
    dimensions = (150, 31)

    # class instances
    colour_input_popup = ColourInputPopup(dimensions)
    help_popup = HelpPopup(dimensions)
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
        screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1], fg=background_popup.background_colour, attr=Screen.A_NORMAL, bg=termColours.sky_blue)
        save_slot_popup.show_popup(screen)

        while not screen.has_resized(): # if screen is correct size
            if save_slot_popup.showing_save_slot_popup:
                event = screen.get_event()

                if isinstance(event, KeyboardEvent):
                    if event.key_code in [keys.up, keys.down, keys.DEL, keys.q, keys.ESC]:
                        save_slot_popup.handle_input(event.key_code, screen)
                    elif event.key_code == keys.enter:
                        # show help menu at the bottom (if not in save deletion popup)
                        if not save_slot_popup.save_deletion_popup.showing_save_deletion_popup:
                            screen.clear_buffer(x=0, y=dimensions[1]-1, w=dimensions[0], h=1, fg=background_popup.background_colour, attr=Screen.A_NORMAL, bg=termColours.black)
                            pen.print_pen_colour(screen)
                            tool.print_tool_type(screen)
                            help_popup.print_help_tip_text(screen)
                            save_slot_popup.show_saved_state(screen)

                        # open file
                        with open(f"data/playermade/level{save_slot_popup.selected_item}.json", "r") as file:
                            data = json.load(file)
                        background_popup.background_colour = data["background_colour"]
                        save_slot_popup.handle_input(event.key_code, screen, level_renderer, data) # handle input
                        spawn_point = SpawnPoint(data)
                        flag = Flag(data)
                        screen.refresh()

            else:
                # get input events (mouse and keyboard)
                event = screen.get_event()

                # show if currently saved
                if event:
                    save_slot_popup.show_saved_state(screen)
                    save_slot_popup.currently_saved = False

                if isinstance(event, MouseEvent):
                    # drawing
                    if not colour_input_popup.showing_colour_input_popup and not help_popup.showing_help_popup and not background_popup.showing_background_colour_popup: # if no popups open
                        if tool.tool_type == "pen": # if using pen tool
                            handle_drawing.handle_drawing(dimensions, screen, event, pen.pen_colour, character_to_draw="█", screen_background_colour=background_popup.background_colour)

                        elif tool.tool_type == "dropper": # if using dropper tool
                            if event.buttons == 1: # mouse down
                                pixel = screen.get_from(event.x, event.y)
                                if pixel[0] != 32: # if not a background pixel
                                    pen.pen_colour = pixel[1] # get colour from pixel
                                else:
                                    pen.pen_colour = pixel[3] # get background
                                    
                                pen.print_pen_colour(screen)
                                screen.refresh()

                        elif tool.tool_type == "spike": # if adding spikes
                            handle_drawing.handle_drawing(dimensions, screen, event, pen.pen_colour, character_to_draw="▲", underlined=4) # 4 is underlined

                        elif tool.tool_type == "spawn point":
                            spawn_point.change_spawn_point(screen, event, background_popup.background_colour)

                        else: # if using flag tool
                            flag.change_flag_pos(screen, event, background_popup.background_colour)

                    elif colour_input_popup.showing_colour_input_popup or background_popup.showing_background_colour_popup: # if click on popup button
                        if event.buttons == 1:
                            if event.y == 18 and 61 <= event.x <= 89:
                                webbrowser.open('https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg') # open colour diagram in browser
                
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
                    # if change background colour open
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
                        # switch to tool type (pen -> dropper etc)
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
                            save_slot_popup.save_screen(screen, background_popup.background_colour, spawn_point.spawn_point, flag.flag_pos)

                        # if hotkeying to change tool type
                        elif event.key_code in [keys.key_1, keys.key_2, keys.key_3, keys.key_4, keys.key_5]:
                            tool.hotkey_change_tool_type(event.key_code)
                            tool.print_tool_type(screen)
                            screen.refresh()

pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("audio/music/level_editor.mp3")
pygame.mixer.music.play(-1)  # Loop forever

# run it
while True:
    Screen.wrapper(demo)