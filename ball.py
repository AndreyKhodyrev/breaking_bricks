import pygame
import math
from directory import all_sprites, racket_sprite, horizontal_borders, vertical_borders, blocks_sprite, balls_list, \
    ball_speed, blocks_used
from bonus import Bonus


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.s = 1
        balls_list.append(self)
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (255, 255, 255),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 0
        self.vy = -6
        self.v = self.vy

    def remove(self, border):
        if border.own and border.purpose == 1:
            for i in horizontal_borders:
                if i.own == border.own:
                    horizontal_borders.remove(i)
                    all_sprites.remove(i)
            for i in vertical_borders:
                if i.own == border.own:
                    vertical_borders.remove(i)
                    all_sprites.remove(i)
            for i in blocks_sprite:
                if i.ind == border.own:
                    block = i
            blocks_sprite.remove(block)
            all_sprites.remove(block)
            if block.bonus != 0:
                Bonus(block.x + block.length // 2, block.y + block.width // 2, block.bonus)

    def update(self):
        flag2 = False
        flag3 = False
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            borders = pygame.sprite.spritecollide(self, horizontal_borders, False)
            border = False
            t = False
            for i in borders:
                flag = False
                for j in blocks_sprite:
                    if i.orient == 1:
                        if j.ind == (i.own[0] - 1, i.own[1]):
                            flag = True
                            break
                    elif i.orient == 2:
                        if j.ind == (i.own[0] + 1, i.own[1]):
                            flag = True
                            break
                    else:
                        border = i
                        t = True
                        break
                if not t and not flag and ((self.vy > 0 and i.orient == 1) or (self.vy < 0 and i.orient == 2)):
                    border = i
                    break
            if border:
                self.remove(border)
                if blocks_used[border.own] != 1 or ((border.orient == 3 and self.vy < 0)or(border.orient == 4 and self.vy > 0)):
                    for i in blocks_used.keys():
                        blocks_used[i] = 0
                    blocks_used[border.own] = 1
                    self.vy = -self.vy
                flag3 = True
            else:
                flag2 = True

        else:
            flag2 = True
        if pygame.sprite.spritecollideany(self, vertical_borders) and flag2:
            borders = pygame.sprite.spritecollide(self, vertical_borders, False)
            border = False
            t = False
            for i in borders:
                flag = False
                for j in blocks_sprite:
                    if i.orient == 1:
                        if j.ind == (i.own[0], i.own[1] - 1):
                            flag = True
                            break
                    elif i.orient == 2:
                        if j.ind == (i.own[0], i.own[1] + 1):
                            flag = True
                            break
                    else:
                        border = i
                        t = True
                        break
                if not t:
                    if not flag and ((self.vx > 0 and i.orient == 1) or (self.vx < 0 and i.orient == 2)):
                        border = i
                        break
            if border:
                self.remove(border)
                if blocks_used[border.own] != 1 or ((border.orient == 3 and self.vx < 0)or(border.orient == 4 and self.vx > 0)):
                    for i in blocks_used.keys():
                        blocks_used[i] = 0
                    blocks_used[border.own] = 1
                    self.vx = -self.vx
                flag3 = True
        if pygame.sprite.spritecollideany(self, racket_sprite):
            flag3 = True
            racket = pygame.sprite.spritecollideany(self, racket_sprite)
            b_x, r_x, b_y, r_y = self.rect.x + self.radius, racket.rect.x, self.rect.y + self.radius, racket.rect.y
            if (b_x > r_x + racket.length and self.vx < 0) or (b_x < r_x and self.vx > 0):
                self.vx = -self.vx
            elif b_y > r_y + racket.width:
                self.vy = -self.vy
            else:
                leng = abs((r_x + racket.length // 2) - b_x)
                segment = racket.length // 2 // 8
                koef = -1
                if (r_x + racket.length // 2) < b_x:
                    koef = 1
                ind = leng // segment
                if ind > 7:
                    ind = 7
                self.vy, self.vx = ball_speed[ind][0], ball_speed[ind][1] * koef
        self.rect = self.rect.move(self.vx, self.vy)
        if not flag3:
            for i in blocks_used.keys():
                blocks_used[i] = 0
        if self.rect.y >= 760:
            all_sprites.remove(self)
            try:
                balls_list.remove(self)
            except:
                pass
