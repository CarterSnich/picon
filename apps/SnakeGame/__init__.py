from random import randrange

from core import PiconGame, Input
from core.input import DPAD_UP, DPAD_RIGHT, DPAD_DOWN, DPAD_LEFT
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

from apps.SnakeGame.Snake import Snake
from apps.SnakeGame.Food import Food
from apps.SnakeGame.Direction import Direction

INITIAL_HEAD_X = 52
INITIAL_HEAD_Y = 48
INPUT_INTERVAL = 100


class Main(PiconGame):
    score = 0

    snake = None
    food = None

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.input.set_debounce(INPUT_INTERVAL)
        self.snake = Snake(INITIAL_HEAD_X, INITIAL_HEAD_Y)
        self.food = Food(-1, -1)
        self.randomize_food()

    def randomize_food(self):
        while True:
            x = randrange(4, SCREEN_WIDTH - 8, 4)
            y = randrange(4, SCREEN_HEIGHT - 8, 4)

            if [x, y] not in self.snake.segments:
                self.food.set_coordinates(x, y)
                break

    def inputs(self):
        if self.input.is_pressed(DPAD_UP) and self.snake.direction != Direction.SOUTH:
            self.snake.set_direction(Direction.NORTH)
        elif self.input.is_pressed(DPAD_RIGHT) and self.snake.direction != Direction.WEST:
            self.snake.set_direction(Direction.EAST)
        elif self.input.is_pressed(DPAD_DOWN) and self.snake.direction != Direction.NORTH:
            self.snake.set_direction(Direction.SOUTH)
        elif self.input.is_pressed(DPAD_LEFT) and self.snake.direction != Direction.EAST:
            self.snake.set_direction(Direction.WEST)

    def update(self):
        # food
        self.food.update(self.current_tick)
        head = self.snake.get_head_segments()
        if self.food.is_intersecting(head[0], head[1]):
            self.sound.tone(1000)
            self.snake.grow(self.current_tick)
            self.randomize_food()
            self.score += 1

        # snake
        self.snake.update(self.current_tick)
        if self.snake.is_dead:
            self.game_over()

    def render(self):
        # border
        self.display.rect(3, 3, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 6, 1)

        # snake
        for (x, y) in self.snake.segments:
            self.display.fill_rect(x, y, 4, 4, 1)

        # food
        if self.food.blink_state:
            self.display.fill_rect(self.food.x, self.food.y, 4, 4, 1)
