from utils import pygame, createText
from constants import DISPLAY_HEIGHT


class Score_util(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.image, self.rect = createText("Score: {0}".format(self.score),
                                           60, 20, (0, 200, 0),
                                           DISPLAY_HEIGHT // 40)

    def update(self):
        self.image, self.rect = createText("Score: {0}".format(self.score),
                                           60, 20, (0, 200, 0),
                                           DISPLAY_HEIGHT // 40)
