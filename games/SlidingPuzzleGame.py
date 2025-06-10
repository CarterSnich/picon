from random import randint, choice
from time import ticks_diff, ticks_ms

from PicoGame import PicoGame
from games.SlidingPuzzle.Resources import NUMBERS


class SlidingPuzzleGame(PicoGame):
    
    def __init__(self):
        super().__init__()
        
        self.puzzle, self.blank_index = self.generate(200)
        
        self.last_press_ms = 200
        self.last_beep_ms = -1
        
    def generate(self, moves = 100):
        puzzle = list(range(0, 16))
        directions = [-4, 4, -1, 1]
        blank = None
        
        for _ in range(moves):
            index = puzzle.index(15)
            row, col = divmod(index, 4)
            valid_moves = []
            
            for d in directions:
                new_index = index + d
                new_row, new_col = divmod(new_index, 4)
                
                if 0 <= new_index < 16 and abs(new_row - row) + abs(new_col - col) == 1:
                    valid_moves.append(new_index)
                    
            if valid_moves:
                target = choice(valid_moves)
                if puzzle[index] == 15:
                    print()
                    blank = target
                puzzle[index], puzzle[target] = puzzle[target], puzzle[index]
        return puzzle, blank
    
    def move(self, a, b):
        self.puzzle[a], self.puzzle[b] = self.puzzle[b], self.puzzle[a]
        self.blank_index = b
        
    def run(self):
        while True:
            if self.button_B():
                return
            
            # sound off
            if ticks_diff(ticks_ms(), self.last_beep_ms) >= 50:
                self.sound(0)
            
            # Render
            self.fill(0)
            start_x, start_y = 32, 0
            for i, n in enumerate(range(0, 16, 4)):
                for j in range(0, 4):
                    index = n+j
                    x = start_x+(j*16)
                    y = start_y+(i*16)
                    self.blit(NUMBERS[self.puzzle[index]], x, y)
            self.show()
            
            # check if puzzle is solved
            if self.blank_index == 15:
                for i, v in enumerate(self.puzzle):
                    if i != v:
                        break
                else:
                    self.winner()
                    return
                    
            # Inputs
            if ticks_diff(ticks_ms(), self.last_press_ms) >= 200:
                if self.button_up() and self.blank_index > 3:
                    self.sound(880)
                    self.last_beep_ms = ticks_ms()
                    self.last_press_ms = self.last_beep_ms
                    self.move(self.blank_index, self.blank_index-4)
                elif self.button_right() and not self.blank_index in [3, 7, 11, 15]:
                    self.sound(880)
                    self.last_beep_ms = ticks_ms()
                    self.last_press_ms = self.last_beep_ms
                    self.move(self.blank_index, self.blank_index+1)
                elif self.button_down() and self.blank_index < 12:
                    self.sound(880)
                    self.last_beep_ms = ticks_ms()
                    self.last_press_ms = self.last_beep_ms
                    self.move(self.blank_index, self.blank_index+4)
                elif self.button_left() and not self.blank_index in [0, 4, 8, 12]:
                    self.sound(880)
                    self.last_beep_ms = ticks_ms()
                    self.last_press_ms = self.last_beep_ms
                    self.move(self.blank_index, self.blank_index-1)
                    
                    
                     
if __name__ == '__main__':
    SlidingPuzzleGame().run()