import time

# values for frame control stuff (like fps, etc.) to ensure smooth gameplay
# no matter the fps
class FrameControl:
    def __init__(self):
        self.delta_time = 0.00000000001 # small number so no divide by 0 error when starting program
        self.start_timestamp = time.time()
        self.total_frames = 1
        self.frame_render_time = 1

        self.fps = 0