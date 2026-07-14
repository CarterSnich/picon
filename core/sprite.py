from framebuf import FrameBuffer, MONO_HLSB


class Sprite:
    width = 0
    height = 0
    data = None
    framebuffer = None


    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.framebuffer = FrameBuffer(
            self.data, self.width, self.height, MONO_HLSB)


    def is_colliding(self):
        ...
