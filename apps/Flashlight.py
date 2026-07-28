from machine import Pin

from core import PiconApp, has_elapsed
from core.config import FLASH, SCREEN_HEIGHT, SCREEN_WIDTH
from core.input import Key

LED_OFF = 0
LED_ON = 1
LED_STROBE = 2

DEFAUTL_STROBE_DELAY_MS = 300


class Main(PiconApp):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

        self.led = Pin(FLASH, Pin.OUT)
        self.led_state = LED_OFF

        self.last_strobe_ms = self.current_ms
        self.strobe_delay = DEFAUTL_STROBE_DELAY_MS


    def inputs(self):
        if self.input.is_pressed(Key.B):
            self.led_state = LED_OFF
            self.quit()
        elif self.input.is_pressed(Key.A):
            self.led_state = (self.led_state + 1) % 3
        elif self.led_state == LED_STROBE:
            if self.input.is_pressed(Key.UP) and self.strobe_delay < 3000:
                self.strobe_delay += 50
            elif self.input.is_pressed(Key.DOWN) and self.strobe_delay > 50:
                self.strobe_delay -= 50


    def update(self):
        if self.led_state == LED_OFF:
            self.led.off()
        elif self.led_state == LED_ON:
            self.led.on()
        elif self.led_state == LED_STROBE:
            if has_elapsed(self.current_ms, self.last_strobe_ms, self.strobe_delay):
                self.last_strobe_ms = self.current_ms
                self.led.value(not self.led.value())


    def render(self):
        if self.led_state == LED_STROBE:
            self.print("STROBE DELAY", str(self.strobe_delay))
        else:
            self.led.value(self.led_state)
            self.print("FLASHLIGHT", "ON" if self.led_state else "OFF")


    def print(self, str1, str2):
        x = lambda s: int(SCREEN_WIDTH / 2) - int((len(s) / 2) * 8)
        y = int(SCREEN_HEIGHT / 2)
        self.display.text(str1, x(str1), y - 8)
        self.display.text(str2, x(str2), y + 8)


if __name__ == '__main__':
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
