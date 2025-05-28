# main.py: Game selection menu by Vincent Mistler (YouMakeTech)
from machine import Pin, PWM, I2C, Timer
from ssd1306 import SSD1306_I2C
import time
import random

# Pin configuration
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

if __name__ == "__main__":
    # To avoid strange errors at startup
    # I don't know why but it works!
    time.sleep(0.2)
    
    # Screen resolution
    SCREEN_WIDTH=128                       
    SCREEN_HEIGHT=64
    
    GAMELIST=[
        "Pong",
        "Snake",
        "Space Invaders",
        "Dino",
        "2048",
        "Tetris",
        "Full Speed",
        "Lunar Module",
        "Flashlight"
    ]

    # Buttons
    up = Pin(Pins.KEYPAD_UP, Pin.IN, Pin.PULL_UP)
    down = Pin(Pins.KEYPAD_DOWN, Pin.IN, Pin.PULL_UP)
    left = Pin(Pins.KEYPAD_LEFT, Pin.IN, Pin.PULL_UP)
    right = Pin(Pins.KEYPAD_RIGHT, Pin.IN, Pin.PULL_UP)
    button1 = Pin(Pins.KEYPAD_A, Pin.IN, Pin.PULL_UP)
    button2 = Pin(Pins.KEYPAD_B, Pin.IN, Pin.PULL_UP)
    
    # Buzzer
    buzzer = PWM(Pin(Pins.SPEAKER))
    
    # OLED Screen
    i2c = machine.I2C(Pins.I2C, sda = Pin(Pins.SDA), scl = Pin(Pins.SCL), freq = 400000)
    oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

    current = 0
    game_selected = -1

    while True:
        oled.fill(0)
        
        oled.text(f"{current+1}/{len(GAMELIST)}", 0, 0, 1)
        oled.text(GAMELIST[current], int(SCREEN_WIDTH/2 - int((len(GAMELIST[current])/2) * 8)), int(SCREEN_HEIGHT/2), 1)
        
        oled.show()
        
        time.sleep(0.2)
        buttonPressed = False
        
        while not buttonPressed:
            if down.value() == 0:
                if current >= len(GAMELIST) - 1:
                    current = 0
                else:
                    current += 1
                buttonPressed = True
            elif up.value() == 0:
                if current <= 0:
                    current = len(GAMELIST) - 1
                else:
                    current -= 1
                buttonPressed = True
            elif button1.value() == 0:
                buttonPressed = True
                game_selected = current

        # Make a sound
        buzzer.freq(1000)
        buzzer.duty_u16(2000)
        time.sleep(0.100)
        buzzer.duty_u16(0)
        
        # Start the selected game
        if game_selected >= 0:
            oled.fill(0)
            oled.show()
            
            if game_selected==0:
                from PicoPong import *
                pico_pong_main()
            elif game_selected==1:
                from PicoSnake import *
                pico_snake_main()
            elif game_selected==2:
                from PicoInvaders import *
                pico_invaders_main()
            elif game_selected==3:
                from PicoDino import *
                pico_dino_main()
            elif game_selected==4:
                from Pico2048 import *
                pico_2048_main()
            elif game_selected==5:
                from PicoTetris import *
                pico_tetris_main()
            elif game_selected==6:
                from PicoFullSpeed import *
                pico_full_speed_main()
            elif game_selected==7:
                from PicoLunarModule import *
                pico_lunar_module_main()
            elif game_selected==8:
                from Flashlight import flashlight
                flashlight()
                
        game_selected=-1


