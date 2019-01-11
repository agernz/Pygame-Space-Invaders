from unit import Unit
from bullet import Bullet
import numpy as np
import pygame.surfarray as surfarray
from constants import (PLAYER_BULLET_COLOR, NUM_PLAYER_BULLETS, PLAYER_LIVES,
                       PLAYER_BULLET_SPEED, PLAYER_HEALTH, PLAYER_SPEED,
                       DISPLAY_WIDTH, ANIM_FRAMES)


class Player(Unit):

    def __init__(self, image, init_x, init_y):
        self.lives = PLAYER_LIVES
        self.score = 0
        self.anim = 0
        self.anim_frames = 0
        self.damaged = np.array(surfarray.array3d(image))
        self.damaged[:, :, 1:] = 0
        self.damaged = surfarray.make_surface(self.damaged)
        self.bullets = [Bullet(PLAYER_BULLET_COLOR, PLAYER_BULLET_SPEED, 90)
                        for i in range(NUM_PLAYER_BULLETS)]
        super().__init__(image, PLAYER_HEALTH, PLAYER_SPEED, init_x, init_y)

    def update(self):
        if self.dir == 180 and self.rect.left > 0:
            x_offset = min(self.speed, self.rect.left)
            self.rect.move_ip(-x_offset, 0)
        elif self.dir == 1 and self.rect.right < DISPLAY_WIDTH:
            x_offset = min(self.speed, DISPLAY_WIDTH - self.rect.right)
            self.rect.move_ip(x_offset, 0)
        self.animate()

    def take_damage(self):
        self.anim_frames = 0
        self.image = self.damaged
        self.health -= 1
        if self.health <= 0:
            self.lives -= 1
        self.health = PLAYER_HEALTH

    def attack(self):
        bullet = None
        if len(self.bullets) > 0:
            bullet = self.bullets.pop()
            bullet.fire(self.rect.midtop)
        return bullet

    def reset(self, game_over):
        self.image = self.base_image
        if game_over:
            self.score = 0
            self.lives = PLAYER_LIVES
        self.bullets = [Bullet(PLAYER_BULLET_COLOR, PLAYER_BULLET_SPEED, 90)
                        for i in range(NUM_PLAYER_BULLETS)]

    def animate(self):
        if self.anim_frames < ANIM_FRAMES:
            self.anim_frames += 1
        elif self.image != self.base_image:
            self.image = self.base_image
