from pynput.keyboard import Listener
from asciimatics.screen import Screen
import time

from scripts.player import Player
from scripts.game_controls import GameControls
from scripts.frame_control import FrameControl

RUNNING = True

def game(screen):
    global RUNNING
    dimensions = (150, 30)

    # check if dimensions are proper
    def check_dimensions(screen, dimensions):
        global RUNNING
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
        while not screen.has_resized() and RUNNING:
            pass


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
    # game loop
    '''while RUNNING:
        frame_start = time.time() # start time to calculate delta time

        game_controls.handle_input(screen, player)

        game_controls.render_frame(screen, player, frame_control)

        # calculate delta time
        frame_control.frame_render_time = time.time() - frame_start


        if ((1/60 - frame_control.frame_render_time) > 0):
            game_controls.time_slept = 1/60 - frame_control.frame_render_time
            time.sleep(1/60 - frame_control.frame_render_time)
        frame_control.total_frames += 1 # for calculating avg FPS


        frame_control.delta_time = time.time() - frame_start'''


while RUNNING:
    Screen.wrapper(game)