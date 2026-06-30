from machine import Pin, PWM, I2C
from ssd1309 import SSD1309_SPI
from keypad import Keypad
from time import sleep_ms, ticks_ms, ticks_diff

import config
from MenuSprites import GAMES_OR_TOOLS, ARROW_RIGHT


class Picon:
    DPAD = Keypad(
        [Pin(config.DPAD_ROWS[0]),Pin(config.DPAD_ROWS[1])], # rows
        [Pin(config.DPAD_COLS[0]),Pin(config.DPAD_COLS[1])], # columns
        [['RT', 'LT'], ['UP', 'DN']])
    KEY_A = Pin(config.KEY_A, Pin.IN, Pin.PULL_UP)
    KEY_B = Pin(config.KEY_B, Pin.IN, Pin.PULL_UP)
    BUZZER = PWM(Pin(config.SPEAKER))
    
    def __init__(self, display, games, tools):
        self.display = display
        self.games = games
        self.tools = tools
    
    def load_and_run(self, path, class_name):
        mod = __import__(path)
        mod = getattr(mod, path.split(".")[1])
        cls = getattr(mod, class_name)
        cls().run()
    
    def run(self):
        # top level menu
        is_top_level_menu = True
        # False = Games, True = Tools
        is_inverted = False
        
        # item selection
        current_index = 0
        selection_index = 0
        items_stop_index = 0
        max_index = 0
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
                _items = items[items_stop_index-max_index:items_stop_index]
                y = 0
                for i, item in enumerate(_items):
                    if i == selection_index:
                        self.display.blit(ARROW_RIGHT, 0, y)
                    self.display.text(item[0], 8, y)
                    y += 8
            self.display.show()
            
            # Add 200ms interval between button presses
            if ticks_diff(tick, last_press_ms) < 200:
                continue
            
            # Handle
            if is_top_level_menu:
                if self.DPAD.read_keypad() == 'UP':
                    last_press_ms = tick
                    is_inverted = False
                elif self.DPAD.read_keypad() == 'DN':
                    last_press_ms = tick
                    is_inverted = True
                elif not self.KEY_A.value():
                    last_press_ms = tick
                    is_top_level_menu = False
                    items = TOOLS if is_inverted else GAMES
                    max_index = min(len(items), 8)
                    items_stop_index = max_index
                    selection_index = 0
            else:
                if not self.KEY_A.value() and len(items):
                    item = items[current_index]
                    path = item[1]
                    mod = item[2]
                    self.load_and_run(path, mod)
                    sleep_ms(200)
                elif not self.KEY_B.value():
                    last_press_ms = tick
                    is_top_level_menu = True
                elif self.DPAD.read_keypad() == 'UP':
                    last_press_ms = tick
                    if selection_index > 0:
                        selection_index -= 1
                    elif items_stop_index > 8:
                        items_stop_index -= 1
                    current_index = items_stop_index-(max_index-selection_index-1)-1
                elif self.DPAD.read_keypad() == 'DN':
                    last_press_ms = tick
                    if selection_index < max_index-1:
                        selection_index += 1
                    elif items_stop_index < len(items):
                        items_stop_index += 1
                    current_index = items_stop_index-(max_index-selection_index-1)-1
                        
            

        
if __name__ == '__main__':
    # this delay saves the world
    sleep_ms(200)
    
    GAMES = [
        ["SNAKE", "games.SnakeGame", "SnakeGame"],
        ["BATTLE CITY", "games.BattleCityGame", "BattleCity"],
        ["RACING GAME", "games.RacingGame", "RacingGame"],
        ["SLIDING PUZZLE", "games.SlidingPuzzleGame", "SlidingPuzzleGame"]
    ]
    TOOLS = [
        ["FLASHLIGHT", "tools.Flashlight", "Flashlight"],
        ["METRONOME", "tools.Metronome", "Metronome"],
        # ["NEOPIXEL CONTROLLER", "tools.NeopixelController", "NeopixelController"],
        ["NOTEPAD", "tools.Notepad", "Notepad"],
        ["KEYPAD TEST", "tools.KeypadTest", "KeypadTest"],
    ]
    
    # Initialize SPI with miso=None to avoid GPIO 16 conflict
    spi = machine.SPI(0,
                      baudrate=10_000_000,
                      polarity=0,
                      phase=0,
                      sck=machine.Pin(18),
                      mosi=machine.Pin(19),
                      miso=None)  # CRITICAL: Avoid GPIO 16 conflict

    # Initialize display
    display = SSD1309_SPI(128, 64, spi,
                       dc=machine.Pin(16),
                       rst=machine.Pin(20),
                       cs=machine.Pin(17))
    
    Picon(display, GAMES, TOOLS).run()