from core import PiconApp
from core.input import *
from core.helper.countdown import *

from apps.KeyTest.sprites import *

EXIT_WAIT_MS = 2000


class Main(PiconApp):
    current_pressed_key: int
    countdown: Countdown


    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.current_pressed_key = -1
        self.countdown = Countdown(EXIT_WAIT_MS)


    def inputs(self):
        self.current_pressed_key = self.input.any_pressed_key()


    def update(self):
        if self.current_pressed_key == KEY_START:
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

        if self.current_pressed_key == DPAD_LEFT:
            self.display.blit(BUTTON_LEFT_INVERT.framebuffer, 2, 33, 0)
        else:
            self.display.blit(BUTTON_LEFT.framebuffer, 2, 33, 0)

        if self.current_pressed_key == DPAD_UP:
            self.display.blit(BUTTON_UP_INVERT.framebuffer, 15, 21, 0)
        else:
            self.display.blit(BUTTON_UP.framebuffer, 15, 21, 0)

        if self.current_pressed_key == DPAD_DOWN:
            self.display.blit(BUTTON_DOWN_INVERT.framebuffer, 15, 45, 0)
        else:
            self.display.blit(BUTTON_DOWN.framebuffer, 15, 45, 0)

        if self.current_pressed_key == DPAD_RIGHT:
            self.display.blit(BUTTON_RIGHT_INVERT.framebuffer, 28, 33, 0)
        else:
            self.display.blit(BUTTON_RIGHT.framebuffer, 28, 33, 0)

        if self.current_pressed_key == KEY_X:
            self.display.blit(BUTTON_X_INVERT.framebuffer, 83, 33, 0)
        else:
            self.display.blit(BUTTON_X.framebuffer, 83, 33, 0)

        if self.current_pressed_key == KEY_Y:
            self.display.blit(BUTTON_Y_INVERT.framebuffer, 96, 21, 0)
        else:
            self.display.blit(BUTTON_Y.framebuffer, 96, 21, 0)

        if self.current_pressed_key == KEY_A:
            self.display.blit(BUTTON_A_INVERT.framebuffer, 96, 45, 0)
        else:
            self.display.blit(BUTTON_A.framebuffer, 96, 45, 0)

        if self.current_pressed_key == KEY_B:
            self.display.blit(BUTTON_B_INVERT.framebuffer, 109, 33, 0)
        else:
            self.display.blit(BUTTON_B.framebuffer, 109, 33, 0)

        if self.current_pressed_key == KEY_SELECT:
            self.display.blit(BUTTON_SELECT_INVERT.framebuffer, 53, 30, 0)
        else:
            self.display.blit(BUTTON_SELECT.framebuffer, 53, 30, 0)

        if self.current_pressed_key == KEY_START:
            self.display.blit(BUTTON_START_INVERT.framebuffer, 53, 43, 0)
        else:
            self.display.blit(BUTTON_START.framebuffer, 53, 43, 0)


if __name__ == "__main__":
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
