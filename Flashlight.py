from PicoGame import PicoGame
from time import sleep_ms, ticks_ms, ticks_diff
from machine import Pin, PWM
from main import Pins


def flashlight():
    game = PicoGame()
    led = PWM(Pin(Pins.FLASH), freq=1000, duty_u16=0)
    last_pressed_ms = ticks_ms()
    brightness = 255
    
    while True:
        delta = ticks_diff(ticks_ms(), last_pressed_ms)
        
        if game.button_A() and delta >= 300:
            last_pressed_ms = ticks_ms()
            if led.duty_u16() == 0:
                led.duty_u16(brightness * 257)
            else:
                led.duty_u16(0)
            last_pressed_ms = ticks_ms()
        elif game.button_up() and brightness < 255 and delta >= 100:
            last_pressed_ms = ticks_ms()
            brightness += 10
            led.duty_u16(brightness * 257)
        elif game.button_down() and brightness > 5 and delta >= 100:
            last_pressed_ms = ticks_ms()
            brightness -= 10
            led.duty_u16(brightness* 257)
        elif game.button_B():
            break
        
            
        game.fill(0)
        game.center_text(f"BRIGHTNESS {brightness}" if led.duty_u16() else "FLASHLIGHT OFF")
        game.show()
        
    
if __name__ == '__main__':
    flashlight()