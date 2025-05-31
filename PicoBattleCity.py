import framebuf
from time import ticks_diff, ticks_ms
from random import randint

from PicoGame import PicoGame
from BattleCity.PlayerTank import PlayerTank
from BattleCity.EnemyTank import EnemyTank
from BattleCity.Tank import Direction


def battle_city():
    game = PicoGame()
    last_button_debounce = -1
    
    x, y = game.get_center(4, 4)
    player = PlayerTank(x, y)
    
    last_enemy_deploy_ms = ticks_ms()
    enemy_tanks = []
    
    
    while True:
        # exit game loop
        if game.button_B():
            break
        
        # update states
        player.update()
        
        # render
        game.fill(0)
        player.render(game)
        game.show()
        
        # inputs
        debounce_delta = ticks_diff(ticks_ms(), last_button_debounce) >= 300
        if game.button_A() and debounce_delta:
            last_button_debounce = ticks_ms()
            player.fire()    
        if game.button_up():
            player.up()
        elif game.button_right():
            player.right()
        elif game.button_down():
            player.down()
        elif game.button_left():
            player.left()
                


if __name__ == '__main__':
    battle_city()