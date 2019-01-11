import time
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from utils import pygame, createText


class FPS_util(pygame.sprite.Sprite):

    def __init__(self, pygame, target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.frames = 0
        self.t1 = time.time()
        self.fps = target
        self.image, self.rect = createText(str(self.fps),
                                           DISPLAY_WIDTH - 20,
                                           20, (0, 200, 0),
                                           DISPLAY_HEIGHT // 40)

    def update(self):
        self.frames += 1
        if self.frames >= self.target:
            t_now = time.time()
            self.fps = self.frames / (t_now - self.t1)
            self.t1 = t_now
            self.frames = 0
            self.image, self.rect = createText(str(int(self.fps)),
                                               DISPLAY_WIDTH - 20,
                                               20, (0, 200, 0),
                                               DISPLAY_HEIGHT // 40)
