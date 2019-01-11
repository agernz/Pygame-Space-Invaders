from constants import pygame, BULLET_WH


class Bullet(pygame.sprite.Sprite):

    def __init__(self, color, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(BULLET_WH)
        self.image.fill(color)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.dir = direction
        self.rect.center = (-15, -15)

    def update(self):
        if self.dir == 90:
            self.rect.move_ip(0, -self.speed)
        elif self.dir == 270:
            self.rect.move_ip(0, self.speed)

    def fire(self, coords):
        self.rect.center = coords
