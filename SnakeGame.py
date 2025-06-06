from time import ticks_ms, ticks_diff
from random import randrange

from PicoGame import PicoGame
from Snake.Snake import Snake
from Snake.Food import Food
from Snake.Direction import Direction
from Snake.Resources import PIXEL


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
            x = randrange(0, self.SCREEN_WIDTH-4, 4)
            y = randrange(0, self.SCREEN_HEIGHT-4, 4)
            
            if [x, y] not in self.snake.segments:
                self.food = Food(x, y)
                break
        
    def run(self):
        self.randomize_food()
        
        while True:
            # mute sounds
            if ticks_diff(ticks_ms(), self.last_eat_ms) >= 50:
                self.sound(0)
                
            # FOOD UPDATE STATE
            head = self.snake.head()
            if self.food.is_intersecting(head[0], head[1]):
                self.last_eat_ms = ticks_ms()
                self.sound(1000)
                self.score += 1
                self.randomize_food()
                self.snake.grow()
            
            # SNAKE UPDATE STATE
            if self.snake.can_move():
                self.snake.move()
            # snake hits wall
            is_blind_AF = (
                head[0] <= -4 or
                head[0] >= self.SCREEN_WIDTH or
                head[1] <= -4 or
                head[1] >= self.SCREEN_HEIGHT
            )
            # snake bites itself
            is_stupid = self.snake.intersecting_self()
            # game over then
            if is_stupid or is_blind_AF:
                self.over()
                break
                
            # RENDER
            self.fill(0)
            # snake
            for s in self.snake.segments:
                self.blit(PIXEL, s[0], s[1])
            # food
            self.blit(PIXEL, self.food.x, self.food.y)
            self.top_right_corner_text(str(self.score))
            self.show()
            
            # inputs
            debounce_delta = ticks_diff(ticks_ms(), self.last_press_ms)
            if debounce_delta >= DEBOUNCE_INTERVAL:
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
                
                
                
if __name__ == '__main__':
    sg = SnakeGame()
    sg.run()
    