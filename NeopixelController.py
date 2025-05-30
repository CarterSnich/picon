from PicoGame import PicoGame
from machine import Pin
from time import ticks_ms, ticks_diff
import neopixel, framebuf
from random import randint

ARROW_UP_BUF = bytearray([
    0b00000000,
    0b00011000,
    0b00111100,
    0b01111110,
])

ARROW_DOWN_BUF = bytearray([
    0b01111110,
    0b00111100,
    0b00011000,
    0b00000000
])

arrow_up = framebuf.FrameBuffer(ARROW_UP_BUF, 8, 4, framebuf.MONO_HLSB)
arrow_down = framebuf.FrameBuffer(ARROW_DOWN_BUF, 8, 4, framebuf.MONO_HLSB)


def neopixel_controller():
    game = PicoGame()
    
    n = neopixel.NeoPixel(Pin(16), 1)
    pixel = [255, 255, 255]
    
    sequencial = False
    current_color = 0
    
    selection = 0
    last_debounce_ms = -1
    
    
    while True:
        if game.button_B():
            n[0] = [0,0,0]
            n.write()
            break
        
        if sequencial:
            if pixel[current_color] >= 255:
                if current_color >= 2:
                    current_color = 0
                else:
                    current_color += 1
                
            pixel[2 if current_color <= 0 else current_color-1] -= 1
            pixel[current_color] += 1
        
        n[0] = pixel
        n.write()
        
        game.fill(0)
        
        x_start = 20
        x_gap = 32
        
        for i, k in enumerate(["R", "G", "B"]):            
            game.text(k, (i * x_gap) + x_start + 8, 10, 1)
            game.text(f"{int(pixel[i]):03}", (i * x_gap) + x_start, 32, 1)
            
            if selection == i and not sequencial:
                game.blit(arrow_up, (i * x_gap)+ 8 + x_start, 24)
                game.blit(arrow_down, (i * x_gap) + 8 + x_start, 44)
                
        
        if sequencial:
            game.text("SEQUENCIAL", int(game.SCREEN_WIDTH / 2) - 40, 50, 1)
    
        game.show()
        
        if ticks_diff(ticks_ms(), last_debounce_ms) >= 100:
            if game.button_A():
                last_debounce_ms = ticks_ms()
                sequencial = not sequencial
                if sequencial:
                    current_color = 0
                    pixel = [0, 0, 255]
            elif not sequencial:
                if game.button_right():
                    last_debounce_ms = ticks_ms()
                    if selection >= 2:
                        selection = 0
                    else:
                        selection += 1
                elif game.button_left():
                    last_debounce_ms = ticks_ms()
                    if selection <= 0:
                        selection = 2
                    else:
                        selection -= 1
                elif game.button_up() and pixel[selection] <= 250:
                    last_debounce_ms = ticks_ms()
                    pixel[selection] += 5
                elif game.button_down() and pixel[selection] > 0:
                    last_debounce_ms = ticks_ms()
                    pixel[selection] -= 5
                

if __name__ == '__main__':
    neopixel_controller()