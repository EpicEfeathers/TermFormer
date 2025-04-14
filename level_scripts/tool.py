from asciimatics.screen import Screen

from level_scripts.create_colour_list import create_colour_list
from config import termColours

class Tool:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.tool_type = "pen"

    def change_tool_type(self):
        if self.tool_type == "pen":
            self.tool_type = "dropper"
        else:
            self.tool_type = "pen"
    
    def print_tool_type(self, screen):

        screen.clear_buffer(x=self.dimensions[0] - 35, y=self.dimensions[1] - 1, w=35, h=1, fg=termColours.white, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK)

        text = f"Tool: {self.tool_type.capitalize()}"
        colour_list = create_colour_list(text, [self.tool_type.capitalize()], Screen.COLOUR_WHITE, background_color=Screen.COLOUR_BLACK, highlight_text_colour=[termColours.white])
        screen.paint(text, self.dimensions[0] - len(text), self.dimensions[1] - 1, colour_map=colour_list)