from time import ticks_ms, ticks_diff

from PicoGame import PicoGame


class SnakeGame(PicoGame):
    
    DEBOUNCE_INTERVAL = 300
    
    def __init__(self):
        super().__init__()
        
        self.last_press_ms = self.DEBOUNCE_INTERVAL
        
        self.snake = Snake()
        
    def run(self):
        while True:
            
            # render
            self.fill(0)
            for s in self.snake.segments:
                self.blit(PIXEL, s[0], s[1])
            self.show()
            
            debounce_delta = ticks_diff(ticks_ms(), self.last_press_ms)
            if self.button_A() and debounce_delta >= self.DEBOUNCE_INTERVAL:
                
                
                
            
            
if __name__ == '__main__':
    sg = SnakeGame()
    sg.run()
    