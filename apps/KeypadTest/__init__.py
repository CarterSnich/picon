from core import PiconApp
from core.input import *
from core.helper import Countdown

from apps.KeypadTest import Sprites


class Main(PiconApp):
    current_pressed_key = None
    countdown = None

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

    def inputs(self):
        self.current_pressed_key = self.input.any_pressed_key()
        if self.current_pressed_key == KEY_START:
            if self.countdown:
                self.countdown.update(self.current_tick)
            else:
                self.countdown = Countdown(3000)

    def update(self):
        if self.countdown and self.countdown.finished():
            self.countdown = None
            self.quit()

    def render(self):
        self.display.text("Hold STA", 32, 2, 1)
        self.display.text("to exit", 36, 11, 1)

        if self.current_pressed_key == DPAD_LEFT:
            self.display.blit(Sprites.KEYPAD_LEFT_INVERT, 2, 33, 0)
        else:
            self.display.blit(Sprites.KEYPAD_LEFT, 2, 33, 0)

        if self.current_pressed_key == DPAD_UP:
            self.display.blit(Sprites.KEYPAD_UP_INVERT, 15, 21, 0)
        else:
            self.display.blit(Sprites.KEYPAD_UP, 15, 21, 0)

        if self.current_pressed_key == DPAD_DOWN:
            self.display.blit(Sprites.KEYPAD_DOWN_INVERT, 15, 45, 0)
        else:
            self.display.blit(Sprites.KEYPAD_DOWN, 15, 45, 0)

        if self.current_pressed_key == DPAD_RIGHT:
            self.display.blit(Sprites.KEYPAD_RIGHT_INVERT, 28, 33, 0)
        else:
            self.display.blit(Sprites.KEYPAD_RIGHT, 28, 33, 0)

        if self.current_pressed_key == KEY_X:
            self.display.blit(Sprites.KEYPAD_X_INVERT, 83, 33, 0)
        else:
            self.display.blit(Sprites.KEYPAD_X, 83, 33, 0)

        if self.current_pressed_key == KEY_Y:
            self.display.blit(Sprites.KEYPAD_Y_INVERT, 96, 21, 0)
        else:
            self.display.blit(Sprites.KEYPAD_Y, 96, 21, 0)

        if self.current_pressed_key == KEY_A:
            self.display.blit(Sprites.KEYPAD_A_INVERT, 96, 45, 0)
        else:
            self.display.blit(Sprites.KEYPAD_A, 96, 45, 0)

        if self.current_pressed_key == KEY_B:
            self.display.blit(Sprites.KEYPAD_B_INVERT, 109, 33, 0)
        else:
            self.display.blit(Sprites.KEYPAD_B, 109, 33, 0)

        if self.current_pressed_key == KEY_SELECT:
            self.display.blit(Sprites.KEY_SELECT_INVERT, 53, 30, 0)
        else:
            self.display.blit(Sprites.KEY_SELECT, 53, 30, 0)

        if self.current_pressed_key == KEY_START:
            self.display.blit(Sprites.KEY_START_INVERT, 53, 43, 0)
        else:
            self.display.blit(Sprites.KEY_START, 53, 43, 0)

