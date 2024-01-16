import pygame
from directory import all_sprites, bonus_sprite, bonus_dict


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, purpose):
        super().__init__(all_sprites)
        self.add(bonus_sprite)
        self.purpose = purpose
        self.image = pygame.transform.scale(pygame.image.load(bonus_dict[purpose]), (20,20))
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        if purpose not in [5, 7]:
            self.v = 1
        else:
            self.v = 4

    def update(self):
        self.rect = self.rect.move(0, self.v)
