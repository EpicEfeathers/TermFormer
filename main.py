from pynput.keyboard import Listener, Key, KeyCode
from asciimatics.screen import Screen
import time
import random

class FrameControl:
    def __init__(self):
        self.delta_time = 0.00000000001 # small number so no divide by 0 error when starting program
        self.start_timestamp = time.time()
        self.total_frames = 1

class GameControls:
    def __init__(self):
        self.running = True
        self.debug_screen = True
        self.debug_screen_height = 8

    def toggle_debug_screen(self, screen):
        self.debug_screen = not self.debug_screen
        screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=30, h=self.debug_screen_height)

    def write_debug_screen(self, screen, player, frame_control):
        if self.debug_screen:
            self.current_line = 0

            # function for printing debug statements easier
            def print_debug_line(text, colour=Screen.COLOUR_WHITE):
                screen.print_at(text, 0, self.current_line, colour)
                self.current_line += 1

            screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=40, h=self.debug_screen_height)

            print_debug_line(f"FPS: {round(1/frame_control.delta_time)}")

            time_since_start = time.time() - frame_control.start_timestamp
            print_debug_line(f"Avg FPS: {round(1 / (time_since_start / frame_control.total_frames))}")
            print_debug_line(f"Delta Time: {frame_control.delta_time}")

            print_debug_line(f"Y: {"{:.3f}".format(round(player.y, 3))}", Screen.COLOUR_GREEN)
            print_debug_line(f"Y velo: {"{:.3f}".format(round(player.y_velo, 3))}", Screen.COLOUR_GREEN)
            print_debug_line(f"Screen height: {screen.height}", Screen.COLOUR_GREEN)
            print_debug_line(f"Jumping: {player.jumping}", Screen.COLOUR_GREEN)

            print_debug_line(f"Tiles: {player.get_tiles_surrounding(screen)}", Screen.COLOUR_BLUE)
            #screen.print_at(f"Tile beneath: {player.get_tile_beneath(screen)}", 0, 6, Screen.COLOUR_BLUE)
            #screen.print_at(f"Tile above: {player.get_tile_above(screen)}", 0, 7, Screen.COLOUR_BLUE)



class Player:
    def __init__(self, screen_width, screen_height): # initializing all player variables
        self.jumping = 0

        self.x = int(screen_width / 2)
        self.y = 1
        self.x_velo = 0
        self.y_velo = 0
        #self.movement_speed_x = 0.01
        self.movement_speed_x = 20

        self.old_x = self.x
        self.old_y = self.y

        #self.gravity = 0.00003
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


    def udpate_position(self, screen, DELTA_TIME):
        self.jumping += 1

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
        if tile_beneath is not None and tile_beneath[0] == 9608 and self.jumping > 0: # if tile underneath is block
            #self.y -= 1
            self.y_velo = 0
            self.jumping = 0
        elif tile_above is not None and tile_above[0] == 9608 and self.y_velo < 0:
            #da a      self.y += 1
            self.y_velo = 0
        else:
            self.y += self.y_velo * DELTA_TIME

        # stop flowing off screen
        if self.y > screen.height:
            self.y = screen.height - 1
            self.y_velo = 0
            self.jumping = 0
        elif self.y < 0:
            self.y = 0
        
        if self.x < 0:
            self.x = 0
        elif self.x > screen.width:
            self.x = screen.width - 1


def demo(screen):
    # on key press
    def on_press(key):
        # movement
        if key == KeyCode(char="a"): # move horizontally
            player.x_velo = -1
        elif key == KeyCode(char="d"):
            player.x_velo = 1
        elif (key == Key.space) or (key == KeyCode(char="w")): # jump
            tile_beneath = player.get_tile_beneath(screen)
            if (tile_beneath is not None and tile_beneath[0] == 9608) and player.jumping == 0:#or (player.y > screen.height - 1):
            #if player.y > screen.height - 1:
                #player.y_velo = -0.02
                player.jumping = -1 # need this because the listener is called first, and always reset the velo
                player.y_velo = -50 # jump strength
        elif (key==KeyCode(char="s")):
            player.y = 1

        # other
        elif key == KeyCode(char="t"): # toggle debug screen on / off
            game_controls.toggle_debug_screen(screen)
        if key == Key.esc: # stop program
            game_controls.running = False

    # on key release
    def on_release(key):
        if key == KeyCode(char="a") or key == KeyCode(char="d"): # reset x_velo if key released
            player.x_velo = 0


    player = Player(screen.width, screen.height)
    game_controls = GameControls()
    frame_control = FrameControl()

    # non-blocking listener for keyboard inputs
    listener = Listener(on_press=on_press,on_release=on_release)
    listener.start()
    #screen.print_at("█████████████████████", int(screen.width/2 - 8), random.randint(screen.height - 10, screen.height - 3))
    for i in range(10):
        screen.print_at("█", int(screen.width/2 - i), screen.height - i)

    for w in range(screen.width): # for some reason, much faster than drawing a line using https://asciimatics.readthedocs.io/en/stable/io.html#drawing-shapes
            screen.print_at("█", w, screen.height-1)

    while game_controls.running:
        start = time.time() # start time to calculate delta time

        player.udpate_position(screen, frame_control.delta_time)

        #screen = draw_player(screen, p)
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD)

        for w in range(screen.width): # for some reason, much faster than drawing a line using https://asciimatics.readthedocs.io/en/stable/io.html#drawing-shapes
            screen.print_at("█", w, screen.height-1)

        # instead of clearing entire screen, check if player has moved and clear that position
        if (int(player.old_x) != int(player.x)) or (int(player.old_y) != int(player.y)):
            screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=int(player.old_x), y=int(player.old_y), w=1, h=1)        

        game_controls.write_debug_screen(screen, player, frame_control)

        # refresh the display
        screen.refresh()

        #if (1/60 - frame_control.delta_time > 0):
         #   time.sleep(1/60 - frame_control.delta_time)

        # calculate delta time
        frame_control.delta_time = time.time() - start
        frame_control.total_frames += 1



Screen.wrapper(demo)