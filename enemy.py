import random as rand
from unit import Unit
from bullet import Bullet
from constants import (ENEMY_FIRE_CHANCE, ENEMY_BULLET_SPEED, ENEMY_HEALTH,
                       ENEMY_BULLET_COLOR, DISPLAY_WIDTH)


class Enemy(Unit):

    def __init__(self, image, speed, init_x, init_y):
        self.just_fired = 0
        super().__init__(image, ENEMY_HEALTH, speed, init_x, init_y)

    def update(self):
        if self.dir == 180 and self.rect.left > 0:
            x_offset = min(self.speed, self.rect.left)
            self.rect.move_ip(-x_offset, 0)
        elif self.dir == 0 and self.rect.right < DISPLAY_WIDTH:
            x_offset = min(self.speed, DISPLAY_WIDTH - self.rect.right)
            self.rect.move_ip(x_offset, 0)
        elif self.dir == 180:
            self.dir = 0
            self.rect.move_ip(0, self.rect.height)
        elif self.dir == 0:
            self.dir = 180
            self.rect.move_ip(0, self.rect.height)

    def take_damage(self):
        self.health -= 1

    def attack(self, num_enemies):
        bullet = None
        chance = rand.random()
        if chance < (ENEMY_FIRE_CHANCE / num_enemies) and not self.just_fired:
            bullet = Bullet(ENEMY_BULLET_COLOR, ENEMY_BULLET_SPEED, 270)
            bullet.fire(self.rect.midbottom)
            self.just_fired = 1
        elif chance < ENEMY_FIRE_CHANCE:
            self.just_fired = 0
        return bullet
