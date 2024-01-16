import pygame
from directory import all_sprites, racket_sprite, horizontal_borders, bonus_sprite, \
    width, balls_list, racket_size
from ball import Ball
from borders import Border


class Racket(pygame.sprite.Sprite):
    def __init__(self, x, y, width, length, ind, lives=3):
        super().__init__(all_sprites)
        self.length = length
        self.lives = lives
        self.stars = 0
        self.ind = ind
        self.width = width
        self.flag = False
        self.add(racket_sprite)
        self.border = None
        self.image = pygame.Surface((length, width), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, length, width)
        pygame.draw.rect(self.image, (245, 141, 0),
                         pygame.Rect(0, 0, length, width))
        self.v = 0

    def new_action(self, direction):
        self.v = direction * 8

    def update(self):
        self.rect = self.rect.move(self.v, 0)
        if self.rect.x + self.length // 2 < 25:
            self.rect.x = 25 - self.length // 2
        elif self.rect.x + self.length // 2 > width - 25:
            self.rect.x = width - 25 - self.length // 2
        if pygame.sprite.spritecollideany(self, bonus_sprite):
            bonuses = pygame.sprite.spritecollide(self, bonus_sprite, True)
            for bonus in bonuses:
                all_sprites.remove(bonus)
                if bonus.purpose == 1:
                    for i in horizontal_borders:
                        if i.bonus:
                            horizontal_borders.remove(i)
                            all_sprites.remove(i)
                    border = Border(25, 750, 535, 750, 1, bonus=True)
                    pygame.time.set_timer(pygame.USEREVENT, 7000)
                    self.flag = True
                    self.border = border
                elif bonus.purpose == 2:
                    self.ind += 1
                    if self.ind > 4:
                        self.ind = 4
                    self.rect = pygame.Rect(self.rect.x + self.length // 2 - racket_size[self.ind] // 2, self.rect.y,
                                            racket_size[self.ind], self.width)
                    self.length = racket_size[self.ind]
                    self.image = pygame.Surface((self.length, self.width), pygame.SRCALPHA, 32)
                    pygame.draw.rect(self.image, (245, 141, 0),
                                     pygame.Rect(0, 0, self.length, self.width))
                elif bonus.purpose == 3:
                    ball1 = Ball(5, bonus.rect.x + 10, bonus.rect.y + 5)
                    ball2 = Ball(5, bonus.rect.x + 10, bonus.rect.y + 5)
                    ball1.vy = ball2.vy = -4
                    ball1.vx = -4
                    ball2.vx = 4
                elif bonus.purpose == 4:
                    arr = balls_list[::]
                    speed = [(-6, -1), (-6, -2), (-5, -3), (-5, -4), (-4, -4), (-4, -5), (-3, -5), (-2, -6), (-1, -6),
                             (0, -6),
                             (1, -6), (2, -6), (3, -5), (4, -5), (4, -4), (5, -4), (5, -3), (6, -2), (6, -1)]
                    for i in speed[::-1]:
                        speed.append((i[0], -i[1]))
                    for ball in arr:
                        balls_list.remove(ball)
                        all_sprites.remove(ball)
                        ball1 = Ball(5, ball.rect.x, ball.rect.y)
                        ball2 = Ball(5, ball.rect.x, ball.rect.y)
                        ind = speed.index((ball.vx, ball.vy))
                        ind1 = (ind + 4) % len(speed)
                        ind2 = (ind - 4) % len(speed)
                        ball1.vx, ball1.vy = speed[ind1]
                        ball2.vx, ball2.vy = speed[ind2]
                elif bonus.purpose == 5:
                    self.stars += 1
                elif bonus.purpose == 6:
                    self.ind -= 1
                    if self.ind < 0:
                        self.ind = 0
                    self.rect = pygame.Rect(self.rect.x + self.length // 2 - racket_size[self.ind] // 2, self.rect.y,
                                            racket_size[self.ind], self.width)
                    self.length = racket_size[self.ind]
                    self.image = pygame.Surface((self.length, self.width), pygame.SRCALPHA, 32)
                    pygame.draw.rect(self.image, (245, 141, 0),
                                     pygame.Rect(0, 0, self.length, self.width))
                else:
                    self.lives -= 1
