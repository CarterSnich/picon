from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms

from core import PiconApp
from core.input import KEY_A, KEY_B, DPAD_UP, DPAD_DOWN
from core.config import FLASH, SCREEN_HEIGHT, SCREEN_WIDTH

LED_OFF = 0
LED_ON = 1
LED_STROBE = 2


class Main(PiconApp):
    led = Pin(FLASH, Pin.OUT)
    led_state = LED_OFF

    last_strobe_ms = 0
    strobe_delay = 300

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)

    def inputs(self):
        if self.input.is_pressed(KEY_B):
            self.led_state = LED_OFF
            self.quit()
        elif self.led_state == LED_STROBE:
            if self.input.is_pressed(DPAD_UP) and self.strobe_delay < 3000:
                self.strobe_delay += 50
            elif self.input.is_pressed(DPAD_DOWN) and self.strobe_delay > 50:
                self.strobe_delay -= 50
        elif self.input.is_pressed(KEY_A):
            self.led_state = (self.led_state + 1) % 3

    def update(self):
        if self.led_state == LED_OFF:
            self.led.off()
        elif self.led_state == LED_ON:
            self.led.on()
        elif self.led_state == LED_STROBE:
            if ticks_diff(self.current_tick, self.last_strobe_ms) >= self.strobe_delay:
                self.last_strobe_ms = ticks_ms()
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

