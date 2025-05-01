from asciimatics.screen import Screen
import json

class LevelRenderer:
    def render_level(self, dimensions, slot_num, screen):
        with open(f"data/playermade/level{slot_num}.json", "r") as file:
            data = json.load(file)
            level_data = data["tiles"]

        # render tiles
        if level_data != []:
            for h, row_data in enumerate(level_data):
                for w, tile in enumerate(row_data):
                    screen.print_at(text=chr(tile[0]), x=w, y=h, colour=tile[1], attr=tile[2], bg=tile[3])

        else:
            background_colour = data["background_colour"]
            screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=0, attr=Screen.A_NORMAL, bg=background_colour) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer

        screen.refresh()