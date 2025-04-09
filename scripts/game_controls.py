from pynput.keyboard import Key, KeyCode
from asciimatics.screen import Screen
import time
from config import termColours

class GameControls:
    global RUNNING
    def __init__(self):
        self.debug_screen = True
        self.debug_screen_height = 19

        self.keys = set()

        self.time_slept = 0

    def handle_input(self, screen, player):
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
            self.toggle_debug_screen(screen)
            self.keys.remove(KeyCode(char="t"))
        if Key.esc in self.keys: # stop program
            global RUNNING
            RUNNING = False


    def toggle_debug_screen(self, screen):
        self.debug_screen = not self.debug_screen
        #screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=60, h=self.debug_screen_height)

    def write_debug_screen(self, screen, player, frame_control, background_color):
        if self.debug_screen:
            self.current_line_left = 0
            self.current_line_right = 0

            # function for printing debug statements easier
            def print_debug_line(text, position, colour=termColours.white): # 15 = white
                if position == "left":
                    screen.print_at(text, 0, self.current_line_left, colour, Screen.A_NORMAL, background_color)
                    self.current_line_left += 1
                else:
                    screen.print_at(text, screen.width - len(text), self.current_line_right, colour, Screen.A_NORMAL, background_color)
                    self.current_line_right += 1

            #screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=40, h=self.debug_screen_height)

            print_debug_line(f"FPS: {round(1/frame_control.delta_time)}", "left")

            time_since_start = time.time() - frame_control.start_timestamp
            print_debug_line(f"Avg FPS: {round(1 / (time_since_start / frame_control.total_frames))}", "left")
            print_debug_line(f"Delta Time: {"{:.4f}".format(frame_control.delta_time)}", "left")
            print_debug_line(f"FPS if uncapped: {round(1/frame_control.frame_render_time)}", "left")

            print_debug_line(f"XY: {"{:.3f}".format(round(player.y, 3))} {"{:.3f}".format(round(player.x, 3))}", "left", termColours.light_green) # 154 is light green
            print_debug_line(f"X velo: {"{:.3f}".format(round(player.x_velo, 3))}", "left", termColours.light_green)
            print_debug_line(f"Y velo: {"{:.3f}".format(round(player.y_velo, 3))}", "left", termColours.light_green)
            #print_debug_line(f"Running: {RUNNING}", "left", Screen.COLOUR_CYAN)

            print_debug_line(f"Tiles: {player.get_tiles_surrounding(screen)}", "right", Screen.COLOUR_BLUE)
            
            print_debug_line(f"Keys: {self.keys}", "right", termColours.yellow)

            print_debug_line(f"Sleep time: {"{:.3f}".format(self.time_slept)}", "right", termColours.yellow)