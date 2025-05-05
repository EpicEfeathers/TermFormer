from create_colour_list import create_colour_list

from config import termColours

#INPUT: screen
#RETURN: None
#PURPOSE: Writes the help messages at the bottom of the screen
def write_help(screen):
    text = "WASD / Space to move"
    colour_list = create_colour_list(text, ["WASD / Space"], termColours.popup_gray, termColours.black, [termColours.white])
    screen.paint(text, 0, 30, colour_map=colour_list) # very left

    text = "T to toggle debug screen"
    colour_list = create_colour_list(text, ["T"], termColours.popup_gray, termColours.black, [termColours.white])
    screen.paint(text, int((150-len(text))/2), 30, colour_map=colour_list) # halfway over