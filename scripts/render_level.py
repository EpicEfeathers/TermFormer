import json
from asciimatics.screen import Screen
#from config import termColours

class LevelRenderer:
    def __init__(self):
        with open("data/playermade/123.json", "r") as file:
            self.data = json.load(file)
            self.level_data = self.data["tiles"]
            self.background_colour = self.data["background_colour"] #termColours.sky_blue

    def render_level(self, screen, player, game_controls, frame_control):
        #screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=0) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer

        # render tiles
        for h, row_data in enumerate(self.level_data):
            for w, tile in enumerate(row_data):
                screen.print_at(text=chr(tile[0]), x=w, y=h, colour=tile[1], attr=tile[2], bg=tile[3])
                #if tile['char'] != " ":
                    #screen.print_at(tile['char'], w, h, tile['colour'])

        # write debug screen
        game_controls.write_debug_screen(screen, player, frame_control, self.background_colour)

        # update player position
        player.update_position(screen, game_controls, frame_control.delta_time)

        # render player
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD, self.background_colour)

        # refresh the display
        screen.refresh()