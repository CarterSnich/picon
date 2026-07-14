from time import ticks_diff

from core.config import SCREEN_HEIGHT, SCREEN_WIDTH

from .direction import Direction

MOVEMENT_INTERVAL = 100


class Snake:
    segments = []
    direction = Direction.EAST
    last_move_ms = -1
    last_eat_ms = -1
    is_dead = False


    def __init__(self, head_x, head_y):
        self.segments = [[head_x, head_y], [head_x - 4, head_y], [head_x - 8, head_y]]


    def get_head_segments(self):
        s = self.segments[0]
        return s[0], s[1]


    def get_tail_segments(self):
        s = self.segments[-1]
        return s[0], s[1]


    def set_direction(self, direction):
        self.direction = direction


    def is_stupid(self):
        x, y = self.get_head_segments()
        return [x, y] in self.segments[1:]


    def is_blind(self):
        head = self.get_head_segments()
        return (head[0] < 4 or
                head[0] >= SCREEN_WIDTH - 4 or
                head[1] < 4 or
                head[1] >= SCREEN_HEIGHT - 4)


    def grow(self, tick):
        tail_x, tail_y = self.get_tail_segments()

        if self.direction == Direction.NORTH:
            tail_y -= 4
        elif self.direction == Direction.EAST:
            tail_x += 4
        elif self.direction == Direction.SOUTH:
            tail_y += 4
        elif self.direction == Direction.WEST:
            tail_x -= 4

        self.segments.append([tail_x, tail_y])
        self.last_eat_ms = tick


    def move(self, tick):
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
        self.last_move_ms = tick


    def update(self, tick):
        if ticks_diff(tick, self.last_move_ms) >= MOVEMENT_INTERVAL:
            self.move(tick)

            self.is_dead = self.is_stupid() or self.is_blind()
