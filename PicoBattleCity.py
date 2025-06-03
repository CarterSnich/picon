from time import ticks_diff, ticks_ms, sleep_ms
from random import randint, choice

from PicoGame import PicoGame
from BattleCity.Tank import Direction
from BattleCity.PlayerTank import PlayerTank
from BattleCity.EnemyTank import EnemyTank

MAX_ENEMY_COUNT = 4

def battle_city():
    game = PicoGame()

    score = 0
    bullets = []
    
    x, y = game.get_center(0, 0)
    player = PlayerTank(x, y)
    
    enemy_tanks = []
    last_enemy_spawn_ms = ticks_ms()
    last_enemy_hit_ms = -1
    
    while True:
        # exit game loop
        if game.button_B():
            break
        
        tick = ticks_ms()
        player_shot_delta = ticks_diff(tick, player.last_shot_ms)
        enemy_hit_delta = ticks_diff(tick, last_enemy_hit_ms)
        if player_shot_delta >= 50 and enemy_hit_delta >= 50:
            game.sound(0)
        
        # state updates
        for b in bullets:
            if b.update():
                if b.from_player:
                    player.shots -= 1
                bullets.remove(b)
                continue
            if b.from_player:
                for et in enemy_tanks:
                    if b.is_colliding(et.x-2, et.y-2, 9, 9):
                        game.sound(1000)
                        last_enemy_hit = ticks_ms()
                        enemy_tanks.remove(et)
                        bullets.remove(b)
                        score += 1
                        player.shots -= 1
                        break
                else:
                    continue
                break
            else:
                if b.is_colliding(player.x-2, player.y-2, 9, 9):
                    game.over()
                    return
            
        for et in enemy_tanks:
            if et.can_shoot():
                bullets.append(et.shoot())
                
            if et.will_collide(player.x, player.y, 8, 8):
                et.change_direction()
            else:
                et.update()
                
                
        # spawn enemy
        delta_passed = ticks_diff(ticks_ms(), last_enemy_hit_ms) >= 1000 and \
            ticks_diff(ticks_ms(), last_enemy_spawn_ms) >= 1000
        if len(enemy_tanks) < MAX_ENEMY_COUNT and delta_passed:
            last_enemy_spawn_ms = ticks_ms()
            while True:
                x = randint(4, game.SCREEN_WIDTH-4)
                y = randint(4, game.SCREEN_HEIGHT-4)
                
                is_intersecting = game.sprites_intersection(
                    x, y, 8, 8,
                    player.x, player.y, 8, 8
                )
                
                if not is_intersecting:
                    break
            enemy_tanks.append(EnemyTank(x, y, randint(0, 3)))
        
            
        # render
        game.fill(0)
        game.blit(player.get_sprite(), player.x-4, player.y-4)
        for e in enemy_tanks:
            game.blit(e.get_sprite(), e.x-4, e.y-4)
        for b in bullets:
            game.blit(b.get_sprite(), b.x-1, b.y-1)
        game.top_right_corner_text(str(score))
        game.show()
        
        # inputs
        if game.button_A() and player.can_shoot():
            game.sound(880)
            bullets.append(player.shoot())
        if game.button_up():
            player.move(Direction.NORTH, enemy_tanks)
        elif game.button_right():
            player.move(Direction.EAST, enemy_tanks)
        elif game.button_down():
            player.move(Direction.SOUTH, enemy_tanks)
        elif game.button_left():
            player.move(Direction.WEST, enemy_tanks)
                


if __name__ == '__main__':
    battle_city()