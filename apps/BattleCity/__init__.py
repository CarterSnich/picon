__NAME__ = "Battle City"
__CATEGORY__ = "games"

from random import randrange

from apps.BattleCity.bullet import Bullet
from apps.BattleCity.direction import Direction
from apps.BattleCity.enemy_tank import EnemyTank
from apps.BattleCity.player_tank import PlayerTank
from core import PiconGame, has_elapsed, randbool
from core.helper import get_center_y
from core.input import Key

PLAYER_MOVE_INTERVAL_MS = 20
PLAYER_SHOOT_INTERVAL_MS = 300

MAX_ENEMY_COUNT = 4
ENEMY_MOVEMENT_INTERVAL_MS = 500
ENEMY_SPAWN_INTERVAL_MS = 3000
ENEMY_SPAWN_POINTS = ((0, 0, Direction.EAST),  # top left
                      (60, 0, Direction.SOUTH),  # top center
                      (120, 0, Direction.SOUTH),  # top right
                      (120, 56, Direction.WEST),  # bottom right
                      (60, 56, Direction.NORTH),  # bottom center
                      (0, 56, Direction.NORTH))  # bottom left
ENEMY_HIT_SOUND_FREQ = 550

BULLET_MOVEMENT_INTERVAL_MS = 10


class Main(PiconGame):

    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.input.set_debounce(0)

        center_x, center_y = 28, get_center_y(8)
        self.player = PlayerTank(center_x, center_y)
        self.last_player_move_ms = self.current_ms
        self.last_player_shoot_ms = self.current_ms

        self.enemy_tanks: list[EnemyTank] = []
        self.last_enemy_spawn_ms = self.current_ms

        self.bullets: list[Bullet] = []

        self.last_tone_ms = 0


    def inputs(self):
        if has_elapsed(self.current_ms, self.last_player_move_ms, PLAYER_MOVE_INTERVAL_MS):
            if self.input.is_pressed(Key.UP):
                self.player.move(Direction.NORTH, self.enemy_tanks)
                self.last_player_move_ms = self.current_ms
            elif self.input.is_pressed(Key.RIGHT):
                self.player.move(Direction.EAST, self.enemy_tanks)
                self.last_player_move_ms = self.current_ms
            elif self.input.is_pressed(Key.DOWN):
                self.player.move(Direction.SOUTH, self.enemy_tanks)
                self.last_player_move_ms = self.current_ms
            elif self.input.is_pressed(Key.LEFT):
                self.player.move(Direction.WEST, self.enemy_tanks)
                self.last_player_move_ms = self.current_ms

        if has_elapsed(self.current_ms, self.last_player_shoot_ms, PLAYER_SHOOT_INTERVAL_MS):
            if self.input.is_pressed(Key.A) and self.player.bullet_count < 3:
                self.bullets.append(Bullet(self.player))
                self.player.bullet_count += 1
                self.last_player_shoot_ms = self.current_ms
                self.sound.tone()
                self.last_tone_ms = self.current_ms


    def update(self):
        # Sound off
        if has_elapsed(self.current_ms, self.last_tone_ms, 20):
            self.sound.stop()

        # Enemy tanks
        for et in self.enemy_tanks:
            if has_elapsed(self.current_ms, et.last_move_ms, ENEMY_MOVEMENT_INTERVAL_MS):
                et.update(self.current_ms, self.enemy_tanks + [self.player])
                et.last_move_ms = self.current_ms
                if randbool() and et.bullet_count < 3:
                    self.bullets.append(Bullet(et))
                    et.bullet_count += 1

        # Spawn enemy tank
        if (has_elapsed(self.current_ms, self.last_enemy_spawn_ms, ENEMY_SPAWN_INTERVAL_MS) and
                len(self.enemy_tanks) < MAX_ENEMY_COUNT):
            if self.spawn_enemy():
                self.last_enemy_spawn_ms = self.current_ms

        # Bullets
        i = 0
        while i < len(self.bullets):
            bullet = self.bullets[i]

            if has_elapsed(self.current_ms, bullet.last_move_ms, BULLET_MOVEMENT_INTERVAL_MS):
                bullet.last_move_ms = self.current_ms
                bullet.update()

                if bullet.is_offscreen():
                    bullet.owner.bullet_count -= 1
                    self.bullets.pop(i)
                    continue

                if bullet.owner is self.player:
                    removed = False
                    for et in self.enemy_tanks:
                        if bullet.is_colliding(et):
                            self.enemy_tanks.remove(et)
                            bullet.owner.bullet_count -= 1
                            self.bullets.pop(i)
                            removed = True
                            self.sound.tone(550)
                            break
                    if removed:
                        continue
                else:
                    if bullet.is_colliding(self.player):
                        self.game_over()
                        return
            i += 1


    def render(self):
        self.player.draw(self.display)

        for et in self.enemy_tanks:
            et.draw(self.display)

        for b in self.bullets:
            b.draw(self.display)


    def spawn_enemy(self):
        x, y, d = ENEMY_SPAWN_POINTS[randrange(4)]
        new_et = EnemyTank(x, y, d)

        for et in self.enemy_tanks:
            if et.is_colliding(new_et):
                return False

        self.enemy_tanks.append(new_et)
        return True


if __name__ == "__main__":
    from core import Display, Input, Sound

    Main(Display(), Input(), Sound()).run()
