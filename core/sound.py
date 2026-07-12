from machine import Pin, PWM

from core.config import SPEAKER


class Sound:

    def __init__(self):
        self.buzzer = PWM(Pin(SPEAKER))

    def tone(self, freq, duty_u16=2000):
        if freq:
            self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty_u16)

    def stop(self):
        self.tone(0)