from core import GameObject
from apps.DinoGame.assets import DINO, DINO_DEAD

GROUND_Y = 36
JUMP_VELOCITY = -8
GRAVITY = 1
MAX_FALL_SPEED = 8


class Dino(GameObject):

    def __init__(self, x, y=GROUND_Y):
        super().__init__(DINO, x, y)

        self.vy = 0
        self.is_jumping = False
        self.is_dead = False


    def update(self, current_ms):
        self.vy += GRAVITY

        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        self.y += self.vy

        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vy = 0
            self.is_jumping = False


    def jump(self):
        self.vy = JUMP_VELOCITY
        self.is_jumping = True


    def reset(self):
        self.is_dead = False
        self.sprite = DINO
        self.vy = 0
        self.is_jumping = False


    def die(self):
        self.is_dead = True
        self.sprite = DINO_DEAD
