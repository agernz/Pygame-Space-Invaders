import time
import sys
import random as rand
from player import Player
from enemy import Enemy
from fps_util import FPS_util
from score_util import Score_util
from constants import *
from utils import *


if __name__ == '__main__':
    show_fps = 0
    try:
        show_fps = int(sys.argv[1])
    except Exception:
        print('Usage = python main <show_fps>: 1 - yes   0 - no')
        exit(1)

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
background = pygame.transform.scale(load_image('sprites/background.png'),
                                    BACKGROUND_WH)
display.blit(background, (0, 0))
pygame.display.set_caption('Space Invaders')
icon = pygame.transform.scale(load_image('sprites/player.png'),
                              (32, 32))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
level = 1

pygame.mixer.init()
snd_player_shoot = load_sound('sounds/p_shoot.wav')
snd_player_hit = load_sound('sounds/p_explode.wav')
snd_enemy_shoot = load_sound('sounds/enemy_shoot.wav')
snd_enemy_explode = load_sound('sounds/enemy_explode.wav')

all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

score_util = Score_util()
all_sprites.add(score_util)

if show_fps:
    fps_util = FPS_util(pygame, CLOCK_SPEED)
    all_sprites.add(fps_util)

player_img = pygame.transform.scale(load_image('sprites/player.png'),
                                    PLAYER_WH)
player = Player(player_img, DISPLAY_WIDTH / 2.,
                DISPLAY_HEIGHT - (PLAYER_WH[1] / 2.))
player_sprite = pygame.sprite.GroupSingle(player)
all_sprites.add(player)

enemy_images = []
for i in range(1, 5):
    enemy_images.append(pygame.transform.scale(
                        load_image('sprites/alien{0}.png'.format(i)),
                        ENEMY_WH))


def spawn_enemies():
    enemy_y = ENEMY_WH[1]
    enemy_x = ENEMY_WH[0]

    for i in range(NUM_ENEMIES):
        image = rand.randint(0, 3)
        enemy = Enemy(enemy_images[image], ENEMY_SPEED * level,
                      enemy_x, enemy_y)
        enemy_x += ENEMY_WH[0] + ENEMY_WH[0] // 3
        if enemy_x > DISPLAY_WIDTH - ENEMY_WH[0]:
            enemy_x = ENEMY_WH[0]
            enemy_y += ENEMY_WH[1] * 2
        enemy.dir = 180
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)


def erase_dirty(surf, spr_rect):
    surf.blit(background, spr_rect, spr_rect)


def exit(early):
    pygame.mixer.quit()
    pygame.quit()
    if early:
        sys.exit()


def game_over():
    global level
    level = 1
    surf, rect = createText('GAME OVER', DISPLAY_WIDTH // 2,
                            DISPLAY_HEIGHT // 2, ENEMY_BULLET_COLOR, 100)
    display.blit(surf, rect)
    pygame.display.flip()
    time.sleep(3)
    display.blit(background, (0, 0))

    player.reset(1)
    player.rect.center = (DISPLAY_WIDTH / 2.,
                          DISPLAY_HEIGHT - (PLAYER_WH[1] / 2.))
    all_sprites.empty()
    all_sprites.add(player)
    if show_fps:
        all_sprites.add(fps_util)
    all_sprites.add(score_util)
    enemy_sprites.empty()
    player_bullets.empty()
    enemy_bullets.empty()
    spawn_enemies()


def next_level():
    global level
    level += 1
    time.sleep(2)
    player.reset(0)
    player.rect.center = (DISPLAY_WIDTH / 2.,
                          DISPLAY_HEIGHT - (PLAYER_WH[1] / 2.))
    all_sprites.empty()
    all_sprites.add(player)
    if show_fps:
        all_sprites.add(fps_util)
    all_sprites.add(score_util)
    enemy_sprites.empty()
    player_bullets.empty()
    enemy_bullets.empty()
    spawn_enemies()


def process_bullets():
    for bullet in player_bullets:
        if bullet.rect.top < 0:
            all_sprites.remove(bullet)
            player_bullets.remove(bullet)
            player.bullets.append(bullet)
            continue
        for enemy in pygame.sprite.spritecollide(bullet, enemy_sprites, 0):
            enemy.take_damage()
            if enemy.health <= 0:
                pygame.mixer.Sound.play(snd_enemy_explode)
                all_sprites.remove(enemy)
                enemy_sprites.remove(enemy)
                player.score += 10
            all_sprites.remove(bullet)
            player_bullets.remove(bullet)
            player.bullets.append(bullet)

    for bullet in enemy_bullets:
        if bullet.rect.bottom > DISPLAY_HEIGHT:
            all_sprites.remove(bullet)
            enemy_bullets.remove(bullet)
        if (bullet.rect.bottom >= player.rect.top and pygame.
           sprite.spritecollideany(bullet, player_sprite)):
            pygame.mixer.Sound.play(snd_player_hit)
            player.take_damage()
            all_sprites.remove(bullet)
            enemy_bullets.remove(bullet)
            if player.lives <= 0:
                game_over()


spawn_enemies()
running = 1
controls = [0, 0]
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.attack()
                if bullet:
                    pygame.mixer.Sound.play(snd_player_shoot)
                    all_sprites.add(bullet)
                    player_bullets.add(bullet)
            if event.key == pygame.K_a:
                controls[0] = 1
            elif event.key == pygame.K_d:
                controls[1] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = 0
            elif event.key == pygame.K_a:
                controls[0] = 0
            elif event.key == pygame.K_d:
                controls[1] = 0

    new_dir = 180 * controls[0] + 1 * controls[1]
    if new_dir != 181:
        player.dir = new_dir

    process_bullets()

    for enemy in enemy_sprites:
        bullet = enemy.attack(len(enemy_sprites))
        if bullet:
            pygame.mixer.Sound.play(snd_enemy_shoot)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        if enemy.rect.bottom > player.rect.top:
            game_over()

    all_sprites.clear(display, erase_dirty)
    score_util.score = player.score
    all_sprites.update()
    all_sprites.draw(display)
    pygame.display.flip()

    if len(enemy_sprites) == 0:
        next_level()

    clock.tick(CLOCK_SPEED)

exit(0)
