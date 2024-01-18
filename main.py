import pygame
import csv
import random
import sqlite3
from ball import Ball
from directory import all_sprites, racket_sprite, horizontal_borders, vertical_borders, blocks_sprite, bonus_sprite, \
    width, height, \
    size, balls_list, screen, blocks_used
from racket import Racket
from button import Button
from borders import Border, Block
from bonus import Bonus

con = sqlite3.connect("data_base.db")
cur = con.cursor()
pygame.display.set_caption('Breaking bricks')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def make_field(markup, bonuses):
    for i in range(len(markup)):
        for j in range(len(markup[i])):
            if markup[i][j][0] != 0:
                if markup[i][j][0] == -1:
                    Block(25 + j * 10, 40 + i * 10, 10, 10, markup[i][j][0], markup[i][j][1], (i, j))
                else:
                    num = random.choice(bonuses)
                    Block(25 + j * 10, 40 + i * 10, 10, 10, markup[i][j][0], markup[i][j][1], (i, j), num)
                    bonuses.remove(num)
                blocks_used[(i, j)] = 0


def redraw(racket):
    all_sprites.draw(screen)
    if racket.flag:
        pygame.draw.rect(screen, (245, 141, 0), (25, 750, 510, 10))
    pygame.draw.rect(screen, (67, 9, 81), (0, 760, 560, 40), 0)
    pygame.draw.rect(screen, (67, 9, 81), (0, 0, 25, 800), 0)
    pygame.draw.rect(screen, (67, 9, 81), (536, 0, 25, 800), 0)
    pygame.draw.rect(screen, (67, 9, 81), (25, 50, 510, 9), 0)
    if racket.lives == 1:
        screen.blit(heart_image, (500, 5))
    elif racket.lives == 2:
        screen.blit(heart_image, (500, 5))
        screen.blit(heart_image, (470, 5))
    else:
        screen.blit(heart_image, (500, 5))
        screen.blit(heart_image, (470, 5))
        screen.blit(heart_image, (440, 5))
    if racket.stars >= 1:
        screen.blit(star_image, (502, 32))
    if racket.stars >= 2:
        screen.blit(star_image, (472, 32))
    if racket.stars >= 3:
        screen.blit(star_image, (442, 32))
    pygame.display.flip()


def star_dict(window_pos):
    arr = cur.execute("SELECT * FROM levels").fetchall()
    stars_dict = {}
    for j in arr:
        stars_dict[j[0]] = j[window_pos - 2]
    return stars_dict


def waiting(running, racket):
    t = False
    while running:
        screen.fill((67, 9, 81))
        pygame.draw.rect(screen, (36, 9, 89), (25, 60, 510, 700), 0)
        redraw(racket)
        flag = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    t = True
            if event.type == pygame.KEYUP and t:
                if event.key == pygame.K_SPACE:
                    flag = False
        if not flag:
            break
    return running


pygame.init()

level_paw = ''
colors_dict = {0: (-1, -1, -1), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (255, 255, 0), 5: (255, 128, 0),
               6: (0, 255, 255),
               7: (255, 0, 255), 8: (128, 255, 0), 9: (128, 0, 255), 10: (149, 149, 149), 11: (0, 128, 255),
               12: (255, 255, 255)}
play_button = Button(136, 250, pygame.image.load("images/button_play.png").convert_alpha(), 1)
settings_button = Button(136, 380, pygame.image.load("images/button_settings.png").convert_alpha(), 1)
exit_button = Button(136, 510, pygame.image.load("images/button_exit.png").convert_alpha(), 1)
back_button = Button(10, 10, pygame.image.load("images/button_back.png").convert_alpha(), 1)
easy_button = Button(136, 250, pygame.image.load("images/button_easy.png").convert_alpha(), 1)
normal_button = Button(136, 380, pygame.image.load("images/button_normal.png").convert_alpha(), 1)
hard_button = Button(136, 510, pygame.image.load("images/button_hard.png").convert_alpha(), 1)
heart_image = pygame.image.load('images/heart.png').convert_alpha()
star_image = pygame.image.load('images/bonus_star.png').convert_alpha()
lock_image = pygame.transform.scale(pygame.image.load('images/lock.png').convert_alpha(), (100, 100))
level_buttons = []
for i in range(3):
    level_buttons.append(Button(136, 250 + i * 130,
                                pygame.image.load("images/level-{0}.png".format(i + 1)).convert_alpha(), 1))
