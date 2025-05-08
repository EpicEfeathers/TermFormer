import json
from asciimatics.screen import Screen

from scripts.write_help import write_help

# render the level around the player
class LevelRenderer:
    def __init__(self, player):
        self.player = player
        self.file_path = "data/levels/level1.json"

    #INPUT: None
    #RETURN: None
    #PURPOSE: Loads data from a specific file
    def get_data(self):
        with open(self.file_path, "r") as file:
            self.data = json.load(file)
        self.level_data = self.data["tiles"]
        self.background_colour = self.data["background_colour"] #termColours.sky_blue
        self.spawn_point = self.data["spawn_point"]
        self.player.x, self.player.y = self.spawn_point

    #INPUT: screen, class, class, class
    #RETURN: None
    #PURPOSE: Renders the level around the player
    def render_level(self, screen, player, game_controls, frame_control):

        # render tiles
        for h, row_data in enumerate(self.level_data):
            for w, tile in enumerate(row_data):
                screen.print_at(text=chr(tile[0]), x=w, y=h, colour=tile[1], attr=tile[2], bg=tile[3])

        # write debug screen
        game_controls.write_debug_screen(screen, player, frame_control, self.background_colour)

        # update player position
        player.update_position(screen, game_controls, frame_control.delta_time, self.spawn_point)

        # render player
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD, self.background_colour)

        write_help(screen)

        # refresh the display
        screen.refresh()