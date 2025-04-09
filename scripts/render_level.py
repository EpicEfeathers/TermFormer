import json
from asciimatics.screen import Screen

class LevelRenderer:
    def __init__(self):
        with open("data/level0.json", "r") as file:
            self.level_data = json.load(file)

    def render_level(self, screen, player, game_controls, frame_control):
        screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer

        for h, row_data in enumerate(self.level_data):
            for w, tile in enumerate(row_data):
                if tile['char'] != " ":
                    screen.print_at(tile['char'], w, h, tile['colour'])

        game_controls.write_debug_screen(screen, player, frame_control)#, game_controls)

        player.update_position(screen, game_controls, frame_control.delta_time)

        #screen = draw_player(screen, p)
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD)

        # refresh the display
        screen.refresh()

        screen.refresh()