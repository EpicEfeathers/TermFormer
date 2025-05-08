from pynput.keyboard import Key, KeyCode

# main player class, does most of the player logic
class Player:
    def __init__(self): # initializing all player variables
        self.x = 1
        self.y = 1
        self.x_velo = 0
        self.y_velo = 0
        self.movement_speed_x = 20

        self.old_x = self.x
        self.old_y = self.y

        self.gravity = 200
        
        self.tile_beneath = None

    #INPUT: screen
    #RETURN: dict
    #PURPOSE: Gets the values of the tiles surrounding the player (later used to check if walls, air, etc.)
    def get_tiles_surrounding(self, screen):
        surrounding = {
            "left": screen.get_from(int(self.x - 1), int(self.y)), 
            "up": screen.get_from(int(self.x), int(self.y - 1)), 
            "right": screen.get_from(int(self.x + 1), int(self.y)), 
            "down": screen.get_from(int(self.x), int(self.y + 1)),
            "in": screen.get_from(int(self.x), int(self.y))
        }
        return surrounding

    #INPUT: screen, class, int, list
    #RETURN: None
    #PURPOSE: Changes player position based on different variables
    def update_position(self, screen, game_controls, DELTA_TIME, spawn_point):
        # old position to check if moved
        self.old_x = self.x
        self.old_y = self.y

        # y axis movement
        self.y_velo += self.gravity * DELTA_TIME

        # check tiles above and beneath to see if valid
        tiles_surrounding = self.get_tiles_surrounding(screen)


        # if touching spike
        if (tiles_surrounding["in"] is not None and tiles_surrounding["in"][0] == 9650):
            self.x, self.y = spawn_point
            self.x_velo = 0
            self.y_velo = 0
            return # don't handle other stuff
        elif (tiles_surrounding["in"] is not None and tiles_surrounding["in"][0] == 9873):
            screen.clear()
            game_controls.main_menu.main_menu = True
            self.x, self.y = -1, -1 # move the character off-screen so it isn't rendered later
            return # don't handle other stuf
    

        if tiles_surrounding["down"] is not None and tiles_surrounding["down"][0] == 9608 and ((Key.space not in game_controls.keys) and (KeyCode(char="w") not in game_controls.keys)): # if tile underneath is block
            self.y_velo = 0
        elif tiles_surrounding["up"] is not None and tiles_surrounding["up"][0] == 9608 and self.y_velo < 0:
            #da a      self.y += 1
            self.y_velo = 0
        else:
            self.y += self.y_velo * DELTA_TIME


        left_tile = tiles_surrounding.get("left") # returns None if position would beoff edge of screen
        right_tile = tiles_surrounding.get("right") # returns None if position would beoff edge of screen
        # if block on left
        if left_tile and left_tile[0] == 9608 and (KeyCode(char="a") in game_controls.keys):
            self.x_velo = 0
        # if block on right
        elif right_tile and right_tile[0] == 9608 and (KeyCode(char="d") in game_controls.keys):
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
            self.y -= 1 # go up one