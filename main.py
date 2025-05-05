#NAME: ***REMOVED***
#ASSIGNMENT: Capstone
#PURPOSE: To create a game using our python skills (terminal-based platformer game, basically a proof-of-concept).

from pynput.keyboard import Listener
from asciimatics.screen import Screen
import time

from scripts.player import Player
from scripts.game_controls import GameControls
from scripts.frame_control import FrameControl
from scripts.render_level import LevelRenderer

RUNNING = True

#INPUT: Screen (the terminal instance), tuple
#RETURN: None
#PURPOSE: Checks screen dimensions to see if proper
def check_dimensions(screen, dimensions):
    global RUNNING
    x_pos = 0

    #INPUT: str, asciimatics colour (int)
    #RETURN: None
    #PURPOSE: Prints to terminal screen, but handles proper x position automatically
    def screen_print(text, color=Screen.COLOUR_WHITE):
        nonlocal x_pos # inherit from above
        screen.print_at(text, x_pos, 0, color)
        x_pos += len(str(text))

    screen_print("Please resize the terminal to ")
    screen_print(f"{dimensions[0]}x{dimensions[1]}", Screen.COLOUR_YELLOW)
    screen_print(". Your current size is ")
    screen_print(f"{screen.width}x{screen.height}.", Screen.COLOUR_RED)

    screen.refresh() 
    while not screen.has_resized() and RUNNING: # if the game has not been resized, don't check
        pass

#INPUT: screen
#RETURN: None
#PURPOSE: Runs the main game
def game(screen):
    global RUNNING
    dimensions = (150, 31)


    #INPUT: Enum
    #RETURN: None
    #PURPOSE: Called when key is pressed, and passes the value on to the game_controls class
    def on_press(key):
        game_controls.keys.add(key)

    #INPUT: Enum
    #RETURN: None
    #PURPOSE: Called when key is released, and passes the value on to the game_controls class
    def on_release(key):
        try:
            game_controls.keys.remove(key)
        except KeyError: # if already been removed
            pass

    # instantiates classes
    player = Player()
    game_controls = GameControls(dimensions)
    frame_control = FrameControl()
    level_renderer = LevelRenderer(player)


    # non-blocking listener for keyboard inputs
    listener = Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()

    # check if right screen size
    if (screen.width, screen.height) != dimensions: # if screen is the incorrect size
        check_dimensions(screen, dimensions)
    else:
        while not screen.has_resized() and RUNNING: # if screen is correct size
            if game_controls.pause_popup.showing_pause_popup: # if showing pause game popup
                game_controls.pause_popup.show_popup(screen)

                game_controls.handle_input(screen, player)
            else:
                # MAIN GAME LOOP
                frame_start = time.time() # start time to calculate delta time

                game_controls.handle_input(screen, player)

                level_renderer.render_level(screen, player, game_controls, frame_control)

                # calculate the time it takes to render this frame
                frame_control.frame_render_time = time.time() - frame_start


                if ((1/60 - frame_control.frame_render_time) > 0):
                    game_controls.time_slept = 1/60 - frame_control.frame_render_time
                    time.sleep(1/60 - frame_control.frame_render_time)
                frame_control.total_frames += 1 # for calculating avg FPS

                # calculate this frames delta time (render time + sleep time)
                frame_control.delta_time = time.time() - frame_start

# run it
while RUNNING:
    Screen.wrapper(game)