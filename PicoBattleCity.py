import framebuf
from time import ticks_diff, ticks_ms
from random import randint

from PicoGame import PicoGame
from BattleCity.PlayerTank import PlayerTank
from BattleCity.EnemyTank import EnemyTank
from BattleCity.Tank import Direction


def battle_city():
    game = PicoGame()
    
    button_delay = 300
    last_button_debounce = -1
    
    x, y = game.get_center(0, 0)
    player = PlayerTank(x+20, y+20)
    
    last_enemy_deploy_ms = ticks_ms()
    enemy_tanks = [EnemyTank(-1, x, y)]
    
    
    while True:
        # exit game loop
        if game.button_B():
            break
        
        # render
        game.fill(0)
        # update states
        player.update()
        player.render(game)
        game.hline(0, player.y-4, PicoGame.SCREEN_WIDTH, 1) # player
        for enemy in enemy_tanks:
        #    enemy.update(player)
            enemy.render(game)
            game.hline(0, enemy.y+4, PicoGame.SCREEN_WIDTH, 1) # enemy
        game.show()
        
        # inputs
        debounce_delta = ticks_diff(ticks_ms(), last_button_debounce)
        if game.button_A() and debounce_delta >= button_delay:
            last_button_debounce = ticks_ms()
            player.shoot()    
        if game.button_up():
            player.up(enemy_tanks)
        elif game.button_right():
            player.right(enemy_tanks)
        elif game.button_down():
            player.down(enemy_tanks)
        elif game.button_left():
            player.left(enemy_tanks)
                


if __name__ == '__main__':
    battle_city()