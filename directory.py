import pygame

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
racket_sprite = pygame.sprite.Group()
blocks_sprite = pygame.sprite.Group()
bonus_sprite = pygame.sprite.Group()
balls_list = []
size = width, height = 560, 800
bonus_dict = {1: 'images/bonus_border.png', 2: 'images/bonus_longer.png', 3: 'images/bonus_+2.png',
              4: 'images/bonus_x2.png', 5: 'images/bonus_star.png',
              6: 'images/bonus_shorter.png', 7: 'images/bonus_bomb.png'}
screen = pygame.display.set_mode(size)
racket_size = [50, 75, 100, 125, 150]
ball_speed = [(-6, 0), (-6, 1), (-6, 2), (-5, 3), (-5, 4), (-4, 5), (-3, 5), (-2, 6)]
blocks_used = {None:0}
