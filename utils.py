from constants import pygame


def load_image(img_path):
    try:
        image = pygame.image.load(img_path)
    except pygame.error:
        raise SystemExit('Could not load image "%s": %s' % (img_path,
                         pygame.get_error()))
    return image.convert_alpha()


def load_sound(sound_path):
    if not pygame.mixer:
        class dummysound:
            def play(self):
                pass
        return dummysound()
    try:
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except pygame.error:
        print('Warning, unable to load, "%s": %s' % (sound_path,
              pygame.get_error()))
    return dummysound()


def createText(text, x, y, color, size):
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    textsurface = fontObj.render(text, True, color, (255, 255, 255, 0))
    textsurface.set_colorkey((255, 255, 255))
    textRectObj = textsurface.get_rect()
    textRectObj.center = (x, y)
    return textsurface, textRectObj
