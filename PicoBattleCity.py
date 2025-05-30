import framebuf
from time import ticks_diff, ticks_ms

from PicoGame import PicoGame
from BattleCity.PlayerTank import PlayerTank
# from BattleCity.EnemyTank import EnemyTank
from BattleCity.Tank import Direction


def battle_city():
    game = PicoGame()
    
    x, y = game.get_center(4, 4)
    player = PlayerTank(x, y)
    
    last_button_debounce = -1
    
    while True:
        player.update()
        
        game.fill(0)
        game.blit(player.get_sprite(), player.x, player.y)
        
        for pb in player.bullets:
            game.pixel(pb[0], pb[1], 1)
        
        game.show()
        
        debounce_delta = ticks_diff(ticks_ms(), last_button_debounce) >= 300
        
        if game.button_A() and debounce_delta:
            last_button_debounce = ticks_ms()
            player.fire()  
        elif game.button_up():
            last_button_debounce = ticks_ms()
            player.up()
        elif game.button_right():
            last_button_debounce = ticks_ms()
            player.right()
        elif game.button_down():
            last_button_debounce = ticks_ms()
            player.down()
        elif game.button_left():
            last_button_debounce = ticks_ms()
            player.left()
                


if __name__ == '__main__':
    battle_city()