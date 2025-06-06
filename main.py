# main.py: Game selection menu by Vincent Mistler (YouMakeTech)
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from time import sleep_ms, ticks_ms, ticks_diff

from MenuSprites import ARROW_RIGHT, ARROW_LEFT

class Pins:
    KEYPAD_A = 28
    KEYPAD_B = 27
    KEYPAD_UP = 29
    KEYPAD_RIGHT = 26
    KEYPAD_DOWN = 15
    KEYPAD_LEFT = 14
    SPEAKER = 9
    I2C = 0
    SDA = 4
    SCL = 5
    FLASH = 10
    RGB = 16
    
def load_and_run(path, name):
    mod = __import__(path)
    cls = getattr(mod, name)
    cls().run()
    

if __name__ == "__main__":
    # To avoid strange errors at startup
    # I don't know why but it works!
    sleep_ms(200)
    
    # Screen resolution
    SCREEN_WIDTH=128                       
    SCREEN_HEIGHT=64
    
    GAMES = [
        ["SNAKE", "SnakeGame", "SnakeGame"],
        ["BATTLE CITY", "PicoBattleCity", "BattleCity"],
        ["RACING GAME", "RacingGame", "RacingGame"]
    ]
    
    TOOLS = [
        ["FLASHLIGHT", "Flashlight", "Flashlight"],
        ["METRONOME", "Metronome", "Metronome"],
        ["NOTEPAD", "Notepad", "Notepad"],
        ["NEOPIXEL", "NeopixelController", "NeopixelController"],
    ]

    # Buttons
    up = Pin(Pins.KEYPAD_UP, Pin.IN, Pin.PULL_UP)
    down = Pin(Pins.KEYPAD_DOWN, Pin.IN, Pin.PULL_UP)
    left = Pin(Pins.KEYPAD_LEFT, Pin.IN, Pin.PULL_UP)
    right = Pin(Pins.KEYPAD_RIGHT, Pin.IN, Pin.PULL_UP)
    button_A = Pin(Pins.KEYPAD_A, Pin.IN, Pin.PULL_UP)
    button_B = Pin(Pins.KEYPAD_B, Pin.IN, Pin.PULL_UP)
    
    # Buzzer
    buzzer = PWM(Pin(Pins.SPEAKER))
    
    # OLED Screen
    i2c = machine.I2C(Pins.I2C, sda = Pin(Pins.SDA), scl = Pin(Pins.SCL), freq = 400000)
    oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

    # True = Games, False = Tools
    tab_index = True
    # True if selecting items, False when selecting tabs
    is_tab_selection = True
    current_item = 0
    items = GAMES
    last_press_ms = ticks_ms()
    
    while True:
        oled.fill(0)
        
        if tab_index:
            if is_tab_selection:
                oled.blit(ARROW_RIGHT, 4, 1)
                oled.text("GAMES", 12, 1, 1)
            else:            
                oled.fill_rect(0, 0, 68, 9, 1)
                oled.text("GAMES", 12, 1, 0)
                oled.blit(ARROW_LEFT, 0, 32)
                oled.blit(ARROW_RIGHT, SCREEN_WIDTH-8, 32)
            oled.text("TOOLS", 76, 1, 1)
        else:
            if is_tab_selection:
                oled.blit(ARROW_RIGHT, 68, 1)
                oled.text("TOOLS", 76, 1, 1)
            else:
                oled.fill_rect(64, 0, 64, 9, 1)
                oled.text("TOOLS", 76, 1, 0)
                oled.blit(ARROW_LEFT, 0, 32)
                oled.blit(ARROW_RIGHT, SCREEN_WIDTH-8, 32)
            oled.text("GAMES", 12, 1, 1)
        
        title = items[current_item][0]
        oled.text(title, 64-int(len(title)/2)*8, 32, 1)
        oled.show()
        
        if ticks_diff(ticks_ms(), last_press_ms) >= 200:
            if button_A.value() == 0 and not is_tab_selection:
                item = items[current_item]
                load_and_run(item[1], item[2])
            elif left.value() == 0:
                last_press_ms = ticks_ms()
                if is_tab_selection:
                    items = GAMES
                    current_item = 0
                    tab_index = not tab_index
                elif current_item <= 0:
                    current_item = len(items)-1
                else:
                    current_item -= 1
            elif right.value() == 0:
                last_press_ms = ticks_ms()
                if is_tab_selection:                    
                    items = TOOLS
                    current_item = 0
                    tab_index = not tab_index
                elif current_item >= len(items)-1:
                    current_item = 0
                else:
                    current_item += 1
            elif up.value() == 0 and not is_tab_selection:
                last_press_ms = ticks_ms()
                is_tab_selection = True
            elif down.value() == 0 and is_tab_selection:
                last_press_ms = ticks_ms()
                is_tab_selection = False
                