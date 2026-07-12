from random import choice
from time import ticks_diff

from core import PiconGame
from core.input import DPAD_UP, DPAD_RIGHT, DPAD_DOWN, DPAD_LEFT

from .Resources import *

MOVE_UP = -4
MOVE_DOWN = 4
MOVE_LEFT = -1
MOVE_RIGHT = 1

SPRITES = [
    ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
    ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN, BLANK
]


class Main(PiconGame):
    puzzle = None
    blank_index = -1

    last_beep_ms = -1

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.generate_puzzle(200)

    def generate_puzzle(self, moves=100):
        puzzle = list(range(0, 16))
        directions = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]
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
                    blank = target
                puzzle[index], puzzle[target] = puzzle[target], puzzle[index]

        self.puzzle, self.blank_index = puzzle, blank

    def move(self, direction):
        target = self.blank_index

        if direction == MOVE_UP and self.blank_index > 3:
            target += MOVE_UP
        elif direction == MOVE_DOWN and self.blank_index < 12:
            target += MOVE_DOWN
        elif direction == MOVE_LEFT and self.blank_index not in (0, 4, 8, 12):
            target += MOVE_LEFT
        elif direction == MOVE_RIGHT and self.blank_index not in (3, 7, 11, 15):
            target += MOVE_RIGHT
        else:
            return

        self.puzzle[self.blank_index], self.puzzle[target] = (
            self.puzzle[target],
            self.puzzle[self.blank_index]
        )
        self.blank_index = target
        self.sound.tone(880)
        self.last_beep_ms = self.current_tick

    def inputs(self):
        if self.input.is_pressed(DPAD_UP):
            self.move(MOVE_UP)
        elif self.input.is_pressed(DPAD_DOWN):
            self.move(MOVE_DOWN)
        elif self.input.is_pressed(DPAD_LEFT):
            self.move(MOVE_LEFT)
        elif self.input.is_pressed(DPAD_RIGHT):
            self.move(MOVE_RIGHT)

    def update(self):
        if ticks_diff(self.current_tick, self.last_beep_ms) >= 50:
            self.sound.tone(0)

        # Check if puzzle is solved
        if self.blank_index == 15:
            for i, v in enumerate(self.puzzle):
                if i != v:
                    break
            else:
                self.winner()

    def render(self):
        start_x, start_y = 32, 0
        for i, n in enumerate(range(0, 16, 4)):
            for j in range(0, 4):
                index = n + j
                x = start_x + (j * 16)
                y = start_y + (i * 16)
                self.display.blit(SPRITES[self.puzzle[index]], x, y)
