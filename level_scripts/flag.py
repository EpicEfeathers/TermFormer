from config import termColours

class Flag:
    def __init__(self, data):
        self.flag_pos = data["flag_pos"]
        
        if self.flag_pos == []:
            self.flag_pos = [0, 0] # would use tuple but json only supports arrays (lists)

    #INPUT: screen, Mouse Event, int
    #RETURN: None
    #PURPOSE: Changes the player's flag_pos
    def change_flag_pos(self, screen, event, file_bg_colour):
        '''
        Changes player flag_pos
        '''
        # cover old flag_pos
        screen.print_at(" ", *self.flag_pos, colour=file_bg_colour, bg=file_bg_colour)

        # print new flag_pos
        self.flag_pos = [event.x, event.y]
        screen.print_at("⚑", *self.flag_pos, colour=termColours.red, bg=file_bg_colour)
        screen.refresh()