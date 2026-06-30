# PicoGame.py by YouMakeTech
# A class to easily write games for the Raspberry Pi Pico RetroGaming System
from machine import Pin, PWM, SPI, Timer
from ssd1309 import SSD1309_SPI
from keypad import Keypad
from framebuf import FrameBuffer, MONO_HLSB
import time
import random
import config

class PicoGame(SSD1309_SPI):
    SCREEN_WIDTH = config.SCREEN_WIDTH
    SCREEN_HEIGHT = config.SCREEN_HEIGHT
    
    def __init__(self):
        # Initialize Dpad matrix
        self.__dpad = Keypad(
            [Pin(config.DPAD_ROWS[0]),Pin(config.DPAD_ROWS[1])], # rows
            [Pin(config.DPAD_COLS[0]),Pin(config.DPAD_COLS[1])], # columns
            [['RT', 'LT'], ['UP', 'DN']])
        
        self.__button_A = Pin(config.KEY_A, Pin.IN, Pin.PULL_UP)
        self.__button_B = Pin(config.KEY_B, Pin.IN, Pin.PULL_UP)
        self.__buzzer = PWM(Pin(config.SPEAKER))
        
    
        # Initialize display    
        # Initialize SPI with miso=None to avoid GPIO 16 conflict
        self.__spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0,
                         sck=Pin(config.SCK),
                         mosi=Pin(config.SDA),
                         miso=None)  # CRITICAL: Avoid GPIO 16 conflict
        super().__init__(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
            self.__spi,
            dc=Pin(config.DC),
            rst=Pin(config.RST),
            cs=Pin(config.CS))
        
        self.__fb=[] # Array of FrameBuffer objects for sprites
        self.__w=[]
        self.__h=[]
        
        self.__mute = False
        
    def get_center_x(self, x_offset):
        return int(self.SCREEN_WIDTH / 2) - x_offset

    def get_center_y(self, y_offset):
        return int(self.SCREEN_HEIGHT / 2) - y_offset
    
    def get_center(self, x_offset, y_offset):
        x = self.get_center_x(x_offset)
        y = self.get_center_y(y_offset)
        return x, y
    
    def get_top_left(self, width, height):
        x = int(self.game.SCREEN_WIDTH / 2) - width
        y = int(self.game.SCREEN_HEIGHT / 2) - height
        return x, y
    
    def center_text(self, s, color = 1):
        x = int(self.width/2)- int(len(s)/2 * 8)
        y = int(self.height/2) - 8
        self.text(s, x, y, color)
        
    def top_right_corner_text(self, s, color = 1):
        x = self.width - int(len(s) * 8)
        y = 0
        self.text(s, x, y, color)
        
    def add_sprite(self, buffer, w, h):
        fb = FrameBuffer(buffer, w, h, MONO_HLSB)
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)
        return len(self.__fb) - 1
       
    def sprite(self, n, x, y, key = 0):
        self.blit(self.__fb[n], x, y, key)
        
    def sprite_width(self,n):
        return self.__w[n]
    
    def sprite_height(self,n):
        return self.__h[n]
    
    def sprites_intersection(self, x1, y1, w1, h1, x2, y2, w2, h2):
    # return true if the 2 sprites rectangles
    # (x1,y1,w1,h1) and (x2,y2,w2,h2) overlaps
        overlap = True
        if x2 > x1 + w1 - 1:
            overlap = False
        if x2 + w2 - 1 < x1:
            overlap = False
        if y2 > y1 + h1 -1:
            overlap = False
        if y2 + h2 -1 < y1:
            overlap = False
        return overlap
    
    def sprites_collision(self, n, x1, y1, m, x2, y2):
        if self.sprites_intersection(x1, y1, self.sprite_width(n), self.sprite_height(n), x2, y2, self.sprite_width(m), self.sprite_height(m)):
            dx = max(x1, x2)
            dy = max(y1, y2)
            dw = min(x1 + self.sprite_width(n), x2 + self.sprite_width(m)) - dx
            dh = min(y1 + self.sprite_height(n), y2 + self.sprite_height(m)) - dy
            for j in range(dy, dy + dh):
                for i in range(dx, dx + dw):
                    if self.__fb[n].pixel(i - x1, j - y1) and self.__fb[m].pixel(i - x2, j - y2):
                        return True          
        return False
            
    def button_up(self):
        return self.__dpad.read_keypad() == 'UP'
    
    def button_down(self):
        return self.__dpad.read_keypad() == 'DN'
    
    def button_left(self):
        return self.__dpad.read_keypad() == 'LT'
    
    def button_right(self):
        return self.__dpad.read_keypad() == 'RT'
    
    def button_A(self):
        return self.__button_A.value()==0
    
    def button_B(self):
        return self.__button_B.value()==0
    
    def any_button(self):
        # returns True if any button is pressed
        button_pressed=False
        if self.button_up():
            button_pressed = True
        if self.button_down():
            button_pressed = True
        if self.button_left():
            button_pressed = True
        if self.button_right():
            button_pressed = True
        if self.button_A():
            button_pressed = True
        if self.button_B():
            button_pressed = True
        return button_pressed
    
    def sound(self, freq, duty_u16 = 2000):
        if not self.__mute:
            # Make a sound at the selected frequency in Hz
            if freq>0:
                self.__buzzer.freq(freq)
                self.__buzzer.duty_u16(duty_u16)
            else:
                self.__buzzer.duty_u16(0)
                
    def banner_text(self, t):
        x = int(self.SCREEN_WIDTH/2)-int((len(t)/2) * 8)
        y = int(self.SCREEN_HEIGHT/2)-4
        self.fill_rect(0, y-1, self.SCREEN_WIDTH, 9, 1)
        self.text(t, x, y, 0)
        
    def winner(self):
        self.banner_text("WINNER")
        self.show()
        self.sound(550)
        time.sleep_ms(150)
        self.sound(550)
        time.sleep_ms(50)
        self.sound(880)
        time.sleep_ms(800)
        self.sound(0)
       
    def game_over(self):
        self.banner_text("GAME OVER")
        self.show()
        self.sound(550)
        time.sleep_ms(1000)
        self.sound(0)
