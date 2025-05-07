# handles the drawing (blocks and spikes)
class HandleDrawing:
    def __init__(self):
        self.mouse_up_pos = None
        self.mouse_down_pos = None

    #INPUT: tuple, screen, Mouse Event, int, str, int (optional), int (optional)
    #RETURN: None
    #PURPOSE: Handles the drawing for the level editor (blocks and spikes) 
    def handle_drawing(self, dimensions, screen, event, pen_colour, character_to_draw, screen_background_colour=None, underlined=1):  
        '''
        Handles mouse up and down input
        and line drawing
        '''  
        if event.buttons == 0: # mouse up
            self.mouse_up_pos = [event.x, event.y]
        elif event.buttons == 1: # mouse down
            self.mouse_down_pos = [event.x, event.y]
            self.mouse_up_pos = None


        if self.mouse_down_pos or self.mouse_up_pos:
            bg_colour = screen.get_from(*self.mouse_down_pos)[3] # just background colour
            if screen_background_colour == pen_colour:
                character_to_draw = " " # if colour same as background, assume user wants to draw background, which is made of spaces
                screen.print_at(character_to_draw, *self.mouse_down_pos, colour=screen_background_colour, attr=underlined, bg=screen_background_colour)
            else:
                screen.print_at(character_to_draw, *self.mouse_down_pos, colour=pen_colour, attr=underlined, bg=bg_colour)

        if self.mouse_up_pos and self.mouse_down_pos:
            if character_to_draw == "█": # allow drawing lines as not have to handle background
                self.mouse_up_pos[1] = min((dimensions[1] - 2), self.mouse_up_pos[1]) # make sure can't draw off bottom of screen
                self.mouse_down_pos[1] = min((dimensions[1] - 2), self.mouse_down_pos[1]) # make sure can't draw off bottom of screen

                screen.move(*self.mouse_down_pos) # * unpacks tuple
                if screen_background_colour == pen_colour:
                    character_to_draw = " " # if colour same as background, assume user wants to draw background, which is made of spaces
                screen.draw(*self.mouse_up_pos, char=character_to_draw, colour=pen_colour, bg=pen_colour, thin=True) # thin means doesn't alias around line


        screen.refresh()