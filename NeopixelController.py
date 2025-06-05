from machine import Pin
from time import ticks_ms, ticks_diff
from random import randint
import neopixel, framebuf

from PicoGame import PicoGame

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


class NeopixelController(PicoGame):
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        n = neopixel.NeoPixel(Pin(16), 1)
        pixel = [255, 255, 255]
        
        sequencial = False
        current_color = 0
        
        selection = 0
        last_debounce_ms = -1
        
        
        while True:
            if self.button_B():
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
            
            self.fill(0)
            
            x_start = 20
            x_gap = 32
            
            for i, k in enumerate(["R", "G", "B"]):            
                self.text(k, (i * x_gap) + x_start + 8, 10, 1)
                self.text(f"{int(pixel[i]):03}", (i * x_gap) + x_start, 32, 1)
                
                if selection == i and not sequencial:
                    self.blit(arrow_up, (i * x_gap)+ 8 + x_start, 24)
                    self.blit(arrow_down, (i * x_gap) + 8 + x_start, 44)
                    
            
            if sequencial:
                self.text("SEQUENCIAL", int(self.SCREEN_WIDTH / 2) - 40, 50, 1)
        
            self.show()
            
            if ticks_diff(ticks_ms(), last_debounce_ms) >= 100:
                if self.button_A():
                    last_debounce_ms = ticks_ms()
                    sequencial = not sequencial
                    if sequencial:
                        current_color = 0
                        pixel = [0, 0, 255]
                elif not sequencial:
                    if self.button_right():
                        last_debounce_ms = ticks_ms()
                        if selection >= 2:
                            selection = 0
                        else:
                            selection += 1
                    elif self.button_left():
                        last_debounce_ms = ticks_ms()
                        if selection <= 0:
                            selection = 2
                        else:
                            selection -= 1
                    elif self.button_up() and pixel[selection] <= 250:
                        last_debounce_ms = ticks_ms()
                        pixel[selection] += 5
                    elif self.button_down() and pixel[selection] > 0:
                        last_debounce_ms = ticks_ms()
                        pixel[selection] -= 5
                

if __name__ == '__main__':
    NeopixelController().run()