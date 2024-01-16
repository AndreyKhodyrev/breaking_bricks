import pygame
from directory import all_sprites, racket_sprite, horizontal_borders, vertical_borders, blocks_sprite, width, height, \
    size


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, length, purpose, color, ind, bonus=-1):
        super().__init__(all_sprites)
        self.ind = ind
        self.purpose = purpose
        self.bonus = bonus
        self.x, self.y = x, y
        self.length = length
        self.width = width
        self.add(blocks_sprite)
        self.l_x = Border(x, y, x, y + self.width, 1, ind, 1, purpose)
        self.r_x = Border(x + self.length, y, x + self.length, y + self.width, 1, ind, 2, purpose)
        self.up_y = Border(x, y, x + self.length, y, 1, ind, 1, purpose)
        self.dn_y = Border(x, y + self.width, x + self.length, y + self.width, 1, ind, 2, purpose)
        self.image = pygame.Surface((length, width), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, length, width)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, length, width))
        self.v = 0


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, length, own=None, orient=4, purpose = -2, bonus = False):
        super().__init__(all_sprites)
        self.own = own
        self.bonus = bonus
        self.purpose = purpose
        self.orient = orient
        self.length = length
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([length, y2 - y1])
            self.rect = pygame.Rect(x1, y1, length, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, length])
            self.rect = pygame.Rect(x1, y1, x2 - x1, length)
