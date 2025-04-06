from pynput.keyboard import Listener, Key, KeyCode
from asciimatics.screen import Screen
import time
import random

class FrameControl:
    def __init__(self):
        self.delta_time = 0.00000000001 # small number so no divide by 0 error when starting program
        self.start_timestamp = time.time()
        self.total_frames = 1
        self.frame_render_time = 0

        self.fps = 0

class GameControls:
    def __init__(self):
        self.running = True
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
            tile_beneath = player.get_tile_beneath(screen)
            if (tile_beneath is not None and tile_beneath[0] == 9608 and player.y_velo >= 0): # make sure only can jump when on ground and not already going up
                player.y_velo = -50 # jump strength
        elif KeyCode(char="s") in self.keys:
            player.y = 1

        # other
        if KeyCode(char="t") in self.keys: # toggle debug screen on / off
            self.toggle_debug_screen(screen)
            self.keys.remove(KeyCode(char="t"))
        if Key.esc in self.keys: # stop program
            self.running = False


    def toggle_debug_screen(self, screen):
        self.debug_screen = not self.debug_screen
        #screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=60, h=self.debug_screen_height)

    def write_debug_screen(self, screen, player, frame_control):
        if self.debug_screen:
            self.current_line_left = 0
            self.current_line_right = 0

            # function for printing debug statements easier
            def print_debug_line(text, position, colour=Screen.COLOUR_WHITE):
                if position == "left":
                    screen.print_at(text, 0, self.current_line_left, colour)
                    self.current_line_left += 1
                else:
                    screen.print_at(text, screen.width - len(text), self.current_line_right, colour)
                    self.current_line_right += 1

            #screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=40, h=self.debug_screen_height)

            print_debug_line(f"FPS: {round(1/frame_control.delta_time)}", "left")

            time_since_start = time.time() - frame_control.start_timestamp
            print_debug_line(f"Avg FPS: {round(1 / (time_since_start / frame_control.total_frames))}", "left")
            print_debug_line(f"Delta Time: {"{:.4f}".format(frame_control.delta_time)}", "left")

            print_debug_line(f"XY: {"{:.3f}".format(round(player.y, 3))} {"{:.3f}".format(round(player.x, 3))}", "left", Screen.COLOUR_GREEN)
            print_debug_line(f"Y velo: {"{:.3f}".format(round(player.y_velo, 3))}", "left", Screen.COLOUR_GREEN)
            print_debug_line(f"Screen height: {screen.height}", "left", Screen.COLOUR_GREEN)

            print_debug_line(f"Tiles: {player.get_tiles_surrounding(screen)}", "right", Screen.COLOUR_BLUE)
            
            print_debug_line(f"Keys: {self.keys}", "right", Screen.COLOUR_YELLOW)

            print_debug_line(f"Sleep time: {"{:.3f}".format(self.time_slept)}", "right", Screen.COLOUR_YELLOW)

    def render_frame(self, screen, player, frame_control):
        screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer

        for i in range(10):
            screen.print_at("█", int(screen.width/2) - 5 + i, screen.height-i) # for some reason, much faster than drawing a line using https://asciimatics.readthedocs.io/en/stable/io.html#drawing-shapest
        screen.print_at("█" * screen.width, 0, screen.height-1) # for some reason, much faster than drawing a line using https://asciimatics.readthedocs.io/en/stable/io.html#drawing-shapest

        self.write_debug_screen(screen, player, frame_control)#, game_controls)

        player.update_position(screen, self, frame_control.delta_time)

        #screen = draw_player(screen, p)
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD)

        # refresh the display
        screen.refresh()



class Player:
    def __init__(self, screen_width, screen_height): # initializing all player variables
        self.x = int(screen_width / 2)
        self.y = 1
        self.x_velo = 0
        self.y_velo = 0
        self.movement_speed_x = 20

        self.old_x = self.x
        self.old_y = self.y

        self.gravity = 200
        
        self.tile_beneath = None

    def get_tiles_surrounding(self, screen):
        surrounding = {
            "left": screen.get_from(int(self.x - 1), int(self.y)), 
            "up": screen.get_from(int(self.x), int(self.y - 1)), 
            "right": screen.get_from(int(self.x + 1), int(self.y)), 
            "down": screen.get_from(int(self.x), int(self.y + 1))
        }
        return surrounding

    def get_tile_beneath(self, screen):
        return screen.get_from(int(self.x), int(self.y + 1))
    
    def get_tile_above(self, screen):
        return screen.get_from(int(self.x), int(self.y - 1))


    def update_position(self, screen, game_controls, DELTA_TIME):
        # old position to check if moved
        self.old_x = self.x
        self.old_y = self.y

        # x axis movement
        self.x += self.x_velo * self.movement_speed_x * DELTA_TIME

        # y axis movement
        self.y_velo += self.gravity * DELTA_TIME

        # check tiles above and beneath to see if valid
        tile_beneath = self.get_tile_beneath(screen)
        tile_above = self.get_tile_above(screen)
        if tile_beneath is not None and tile_beneath[0] == 9608 and ((Key.space not in game_controls.keys) and (KeyCode(char="w") not in game_controls.keys)): # if tile underneath is block
            self.y_velo = 0
        elif tile_above is not None and tile_above[0] == 9608 and self.y_velo < 0:
            #da a      self.y += 1
            self.y_velo = 0
        else:
            self.y += self.y_velo * DELTA_TIME

        # stop flowing off screen
        if self.y > screen.height:
            self.y = screen.height - 1
            self.y_velo = 0
        elif self.y < 0:
            self.y = 0
        
        if self.x < 0:
            self.x = 0
        elif self.x > screen.width:
            self.x = screen.width - 1



def game(screen):
    # on key press
    def on_press(key):
        game_controls.keys.add(key)

    # on key release
    def on_release(key):
        try:
            game_controls.keys.remove(key)
        except KeyError: # if already been removed (say to prevent key being held down indefinitely)
            pass


    player = Player(screen.width, screen.height)
    game_controls = GameControls()
    frame_control = FrameControl()

    # non-blocking listener for keyboard inputs
    listener = Listener(on_press=on_press,on_release=on_release)
    listener.start()
    for i in range(10):
        screen.print_at("█", int(screen.width/2 - i), screen.height - i)

    # game loop
    while game_controls.running:
        frame_start = time.time() # start time to calculate delta time

        game_controls.handle_input(screen, player)

        game_controls.render_frame(screen, player, frame_control)

        # calculate delta time
        frame_control.frame_render_time = time.time() - frame_start


        if ((1/60 - frame_control.frame_render_time) > 0):
            game_controls.time_slept = 1/60 - frame_control.frame_render_time
            time.sleep(1/60 - frame_control.frame_render_time)
        frame_control.total_frames += 1 # for calculating avg FPS


        frame_control.delta_time = time.time() - frame_start



Screen.wrapper(game)