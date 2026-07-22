from random import randrange
from time import ticks_diff

from core import PiconGame
from core.input import DPAD_UP, DPAD_RIGHT, DPAD_DOWN, DPAD_LEFT
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT

from apps.SnakeGame.snake import Snake
from apps.SnakeGame.food import Food
from apps.SnakeGame.direction import Direction

INITIAL_HEAD_X = 52
INITIAL_HEAD_Y = 48

EAT_SOUND_DURATION = 50
MOVEMENT_INTERVAL = 100


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.score = 0
        self.snake = Snake(INITIAL_HEAD_X, INITIAL_HEAD_Y)
        self.food = Food(-1, -1)

        self.last_move_ms = -1
        self.last_eat_ms = None

        self.randomize_food()


    def inputs(self):
        if self.input.is_pressed(DPAD_UP) and self.snake.direction != Direction.SOUTH:
            self.snake.redirect(Direction.NORTH)
        elif self.input.is_pressed(DPAD_RIGHT) and self.snake.direction != Direction.WEST:
            self.snake.redirect(Direction.EAST)
        elif self.input.is_pressed(DPAD_DOWN) and self.snake.direction != Direction.NORTH:
            self.snake.redirect(Direction.SOUTH)
        elif self.input.is_pressed(DPAD_LEFT) and self.snake.direction != Direction.EAST:
            self.snake.redirect(Direction.WEST)


    def update(self):
        # sound off
        if self.last_eat_ms and ticks_diff(self.current_ms, self.last_eat_ms) >= EAT_SOUND_DURATION:
            self.sound.stop()
            self.last_eat_ms = None

        # snake
        if ticks_diff(self.current_ms, self.last_move_ms) >= MOVEMENT_INTERVAL:
            self.last_move_ms = self.current_ms
            self.snake.move()
            if self.snake.is_stupid() or self.snake.is_blind():
                self.game_over()

        # food
        self.food.update(self.current_ms)
        head = self.snake.get_head_segments()
        if self.food.is_intersecting(head[0], head[1]):
            self.sound.tone(1000)
            self.snake.grow(self.food.x, self.food.y)
            self.randomize_food()
            self.score += 1
            self.last_eat_ms = self.current_ms


    def render(self):
        # border
        self.display.rect(3, 3, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 6, 1)

        # snake
        for (x, y) in self.snake.segments:
            self.display.fill_rect(x, y, 4, 4, 1)

        # food
        if self.food.blink_state:
            self.display.fill_rect(self.food.x, self.food.y, 4, 4, 1)


    def randomize_food(self):
        while True:
            x = randrange(4, SCREEN_WIDTH - 8, 4)
            y = randrange(4, SCREEN_HEIGHT - 8, 4)

            if [x, y] not in self.snake.segments:
                self.food.set_coordinates(x, y)
                break