clock = pygame.time.Clock()
window_pos = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if window_pos == 0:
        screen.fill((52, 78, 91))
        draw_text("Breaking bricks", pygame.font.SysFont("Arial Black", 55), (255, 255, 255), 40, 60)
        if play_button.draw(screen):
            window_pos = 1
        if settings_button.draw(screen):
            window_pos = 2
        if exit_button.draw(screen):
            running = False
    elif window_pos == 1:
        screen.fill((52, 78, 91))
        if back_button.draw(screen):
            window_pos = 0
        if easy_button.draw(screen):
            window_pos = 3
        if normal_button.draw(screen):
            window_pos = 4
        if hard_button.draw(screen):
            window_pos = 5
    elif window_pos == 2:
        window_pos = 0
    elif window_pos in [3, 4, 5]:
        screen.fill((52, 78, 91))
        if back_button.draw(screen):
            window_pos = 1
        lev_list = {}
        for i in range(len(level_buttons)):
            stars_dict = star_dict(window_pos)
            if level_buttons[i].draw(screen) and stars_dict[i + 1] != -1:
                if window_pos == 3:
                    level_paw = 'levels/easy/' + str(i + 1)
                elif window_pos == 4:
                    level_paw = 'levels/normal/' + str(i + 1)
                else:
                    level_paw = 'levels/hard/' + str(i + 1)
                window_pos *= 2
                break
        else:
            arr = cur.execute("SELECT * FROM levels").fetchall()
            surf = pygame.Surface((286, 123))
            surf.fill(colors_dict[10])
            surf.set_alpha(100)
            stars_dict = star_dict(window_pos)
            if stars_dict[1] == 1:
                screen.blit(star_image, (260, 330))
            elif stars_dict[1] == 2:
                screen.blit(star_image, (245, 330))
                screen.blit(star_image, (275, 330))
            elif stars_dict[1] == 3:
                screen.blit(star_image, (230, 330))
                screen.blit(star_image, (290, 330))
                screen.blit(star_image, (260, 330))

            if stars_dict[2] == -1:
                screen.blit(lock_image, (215, 387))
                screen.blit(surf, (136, 380))
            elif stars_dict[2] == 1:
                screen.blit(star_image, (260, 460))
            elif stars_dict[2] == 2:
                screen.blit(star_image, (245, 460))
                screen.blit(star_image, (275, 460))
            elif stars_dict[2] == 3:
                screen.blit(star_image, (230, 460))
                screen.blit(star_image, (290, 460))
                screen.blit(star_image, (260, 460))

            if stars_dict[3] == -1:
                screen.blit(lock_image, (215, 517))
                screen.blit(surf, (136, 510))
            elif stars_dict[3] == 1:
                screen.blit(star_image, (260, 590))
            elif stars_dict[3] == 2:
                screen.blit(star_image, (245, 590))
                screen.blit(star_image, (275, 590))
            elif stars_dict[3] == 3:
                screen.blit(star_image, (230, 590))
                screen.blit(star_image, (290, 590))
                screen.blit(star_image, (260, 590))

    elif window_pos in [6, 8, 10]:
        csvfile = open(level_paw + '.csv', 'r', newline='', encoding="utf8")
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        field = []
        cnt = 0
        count = 0
        for i in reader:
            arr = []
            for j in i:
                s = j.split('*')
                arr.append([int(s[0]), colors_dict[int(s[1])]])
                if int(s[0]) == 1:
                    cnt += 1
            field.append(arr)
        cnt2 = int((int(cnt * 0.07) - 7) * 0.2)
        bonuses = [5, 5, 5] + int(cnt * 0.93) * [0] + [7] * 4 + cnt2 * [1] + cnt2 * [2] + cnt2 * [6] + cnt2 * [
            4] + cnt2 * [3]
        mas = [1, 2, 3, 4, 6]
        for i in range(cnt - len(bonuses)):
            bonuses.append(mas[i % 5])
        racket = Racket(width // 2 - 43, height * 5 // 6, 10, 100, 2)
        Border(25, 60, 535, 60, 1, orient=3)
        Border(25, 60, 25, 760, 1, orient=3)
        Border(535, 60, 535, 760, 1, orient=4)
        ball = Ball(5, width // 2, height * 3 // 4)
        pause_button = Button(25, 10, pygame.image.load("images/button_pause.png").convert_alpha(), 0.5)
        make_field(field, bonuses)
        running = waiting(running, racket)
        while running:
            screen.fill((67, 9, 81))
            pygame.draw.rect(screen, (36, 9, 89), (25, 60, 510, 700), 0)
            if pause_button.draw(screen):
                resume_button = Button(183, 225, pygame.image.load("images/button_resume.png").convert_alpha(), 1)
                restart_button = Button(183, 325, pygame.image.load("images/button_restart.png").convert_alpha(), 1)
                exit_button2 = Button(183, 425, pygame.image.load("images/button_exit.png").convert_alpha(), 0.666666)
                t = False
                surf = pygame.Surface(size)
                surf.fill((36, 9, 89))
                surf.set_alpha(180)
                redraw(racket)
                screen.blit(surf, (0, 0))
                while running:
                    pygame.draw.rect(screen, (245, 141, 0), (150, 150, 255, 380), 0)
                    pygame.draw.rect(screen, (67, 9, 81), (160, 160, 235, 356), 0)
                    draw_text("Paused", pygame.font.SysFont("Arial Black", 40), (255, 255, 255), 192, 160)
                    if resume_button.draw(screen):
                        break
                    if restart_button.draw(screen):
                        t = True
                        break
                    if exit_button2.draw(screen):
                        t = True
                        window_pos //= 2
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            t = True
                            running = False
                            break
                    pygame.display.flip()
                if t:
                    break
            all_sprites.update()
            redraw(racket)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if (event.type == pygame.USEREVENT) and racket.flag:
                    racket.flag = False
                    all_sprites.remove(racket.border)
                    horizontal_borders.remove(racket.border)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        racket.new_action(-1)
                    elif event.key == pygame.K_RIGHT:
                        racket.new_action(1)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        racket.v = 0
            t = True
            for i in blocks_sprite:
                if i.purpose != -1:
                    t = False
            if t:
                mas = level_paw.split('/')
                arr = cur.execute("SELECT * FROM levels").fetchall()
                stars_dict = star_dict(window_pos // 2)
                cur.execute("UPDATE levels SET " + mas[1] + " = ? WHERE id = ?",
                            (max(racket.stars, stars_dict[int(mas[2])]), mas[2]))
                con.commit()
                if int(mas[2]) < 3:
                    cur.execute("UPDATE levels SET " + mas[1] + " = ? WHERE id = ?",
                                (max(0, stars_dict[int(mas[2]) + 1]), int(mas[2]) + 1))
                    con.commit()
                    next_button = Button(185, 340, pygame.image.load("images/button_next.png").convert_alpha(), 1)
                    try_again_button = Button(185, 250,
                                              pygame.image.load("images/button_try_again.png").convert_alpha(), 1)
                    exit_button2 = Button(185, 430, pygame.image.load("images/button_exit.png").convert_alpha(),
                                          0.666666)
                else:
                    try_again_button = Button(185, 300,
                                              pygame.image.load("images/button_try_again.png").convert_alpha(), 1)
                    exit_button2 = Button(185, 390, pygame.image.load("images/button_exit.png").convert_alpha(),
                                          0.666666)
                redraw(racket)
                surf = pygame.Surface(size)
                surf.fill((36, 9, 89))
                surf.set_alpha(180)
                screen.blit(surf, (0, 0))
                while running:
                    pygame.draw.rect(screen, (245, 141, 0), (150, 150, 255, 380), 0)
                    pygame.draw.rect(screen, (67, 9, 81), (160, 160, 235, 356), 0)
                    t = False
                    draw_text("You win!", pygame.font.SysFont("Arial Black", 40), (255, 255, 255), 183, 160)
                    if racket.stars == 0:
                        draw_text("no stars", pygame.font.SysFont("Arial Black", 25), (255, 255, 255), 220, 210)
                    elif racket.stars == 1:
                        screen.blit(star_image, (265, 215))
                    elif racket.stars == 2:
                        screen.blit(star_image, (250, 215))
                        screen.blit(star_image, (280, 215))
                    else:
                        screen.blit(star_image, (265, 215))
                        screen.blit(star_image, (230, 215))
                        screen.blit(star_image, (300, 215))
                    if try_again_button.draw(screen):
                        t = True
                        break
                    if exit_button2.draw(screen):
                        t = True
                        window_pos //= 2
                        break
                    if int(mas[2]) < 3 and next_button.draw(screen):
                        level_paw = level_paw[:-1] + str(int(mas[2]) + 1)
                        t = True
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            t = True
                            running = False
                            break
                    pygame.display.flip()
                if t:
                    break
            elif len(balls_list) == 0 and racket.lives > 1:
                racket.lives -= 1
                for i in all_sprites:
                    if type(i) == Bonus:
                        all_sprites.remove(i)
                        bonus_sprite.remove(i)
                ball = Ball(5, width // 2, height * 3 // 4)
                racket.rect.x, racket.rect.y = width // 2 - 43 + 50 - racket.length // 2, height * 5 // 6
                running = waiting(running, racket)
            if (len(balls_list) == 0 and racket.lives < 2) or racket.lives == 0:
                try_again_button = Button(183, 275, pygame.image.load("images/button_try_again.png").convert_alpha(), 1)
                exit_button2 = Button(183, 375, pygame.image.load("images/button_exit.png").convert_alpha(), 0.666666)
                t = False
                redraw(racket)
                surf = pygame.Surface(size)
                surf.fill((36, 9, 89))
                surf.set_alpha(180)
                screen.blit(surf, (0, 0))
                while running:
                    pygame.draw.rect(screen, (245, 141, 0), (150, 150, 255, 380), 0)
                    pygame.draw.rect(screen, (67, 9, 81), (160, 160, 235, 356), 0)
                    draw_text("You lost :(", pygame.font.SysFont("Arial Black", 35), (255, 255, 255), 180, 160)
                    if try_again_button.draw(screen):
                        t = True
                        break
                    if exit_button2.draw(screen):
                        t = True
                        window_pos //= 2
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            t = True
                            running = False
                            break
                    pygame.display.flip()
                if t:
                    break
            clock.tick(60)
        all_sprites.empty()
        racket_sprite.empty()
        horizontal_borders.empty()
        vertical_borders.empty()
        blocks_sprite.empty()
        bonus_sprite.empty()
        balls_list.clear()
    else:
        pass
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
