from time import ticks_diff

from core.config import SCREEN_HEIGHT, SCREEN_WIDTH

from apps.SnakeGame.direction import Direction


class Snake:

    def __init__(self, head_x, head_y):
        self.segments = [[head_x, head_y], [head_x - 4, head_y], [head_x - 8, head_y]]
        self.direction = Direction.EAST
        self.redirection = Direction.EAST
        self.can_move = False


    def get_head_segments(self):
        s = self.segments[0]
        return s[0], s[1]


    def get_tail_segments(self):
        s = self.segments[-1]
        return s[0], s[1]


    def redirect(self, direction):
        if self.can_move:
            self.direction = direction
            self.can_move = False


    def is_stupid(self):
        x, y = self.get_head_segments()
        return [x, y] in self.segments[1:]


    def is_blind(self):
        head = self.get_head_segments()
        return (head[0] < 4 or
                head[0] >= SCREEN_WIDTH - 4 or
                head[1] < 4 or
                head[1] >= SCREEN_HEIGHT - 4)


    def grow(self, x, y):
        self.segments.insert(0, [x, y])


    def move(self):
        head_x, head_y = self.get_head_segments()

        if self.direction == Direction.NORTH:
            head_y -= 4
        elif self.direction == Direction.EAST:
            head_x += 4
        elif self.direction == Direction.SOUTH:
            head_y += 4
        elif self.direction == Direction.WEST:
            head_x -= 4

        self.segments.insert(0, [head_x, head_y])
        self.segments.pop()
        self.can_move = True
