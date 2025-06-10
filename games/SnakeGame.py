from time import ticks_ms, ticks_diff
from random import randrange

from PicoGame import PicoGame
from games.Snake.Snake import Snake
from games.Snake.Food import Food
from games.Snake.Direction import Direction
from games.Snake.Resources import SNAKE_HEAD


DEBOUNCE_INTERVAL = 100
INITIAL_HEAD_X = 52
INITIAL_HEAD_Y = 48

class SnakeGame(PicoGame):

    def __init__(self):
        super().__init__()
        
        self.score = 0
        self.last_press_ms = DEBOUNCE_INTERVAL
        self.last_eat_ms = 0
        
        self.snake = Snake(INITIAL_HEAD_X, INITIAL_HEAD_Y)
        self.food = None
    
    def randomize_food(self):
        while True:
            x = randrange(4, self.SCREEN_WIDTH-8, 4)
            y = randrange(4, self.SCREEN_HEIGHT-8, 4)
            
            if [x, y] not in self.snake.segments:
                self.food = Food(x, y)
                break
        
    def run(self):
        self.randomize_food()
        
        while True:
            # mute sounds
            if ticks_diff(ticks_ms(), self.last_eat_ms) >= 50:
                self.sound(0)
            
            # SNAKE UPDATE STATE
            if self.snake.can_move():
                self.snake.move()
            head = self.snake.head()
            # snake hits wall
            is_blind_AF = (
                head[0] < 4 or
                head[0] >= self.SCREEN_WIDTH-4 or
                head[1] < 4 or
                head[1] >= self.SCREEN_HEIGHT-4
            )
            # snake bites itself
            is_stupid = self.snake.intersecting_self()
            # game over then
            if is_stupid or is_blind_AF:
                self.game_over()
                break
            
            # RENDER
            self.fill(0)
            self.rect(3, 3, self.SCREEN_WIDTH-6, self.SCREEN_HEIGHT-6, 1)
            # food
            if self.food.blink_state:
                self.fill_rect(self.food.x, self.food.y, 4, 4, 1)
            
            # snake
            for s in self.snake.segments:
                self.fill_rect(s[0], s[1], 4, 4, 1)
            self.show()
            
            # inputs
            debounce_delta = ticks_diff(ticks_ms(), self.last_press_ms)
            if self.snake.can_move():
                if self.button_up()and self.snake.direction != Direction.SOUTH:
                    self.last_press_ms = ticks_ms()
                    self.snake.set_direction(Direction.NORTH)
                elif self.button_right()and self.snake.direction != Direction.WEST:
                    self.last_press_ms = ticks_ms()
                    self.snake.set_direction(Direction.EAST)
                elif self.button_down() and self.snake.direction != Direction.NORTH:
                    self.last_press_ms = ticks_ms()
                    self.snake.set_direction(Direction.SOUTH)
                elif self.button_left() and self.snake.direction != Direction.EAST:
                    self.last_press_ms = ticks_ms()
                    self.snake.set_direction(Direction.WEST)
            
            # snake head
            head = self.snake.head()
            # FOOD UPDATE STATE
            if self.food.is_intersecting(head[0], head[1]):
                self.last_eat_ms = ticks_ms()
                self.sound(1000)
                self.score += 1
                self.randomize_food()
                self.snake.grow()
            # food update
            self.food.update()
                
                
if __name__ == '__main__':
    SnakeGame().run()
    