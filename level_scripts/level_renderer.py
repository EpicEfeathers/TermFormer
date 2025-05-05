from asciimatics.screen import Screen

from config import termColours

# i guess i don't really need this class do i?
class LevelRenderer:
    #INPUT: tuple, screen, dict
    #RETURN: None
    #PURPOSE: Renders the level when first opened in the slot popup
    def render_level(self, dimensions, screen, data):
        level_data = data["tiles"]
        background_colour = data["background_colour"]

        if data["spawn_point"] != []:
            spawn_point = data["spawn_point"]

        # render tiles
        if level_data != []:
            for h, row_data in enumerate(level_data):
                for w, tile in enumerate(row_data):
                    screen.print_at(text=chr(tile[0]), x=w, y=h, colour=tile[1], attr=tile[2], bg=tile[3])

        else:
            screen.clear_buffer(x=0, y=0, w=dimensions[0], h=dimensions[1] - 1, fg=0, attr=Screen.A_NORMAL, bg=background_colour) # use this over clear https://asciimatics.readthedocs.io/en/stable/asciimatics.html#asciimatics.screen.Screen.clear_buffer

        screen.print_at("*", *spawn_point, colour=termColours.red, attr=0, bg=background_colour)

        screen.refresh()