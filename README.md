# picon

Mini retro console using RP2040 (WaveShare RP2040 Zero)

Code and games for the Raspberry Pi Pico RetroGaming System
* [YouTube video](https://youtu.be/VYeIR5n5Few)
* [Assembly instructions](https://www.youmaketech.com/raspberry-pi-pico-retrogaming-system/)


Files
=====
Forked from [YouMakeTech](https://github.com/YouMakeTech/PicoRetroGamingSystem)

* PicoPong.py: a simple Pong game
* PicoInvaders.py: A simplified Space Invaders game
* PicoInvadersPnp: A Space Invaders game by Print N'Play (Original source code from https://github.com/printnplay/Pico-MicroPython)
* PicoSnake.py: A snake game by Twan37 (Original source code from https://github.com/Twan37/PicoSnake)
  * Snake now has two segments intially.
* PicoDino.py: A Dino game port by tyrkelko
* Pico2048.py: A 2048 game port by tyrkelko
* PicoTetris.py: A tetris clone game port by tyrkelko
* PicoFullSpeed.py: A moto game by Kuba & Stepan (Original source code from https://github.com/Hellmole/Raspberry-pi-pico-games)
  * I switched the Right and Left buttons for more natural turning.
* PicoLunarModule.py: A lunar module game by Kuba & Stepan (Original source code from https://github.com/Hellmole/Raspberry-pi-pico-games)
* PicoGame.py: A class to easily write games for the Raspberry Pi Pico RetroGaming System (used by some games)
  * Modified pins to match my console.
* ss1306py.py: Official MicroPython SSD1306 OLED driver, I2C and SPI interfaces
* other files are written by me

How to use
==========
* Install MicroPython on your RP2040 board
* Copy the files to the root directory of your RP2040 board
* Restart
* Enjoy!
