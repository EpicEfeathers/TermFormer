from config import termColours

# class for manipulating spawn points
class SpawnPoint:
    def __init__(self, data):
        self.spawn_point = data["spawn_point"]
        
        if self.spawn_point == []:
            self.spawn_point = [0, 0] # would use tuple but json only supports arrays (lists)

    #INPUT: screen, Mouse Event, int
    #RETURN: None
    #PURPOSE: Changes the player's spawn point
    def change_spawn_point(self, screen, event, file_bg_colour):
        '''
        Changes player spawn point
        '''
        # cover old spawn point
        screen.print_at(" ", *self.spawn_point, colour=file_bg_colour, bg=file_bg_colour)

        # print new spawn point
        self.spawn_point = [event.x, event.y]
        screen.print_at("*", *self.spawn_point, colour=termColours.red, bg=file_bg_colour)
        screen.refresh()