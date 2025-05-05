from asciimatics.screen import Screen

from create_colour_list import create_colour_list
from config import termColours, keys

# handles tools and tool switching
class Tool:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.tool_type = "pen"
        self.tool_index = 0

        self.tools = ["pen","dropper","spike","spawn point"]

    #INPUT: None
    #RETURN: None
    #PURPOSE: Rotates through tools
    def change_tool_type(self):
        '''
        Rotates through tools.
        '''
        self.tool_index += 1
        self.tool_type = self.tools[self.tool_index % len(self.tools)] # set tool type to the first index of the list
        
    #INPUT: int
    #RETURN: None
    #PURPOSE: Sets user's tool, based on a hotkey (keys 1-4) 
    def hotkey_change_tool_type(self, key):
        '''
        Hotkeys for different tool types'''
        tool_types = {
            keys.key_1: self.tools[0],
            keys.key_2: self.tools[1],
            keys.key_3: self.tools[2],
            keys.key_4: self.tools[3]
        }

        self.tool_type = tool_types[key]
        self.tool_index = list(tool_types).index(key)
    
    #INPUT: screen
    #RETURN: None
    #PURPOSE: Prints the tool type at the bottom right of the screen
    def print_tool_type(self, screen):
        '''
        UI ELEMENT
        Prints the tool type at the bottom right corner of the screen.
        '''

        screen.clear_buffer(x=self.dimensions[0] - 35, y=self.dimensions[1] - 1, w=35, h=1, fg=termColours.white, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK)

        text = f"Tool: {self.tool_type.capitalize()}"
        colour_list = create_colour_list(text, [self.tool_type.capitalize()], Screen.COLOUR_WHITE, background_color=Screen.COLOUR_BLACK, highlight_text_colour=[termColours.white])
        screen.paint(text, self.dimensions[0] - len(text), self.dimensions[1] - 1, colour_map=colour_list)