from time import sleep_ms, ticks_ms, ticks_diff
from machine import Pin
from config import FLASH

from PicoGame import PicoGame


class Flashlight(PicoGame):
    
    def __init__(self):
        super().__init__()
    
    
    def print(self, str1, str2):
        x = lambda s: int(self.SCREEN_WIDTH/2) - int((len(s)/2) * 8)
        y = int(self.SCREEN_HEIGHT/2)
        self.text(str1, x(str1), y - 8)
        self.text(str2, x(str2), y + 8)
    
    def run(self):
        last_pressed_ms = ticks_ms()
        button_debounce_ms = 200
        
        led = Pin(FLASH, Pin.OUT)
        led_state = 0 # OFF, ON, Strobe
        
        last_strobe_ms = ticks_ms()
        strobe_delay = 300
        
        while True:
            up = False
            down = False
            delta = ticks_diff(ticks_ms(), last_pressed_ms)
        
            if self.button_B():
                led.off()
                sleep_ms(300)
                break
            elif delta >= button_debounce_ms:
                if self.button_A():
                    last_pressed_ms = ticks_ms()
                    led_state = (led_state + 1) % 3
                elif self.button_up():
                    last_pressed_ms = ticks_ms()
                    up = True            
                elif self.button_down():
                    last_pressed_ms = ticks_ms()
                    down = True

            self.fill(0)
            
            # LED State OFF
            if led_state == 0:
                led.off()
                self.print("FLASHLIGHT", "OFF")
                
            # LED State ON
            elif led_state == 1:
                led.on()
                self.print("FLASHLIGHT", "ON")
                
            # LED State Strobe
            elif led_state == 2:
                if up and strobe_delay < 3000:
                    strobe_delay += 50
                elif down and strobe_delay > 50:
                    strobe_delay -= 50
                    
                if ticks_diff(ticks_ms(), last_strobe_ms) >= strobe_delay:
                    last_strobe_ms = ticks_ms()
                    led.value(not led.value())
                        
                self.print("STROBE DELAY", str(strobe_delay))
                
            self.show()

if __name__ == '__main__':
    Flashlight().run()