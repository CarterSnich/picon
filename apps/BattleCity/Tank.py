from apps.BattleCity.direction import Direction
from core import GameObject, Sprite, SCREEN_WIDTH, SCREEN_HEIGHT


class Tank(GameObject):

    def __init__(self, sprites: dict[Direction, Sprite], x, y, direction, speed=1):

        self.direction = direction
        self.speed = speed
        self.sprites = sprites
        self.bullet_count = 0

        super().__init__(self.sprites[direction], x, y)


    def move(self, direction: Direction, obstacles: list[GameObject]):
        if self.direction != direction:
            self.direction = direction
            self.sprite = self.sprites[direction]
            return

        dx, dy = direction

        new_x = min(max(0, self.x + dx * self.speed), SCREEN_WIDTH - self.sprite.width)
        new_y = min(max(0, self.y + dy * self.speed), SCREEN_HEIGHT - self.sprite.height)

        old_x, old_y = self.x, self.y

        # Temporarily move for collision testing
        self.x = new_x
        self.y = new_y

        for obs in obstacles:
            if obs is not self and self.is_colliding(obs, box_collision=True):
                self.x = old_x
                self.y = old_y
                return
