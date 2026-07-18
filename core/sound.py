from machine import Pin, PWM

from core.config import SPEAKER

DEFAULT_DUTY_CYCLE = 32768


class Sound:
    is_active: bool


    def __init__(self):
        self.buzzer = PWM(Pin(SPEAKER))
        self.is_active = False
        self.stop()


    def tone(self, freq, duty_u16=DEFAULT_DUTY_CYCLE):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty_u16)
        self.is_active = True


    def stop(self):
        self.buzzer.duty_u16(0)
        self.is_active = False
