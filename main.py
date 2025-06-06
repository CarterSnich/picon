from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from time import sleep_ms, ticks_ms, ticks_diff

import config
from MenuSprites import ARROW_LEFT, GAMES_OR_TOOLS


class Picon:
    KEY_UP = Pin(config.KEY_UP, Pin.IN, Pin.PULL_UP)
    KEY_DOWN = Pin(config.KEY_DOWN, Pin.IN, Pin.PULL_UP)
    KEY_LEFT = Pin(config.KEY_LEFT, Pin.IN, Pin.PULL_UP)
    KEY_RIGHT = Pin(config.KEY_RIGHT, Pin.IN, Pin.PULL_UP)
    KEY_A = Pin(config.KEY_A, Pin.IN, Pin.PULL_UP)
    KEY_B = Pin(config.KEY_B, Pin.IN, Pin.PULL_UP)
    BUZZER = PWM(Pin(config.SPEAKER))
    
    def __init__(self, display, games, tools):
        self.display = display
        self.games = games
        self.tools = tools
    
    def load_and_run(self, path, name):
        mod = __import__(path)
        cls = getattr(mod, name)
        cls().run()
    
    def run(self):
        # top level menu
        is_top_level_menu = True
        # False = Games, True = Tools
        is_inverted = False
        
        # item selection
        current_index = 0
        items = []
        
        last_press_ms = 0
        
        while True:
            # curren tick
            tick = ticks_ms()
            
            # Render
            self.display.fill(0)
            
            if is_top_level_menu:                
                self.display.blit(GAMES_OR_TOOLS, 0, 0)
                self.display.invert(is_inverted)
            else:
                self.display.invert(0)
                for i, y in enumerate(range(0, config.SCREEN_HEIGHT-8, 8)):
                    if i >= len(items):
                        break
                    if current_index == i:
                        self.display.blit(ARROW_LEFT, config.SCREEN_WIDTH-8, y)
                    self.display.text(items[i][0], 0, y, 1)
            self.display.show()
            
            # Handle inputs
            if ticks_diff(tick, last_press_ms) < 300:
                continue
            
            if is_top_level_menu:
                if not self.KEY_UP.value():
                    last_press_ms = tick
                    is_inverted = False
                elif not self.KEY_DOWN.value():
                    last_press_ms = tick
                    is_inverted = True
                elif not self.KEY_A.value():
                    last_press_ms = tick
                    is_top_level_menu = False
                    items = TOOLS if is_inverted else GAMES
            else:
                if not self.KEY_A.value():
                    path = items[current_index][1]
                    mod = items[current_index][2]
                    self.load_and_run(path, mod)
                    sleep_ms(300)
                elif not self.KEY_B.value():
                    last_press_ms = tick
                    is_top_level_menu = True
                elif not self.KEY_UP():
                    last_press_ms = tick
                    if current_index <= 0:
                        current_index = len(items)-1
                    else:
                        current_index -= 1
                elif not self.KEY_DOWN.value():
                    last_press_ms = tick
                    if current_index >= len(items)-1:
                        current_index = 0
                    else:
                        current_index += 1
            

        
if __name__ == '__main__':
    # this delay saves the world
    sleep_ms(200)
    
    GAMES = [
        ["SNAKE", "SnakeGame", "SnakeGame"],
        ["BATTLE CITY", "PicoBattleCity", "BattleCity"],
        ["RACING GAME", "RacingGame", "RacingGame"]
    ]
    TOOLS = [
        ["FLASHLIGHT", "Flashlight", "Flashlight"],
        ["METRONOME", "Metronome", "Metronome"],
        ["NEOPIXEL", "NeopixelController", "NeopixelController"],
        ["NOTEPAD", "Notepad", "Notepad"],
        ["KEYPAD TEST", "KeypadTest", "KeypadTest"],
    ]
    
    i2c = machine.I2C(config.I2C, sda = Pin(config.SDA), scl = Pin(config.SCL), freq = 400000)
    display = SSD1306_I2C(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, i2c)
    
    Picon(display, GAMES, TOOLS).run()