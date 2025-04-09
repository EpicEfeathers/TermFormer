from pynput.keyboard import Key, KeyCode

class Player:
    def __init__(self, screen_width, screen_height): # initializing all player variables
        self.x = 2 #int(screen_width / 2)
        self.y = 1
        self.x_velo = 0
        self.y_velo = 0
        self.movement_speed_x = 20

        self.old_x = self.x
        self.old_y = self.y

        self.gravity = 200
        
        self.tile_beneath = None

    def get_tiles_surrounding(self, screen):
        surrounding = {
            "left": screen.get_from(int(self.x - 1), int(self.y)), 
            "up": screen.get_from(int(self.x), int(self.y - 1)), 
            "right": screen.get_from(int(self.x + 1), int(self.y)), 
            "down": screen.get_from(int(self.x), int(self.y + 1)),
            "in": screen.get_from(int(self.x), int(self.y))
        }
        return surrounding


    def update_position(self, screen, game_controls, DELTA_TIME):
        # old position to check if moved
        self.old_x = self.x
        self.old_y = self.y

        # y axis movement
        self.y_velo += self.gravity * DELTA_TIME

        # check tiles above and beneath to see if valid
        tiles_surrounding = self.get_tiles_surrounding(screen)
        if tiles_surrounding["down"] is not None and tiles_surrounding["down"][0] == 9608 and ((Key.space not in game_controls.keys) and (KeyCode(char="w") not in game_controls.keys)): # if tile underneath is block
            self.y_velo = 0
        elif tiles_surrounding["up"] is not None and tiles_surrounding["up"][0] == 9608 and self.y_velo < 0:
            #da a      self.y += 1
            self.y_velo = 0
        else:
            self.y += self.y_velo * DELTA_TIME


        if tiles_surrounding["left"][0] == 9608 and (KeyCode(char="a") in game_controls.keys):
            self.x_velo = 0
        elif tiles_surrounding["right"][0] == 9608 and (KeyCode(char="d") in game_controls.keys):
            self.x_velo = 0
        else:
            # x axis movement
            self.x += self.x_velo * self.movement_speed_x * DELTA_TIME

        # stop flowing off screen
        if self.y > screen.height:
            self.y = screen.height - 1
            self.y_velo = 0
        elif self.y < 0:
            self.y = 0
        
        if self.x < 0:
            self.x = 0
        elif self.x > screen.width:
            self.x = screen.width - 1


        if tiles_surrounding["in"][0] == 9608: # if in block
            self.y -= 1