from machine import Pin, PWM

from core.config import SPEAKER

DEFAULT_DUTY_CYCLE = 32768


class Sound:

    def __init__(self):
        self.buzzer = PWM(Pin(SPEAKER))


    def tone(self, freq, duty_u16=DEFAULT_DUTY_CYCLE):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty_u16)


    def stop(self):
        self.buzzer.duty_u16(0)
