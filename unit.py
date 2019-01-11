from abc import ABC, abstractmethod
from constants import pygame


class Unit(ABC, pygame.sprite.Sprite):

    def __init__(self, image, health, speed, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = image
        self.image = image
        self.health = health
        self.speed = speed
        self.rect = image.get_rect()
        self.dir = -1
        self.rect.center = (init_x, init_y)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def take_damage(self):
        pass

    @abstractmethod
    def attack(self):
        pass
