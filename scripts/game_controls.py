from pynput.keyboard import Key, KeyCode
from asciimatics.screen import Screen
import time

from config import termColours
from scripts.popups.pause_popup import PausePopup
from scripts.popups.main_menu_popup import MainMenu

# handles all game controlling type stuff (input, debug screen, etc.), other than rendering
class GameControls:
    def __init__(self, dimensions, level_renderer):
        self.debug_screen = False
        self.debug_screen_height = 19

        self.running = True

        self.keys = set()

        self.time_slept = 0

        self.pause_key_held = False
        self.pause_popup = PausePopup(dimensions)
        
        self.main_menu = MainMenu(dimensions, self)
        self.level_renderer = level_renderer

    #INPUT: screen (asciimatics class), player: class
    #RETURN: None
    #PURPOSE: Handles user input
    def handle_input(self, screen, player):
        if self.main_menu.main_menu: # if showing main menu, let that class handle user input
            self.main_menu.handle_inputs(screen, self.keys)
        
        else:
            if KeyCode(char="a") in self.keys: # move horizontally
                player.x_velo = -1

            if KeyCode(char="d") in self.keys:
                player.x_velo = 1
            
            if KeyCode(char="a") not in self.keys and KeyCode(char="d") not in self.keys: # if neither pressed
                player.x_velo = 0
            if (Key.space in self.keys) or (KeyCode(char="w") in self.keys): # jump
                tile_beneath = player.get_tiles_surrounding(screen)["down"]
                if (tile_beneath is not None and tile_beneath[0] == 9608 and player.y_velo >= 0): # make sure only can jump when on ground and not already going up
                    player.y_velo = -50 # jump strength
            elif KeyCode(char="s") in self.keys:
                player.y = 1

            # other
            if KeyCode(char="t") in self.keys: # toggle debug screen on / off
                self.toggle_debug_screen()
                self.keys.remove(KeyCode(char="t"))

            if (Key.esc in self.keys) or (KeyCode(char="q") in self.keys): # pause program
                if not self.pause_key_held:
                    self.pause_popup.showing_pause_popup = not self.pause_popup.showing_pause_popup # toggle
                self.pause_key_held = True

    #INPUT: None
    #RETURN: None
    #PURPOSE: Toggles the debug_screen class variable (whether debug screen showing)
    def toggle_debug_screen(self):
        self.debug_screen = not self.debug_screen

    #INPUT: screen (asciimatics class), player: class, frame_control: class, background_colour: int
    #RETURN: None
    #PURPOSE: Shows the popup on the screen
    def write_debug_screen(self, screen, player, frame_control, background_colour: int):
        if self.debug_screen:
            self.current_line_left = 0
            self.current_line_right = 0

            #INPUT: text: str, position: str, colour: int
            #RETURN: None
            #PURPOSE: Makes printing debug statements easier (remembers the line)
            def print_debug_line(text:str, position:str, colour:int = termColours.white): # 15 = white
                if position == "left":
                    screen.print_at(text, 0, self.current_line_left, colour, Screen.A_NORMAL, background_colour)
                    self.current_line_left += 1
                else:
                    screen.print_at(text, screen.width - len(text), self.current_line_right, colour, Screen.A_NORMAL, background_colour)
                    self.current_line_right += 1

            print_debug_line(f"FPS: {round(1/frame_control.delta_time)}", "left")

            time_since_start = time.time() - frame_control.start_timestamp
            print_debug_line(f"Avg FPS: {round(1 / (time_since_start / frame_control.total_frames))}", "left")
            print_debug_line(f"Delta Time: {"{:.4f}".format(frame_control.delta_time)}", "left")
            print_debug_line(f"FPS if uncapped: {round(1/frame_control.frame_render_time)}", "left")

            print_debug_line(f"XY: {"{:.3f}".format(round(player.x, 3))} {"{:.3f}".format(round(player.y, 3))}", "left", termColours.light_green) # 154 is light green
            print_debug_line(f"X velo: {"{:.3f}".format(round(player.x_velo, 3))}", "left", termColours.light_green)
            print_debug_line(f"Y velo: {"{:.3f}".format(round(player.y_velo, 3))}", "left", termColours.light_green)

            print_debug_line(f"Tiles: {player.get_tiles_surrounding(screen)}", "right", Screen.COLOUR_BLUE)
            
            print_debug_line(f"Keys: {self.keys}", "right", termColours.yellow)

            print_debug_line(f"Sleep time: {"{:.3f}".format(self.time_slept)}", "right", termColours.yellow)