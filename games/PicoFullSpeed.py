# Game "Full Speed" by Kuba & Stepan
# Source code from https://github.com/Hellmole/Raspberry-pi-pico-games.git

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import random
from main import Pins

def pico_full_speed_main():
    
    # OLED Screen connected to GP14 (SDA) and GP15 (SCL)
    i2c = I2C(Pins.I2C, sda = Pin(Pins.SDA), scl = Pin(Pins.SCL), freq = 400000)
    oled = SSD1306_I2C(128, 64, i2c)

    oled.fill(0)  
    oled.text("Full Speed", 5, 6)
    oled.text("By Kuba", 30, 23)
    oled.text("&", 55, 35)
    oled.text("Stepan", 35, 47)
    oled.rect(0, 0, 128, 20 , 1)
    oled.show()
    time.sleep(2)

    x = 1
    y = 1
    prekazka = 1
    ran = 0
    direction3 = 1
    x_pos = 2
    tilt = 0
    score = 1
    speed= 1
    acceleration = 1
    level = 1
    y_rival = 0
    crasch = 0

    right = Pin(Pins.KEYPAD_LEFT, Pin.IN, Pin.PULL_UP)
    left = Pin(Pins.KEYPAD_RIGHT, Pin.IN, Pin.PULL_UP)

    while True:
    
        oled.fill(0) 
        tilt = 0

        if not left.value():
            # button left pressed
            x_pos = x_pos + 2
            tilt = 4 
  
        if not right.value():
            # button right pressed
            x_pos = x_pos - 2
            tilt = -4
    
        y_rival = ran + y
        oled.text("Score:" + str(score), 0, 0)
        oled.text(str(score * 5) + " km/h", 70, 0)
    
        x = x + 1
        y = y + direction3
        prekazka = prekazka + speed

    
        # horizon
        oled.line(20 + y // 5, 35 + y // 10 , 9 + y // 4 , 39 + y // 10, 1)
        oled.line(20 + y // 5, 35 + y // 10, 29 + y // 4, 39 + y // 10, 1)
        
        # road
        oled.rect(0, 40 + y //10, 128, 2, 1)

        oled.line(50 + y, 40 + y // 10, 30 , 50, 1)
        oled.line(70 + y , 40 + y // 10, 90, 50, 1)
    
        oled.line(30, 50, 10, 63, 1)
        oled.line(90, 50, 118, 63, 1)
    
        oled.rect(0, 42 + x//2, 128, 4, 0)
    
        oled.rect(0, 52 + x, 128, 8, 0)
    
        # your moto
        oled.rect(60 + x_pos, 58, 2, 4, 1)
        oled.rect(59  + x_pos + tilt // 2, 55, 5, 4, 1)

        oled.rect(60 + x_pos + tilt, 52, 2, 2, 1)

        # rival
        if prekazka > 10: 
            oled.rect(60 + ran + y, 38 + prekazka , 2, 4, 1)
            oled.rect(59 + y // 20  + ran + y, 35 + prekazka, 5, 4, 1)

            oled.rect(60 + y // 10  + ran + y, 32 + prekazka, 2, 2, 1)
        
        if prekazka <= 10: 
            oled.rect(60 + ran + y, 38 + prekazka , 2, 4, 1)
    
        oled.show()
    
        if x== 4:  
            x = 0

        if prekazka >= 30:  
            ran = random.randint(-5, 5)
            ran = ran * 2
            prekazka = 0
            score = score + 1
            acceleration = acceleration + 0.05
            speed = round(acceleration)
    

        if y <= -35  or y >= 25:  
            direction3 = -direction3

        if y <= -15:  
            x_pos = x_pos + 2
        
        if y > 15 :  
            x_pos = x_pos - 2
            
        if x_pos >=  46 or x_pos < -46:       
            crasch = 1

        if x_pos <= y_rival + 4  and x_pos >= y_rival - 4 and prekazka >= 15:       
            crasch = 1


        if  crasch ==  1:  
            oled.text("GAME OVER", 25, 26)
            oled.show()
            time.sleep(2)
            return
        
        time.sleep(0.1)
        
if __name__ == "__main__":
    pico_full_speed_main()
