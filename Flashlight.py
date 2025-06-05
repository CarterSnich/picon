from PicoGame import PicoGame
from time import sleep_ms, ticks_ms, ticks_diff
from machine import Pin, PWM
from main import Pins


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
        
        led = PWM(Pin(Pins.FLASH), freq=1000, duty_u16=0)
        led_state = 0 # OFF, ON, Strobe
        brightness = 100
        
        last_strobe_ms = ticks_ms()
        strobe_delay = 300
        
        while True:
            up = False
            down = False
            left = False
            right = False
            delta = ticks_diff(ticks_ms(), last_pressed_ms)
        
            if self.button_B():
                led.duty_u16(0)
                sleep_ms(300)
                led.deinit()
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
                elif self.button_left():
                    last_pressed_ms = ticks_ms()
                    left = True
                elif self.button_right():
                    last_pressed_ms = ticks_ms()
                    right = True

            self.fill(0)
            
            # LED State OFF
            if led_state == 0:
                led.duty_u16(0)
                self.print("FLASHLIGHT", "OFF")
                
            # LED State ON
            elif led_state == 1:
                if up and brightness < 100 :
                    brightness += 5
                elif down and brightness > 5:
                    brightness -= 5
                led.duty_u16(int(brightness * 65535 / 100))
                self.print("BRIGHTNESS", str(brightness))
                
            # LED State Strobe
            elif led_state == 2:
                if up and strobe_delay < 3000:
                    strobe_delay += 50
                elif down and strobe_delay > 50:
                    strobe_delay -= 50
                    
                if ticks_diff(ticks_ms(), last_strobe_ms) >= strobe_delay:
                    last_strobe_ms = ticks_ms()
                    if led.duty_u16() > 0:
                        led.duty_u16(0)
                    else:
                        led.duty_u16(65535)
                        
                self.print("STROBE DELAY", str(strobe_delay))
                
            self.show()
        
if __name__ == '__main__':
    f = Flashlight()
    f.run()