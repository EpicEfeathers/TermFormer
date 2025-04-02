from pynput.keyboard import Listener, Key, KeyCode
from asciimatics.screen import Screen
import time

RUNNING = True

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.jumping = False

        self.x = int(self.screen_width / 2)
        #self.y = int(self.screen_height / 2)
        self.y = 0
        self.x_velo = 0
        self.y_velo = 0
        #self.movement_speed_x = 0.01
        self.movement_speed_x = 20
        #self.movement_speed_y = 0.005

        self.old_x = self.x
        self.old_y = self.y

        #self.gravity = 0.00003
        self.gravity = 200


    def udpate_position(self, screen_height, screen_width, DELTA_TIME):
        self.old_x = self.x
        self.old_y = self.y

        
        self.x += self.x_velo * self.movement_speed_x * DELTA_TIME
        #self.y += self.y_velo * self.movement_speed_y   
        self.y_velo += self.gravity * DELTA_TIME
        self.y += self.y_velo * DELTA_TIME

        # stop flowing off screen
        if self.y > screen_height:
            self.y = screen_height - 1
            self.y_velo = 0
        elif self.y < 0:
            self.y = 0
        
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width:
            self.x = screen_width - 1


def demo(screen):
    def on_press(key):
        if key == KeyCode(char="w"):
            if player.y >= 10:
                player.y_velo = -1
                player.jumping = True
        elif key == KeyCode(char="a"):
            player.x_velo = -1
        elif key == KeyCode(char="s"):
            player.y_velo = 1
        elif key == KeyCode(char="d"):
            player.x_velo = 1
        elif key == Key.space:
            if player.y > 16:
                #player.y_velo = -0.02
                player.y_velo = -50

    def on_release(key):
        if key == KeyCode(char="w") or key == KeyCode(char="s"):
            player.y_velo = 0
        elif key == KeyCode(char="a") or key == KeyCode(char="d"):
            player.x_velo = 0
        #print(f'{key} released')
        if key == Key.esc:
            # Stop listener
            global RUNNING
            RUNNING = False


    player = Player(screen.width, screen.height)

    # non-blocking listener for keyboard inputs
    listener = Listener(on_press=on_press,on_release=on_release)
    listener.start()
    #screen.print_at("███████████████████", int(screen.width/2 - 8), 11)

    total_time = 0.00000000001
    total_frames = 1
    delta_time = 1

    while RUNNING:
        start = time.time() # start time to calculate delta time
        player.udpate_position(screen.height, screen.width, delta_time)

        #screen = draw_player(screen, p)
        screen.print_at(f"o", int(player.x), int(player.y), Screen.COLOUR_WHITE, Screen.A_BOLD)
        if (int(player.old_x) != int(player.x)) or (int(player.old_y) != int(player.y)):
            screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=int(player.old_x), y=int(player.old_y), w=1, h=1)
        
        screen.refresh()


        screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLACK, x=0, y=0, w=30, h=2)
        screen.print_at(f"Y: {"{:.3f}".format(round(player.y, 3))}, Y velo: {"{:.3f}".format(round(player.y_velo, 3))}", 0, 0, Screen.COLOUR_GREEN)
        screen.print_at(f"{round(1/delta_time)} FPS, {round(1/(total_time / total_frames), 5)} Avg FPS", 0, 1)



        #time.sleep(1/60)

        # calculate delta time
        delta_time = time.time() - start
        total_time += delta_time
        total_frames += 1




Screen.wrapper(demo)