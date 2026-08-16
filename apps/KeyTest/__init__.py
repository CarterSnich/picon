__NAME__ = "Key Test"
__CATEGORY__ = "tools"

from apps.KeyTest.sprites import *
from core import PiconApp
from core.helper.countdown import Countdown, STATE_FINISHED, STATE_IDLE, STATE_TICKING
from core.input import Key

COUNTDOWN_MS = 2000


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.current_pressed_key = None
        self.countdown = Countdown(COUNTDOWN_MS)


    def inputs(self):
        self.current_pressed_key = self.input.any_pressed_key()
        if self.current_pressed_key == Key.START:
            if self.countdown.state == STATE_IDLE:
                self.countdown.start(self.current_ms)
        else:
            self.countdown.stop()
            self.countdown.set(COUNTDOWN_MS)


    def update(self):
        if self.current_pressed_key == Key.START:
            if self.countdown.state == STATE_IDLE:
                self.countdown.start(self.current_ms)
            else:
                self.countdown.update(self.current_ms)
                if self.countdown.state == STATE_FINISHED:
                    self.countdown.stop()
                    self.quit()
        elif self.countdown.state == STATE_TICKING:
            self.countdown.stop()
            self.countdown.reset()


    def render(self):
        self.display.text("Hold STA", 32, 2, 1)
        self.display.text("to exit", 36, 11, 1)

        if self.current_pressed_key == Key.LEFT:
            self.display.blit(BUTTON_LEFT_INVERT.framebuffer, 2, 33, 0)
        else:
            self.display.blit(BUTTON_LEFT.framebuffer, 2, 33, 0)

        if self.current_pressed_key == Key.UP:
            self.display.blit(BUTTON_UP_INVERT.framebuffer, 15, 21, 0)
        else:
            self.display.blit(BUTTON_UP.framebuffer, 15, 21, 0)

        if self.current_pressed_key == Key.DOWN:
            self.display.blit(BUTTON_DOWN_INVERT.framebuffer, 15, 45, 0)
        else:
            self.display.blit(BUTTON_DOWN.framebuffer, 15, 45, 0)

        if self.current_pressed_key == Key.RIGHT:
            self.display.blit(BUTTON_RIGHT_INVERT.framebuffer, 28, 33, 0)
        else:
            self.display.blit(BUTTON_RIGHT.framebuffer, 28, 33, 0)

        if self.current_pressed_key == Key.X:
            self.display.blit(BUTTON_X_INVERT.framebuffer, 83, 33, 0)
        else:
            self.display.blit(BUTTON_X.framebuffer, 83, 33, 0)

        if self.current_pressed_key == Key.Y:
            self.display.blit(BUTTON_Y_INVERT.framebuffer, 96, 21, 0)
        else:
            self.display.blit(BUTTON_Y.framebuffer, 96, 21, 0)

        if self.current_pressed_key == Key.A:
            self.display.blit(BUTTON_A_INVERT.framebuffer, 96, 45, 0)
        else:
            self.display.blit(BUTTON_A.framebuffer, 96, 45, 0)

        if self.current_pressed_key == Key.B:
            self.display.blit(BUTTON_B_INVERT.framebuffer, 109, 33, 0)
        else:
            self.display.blit(BUTTON_B.framebuffer, 109, 33, 0)

        if self.current_pressed_key == Key.SELECT:
            self.display.blit(BUTTON_SELECT_INVERT.framebuffer, 53, 30, 0)
        else:
            self.display.blit(BUTTON_SELECT.framebuffer, 53, 30, 0)

        if self.current_pressed_key == Key.START:
            self.display.blit(BUTTON_START_INVERT.framebuffer, 53, 43, 0)
        else:
            self.display.blit(BUTTON_START.framebuffer, 53, 43, 0)


if __name__ == "__main__":
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
