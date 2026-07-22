from framebuf import FrameBuffer, MONO_HLSB


class Sprite:

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height
        self.framebuffer = FrameBuffer(
            self.data, self.width, self.height, MONO_HLSB)


    def draw(self, display, x, y, key=-1):
        display.blit(self.framebuffer, x, y, key)


class GameObject:

    def __init__(self, sprite: Sprite, x: int, y: int):
        self.sprite = sprite
        self.x = x
        self.y = y


    def is_colliding(self, other: GameObject, box_collision=False):
        # Bounding box
        if (self.x >= other.x + other.sprite.width or
                other.x >= self.x + self.sprite.width or
                self.y >= other.y + other.sprite.height or
                other.y >= self.y + self.sprite.height):
            return False

        if box_collision:
            return True

        left = max(self.x, other.x)
        top = max(self.y, other.y)
        right = min(self.x + self.sprite.width, other.x + other.sprite.width)
        bottom = min(self.y + self.sprite.height, other.y + other.sprite.height)

        for y in range(top, bottom):
            for x in range(left, right):
                if (self.sprite.framebuffer.pixel(x - self.x, y - self.y) and
                        other.sprite.framebuffer.pixel(x - other.x, y - other.y)):
                    return True

        return False


    def draw(self, display, x, y, key=-1):
        self.sprite.draw(display, x, y, key)
