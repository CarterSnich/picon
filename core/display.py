from machine import Pin, SPI

from core import config
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from lib.ssd1309 import SSD1309_SPI


class Display(SSD1309_SPI):

    def __init__(self):
        # Initialize SPI with miso=None to avoid GPIO 16 conflict
        spi = SPI(0,
                  baudrate=10_000_000,
                  polarity=0,
                  phase=0,
                  sck=Pin(config.SCK),
                  mosi=Pin(config.SDA),
                  miso=None)  # CRITICAL: Avoid GPIO 16 conflict

        # Initialize display
        super().__init__(SCREEN_WIDTH,
                         SCREEN_HEIGHT,
                         spi,
                         dc=Pin(config.DC),
                         rst=Pin(config.RST),
                         cs=Pin(config.CS))


    def center_text(self, text, banner=False):
        x = int(SCREEN_WIDTH / 2) - int((len(text) / 2) * 8)
        y = int(SCREEN_HEIGHT / 2) - 4
        if banner:
            self.fill_rect(0, y - 1, SCREEN_WIDTH, 9, 1)
        self.text(text, x, y, not banner)
