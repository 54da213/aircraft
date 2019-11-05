# -*- coding: utf-8 -*-
import copy
import random
import pygame
import time

from pygame.locals import *
import sys

AIRCRAFT1_IMAGE_PATH = "./material/hero1.png"
AIRCRAFT2_IMAGE_PATH = "./material/hero2.png"
BACK_IMAGE_PATH = "./material/background.png"
BULLET = "./material/bullet1.png"
ENEMY_1_1 = "./material/enemy1.png"
ENEMY1_BANG_1 = "./material/enemy1_down1.png"
ENEMY1_BANG_2 = "./material/enemy1_down2.png"
ENEMY1_BANG_3 = "./material/enemy1_down3.png"
ENEMY1_BANG_4 = "./material/enemy1_down4.png"

PLAYERS_BANG_1 = "./material/hero_blowup_n1.png"
PLAYERS_BANG_2 = "./material/hero_blowup_n2.png"
PLAYERS_BANG_3 = "./material/hero_blowup_n3.png"
PLAYERS_BANG_4 = "./material/hero_blowup_n4.png"

W = 480
H = 852


def get_enemy_init_point_x():
    return random.randint(0, H - 1)


def get_enemy_speed():
    return random.randint(1, 6)


enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


class Aircraft(pygame.sprite.Sprite):
    def __init__(self, image_file_group, bang_file_group):
        pygame.sprite.Sprite.__init__(self)  # 基类的init方法
        self.images = []
        self.bangs = []
        for image_file in image_file_group:
            self.images.append(pygame.image.load(image_file))

        for bang_file in bang_file_group:
            self.bangs.append(pygame.image.load(bang_file))

        self.direction = None
        self.speed = [0, 0, 0, 0]
        self.index = 0
        self.image = self.images[self.index]
        rect = self.image.get_rect()
        self.w = rect[2]
        self.h = rect[3]
        self.rect = pygame.Rect((W - rect[2]) / 2, H - rect[3], self.w, self.h)

    def get_barrel_point(self, *args, **kwargs):
        left_barrel_x = self.rect.x + self.w / 8
        left_barrel_y = self.rect.y + self.h / 4

        right_barrel_x = self.rect.x + self.w - self.w / 5
        right_barrel_y = self.rect.y + self.h / 4

        return (left_barrel_x, left_barrel_y), (right_barrel_x, right_barrel_y)  # 左右炮筒相对于飞机的位置

    def get_rect(self):
        return self.rect

    def update(self, *args):
        x, y, = args
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        # # 设置飞机随鼠标移动
        # x, y = pygame.mouse.get_pos()
        # # 获得鼠标位置
        # x -= self.image.get_width() / 2
        # y -= self.image.get_height() / 2
        if x < 0:
            x = 0
        elif x + self.w > W:
            x = W - self.w

        if y < 0:
            y = 0
        elif y + self.h > H:
            y = H - self.h
        self.set_point(x, y)

    def set_point(self, x, y):
        self.rect = pygame.Rect(x, y, self.rect[2], self.rect[3])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, barrel_point, barrel_direction):
        pygame.sprite.Sprite.__init__(self)  # 基类的init方法
        self.image = pygame.image.load(BULLET)
        rect = self.image.get_rect()
        self.rect = pygame.Rect(barrel_point[0], barrel_point[1], rect[2], rect[3])
        # 炮筒位置标记 0是左边  1是右边
        self.barrel_direction = barrel_direction
        self.speed = 30

    def update(self, *args):
        self.rect = pygame.Rect(self.rect[0], self.rect[1] - self.speed, self.rect[2], self.rect[3])
        point, = args
        # 大于上边界重置子弹位置 左边
        if self.rect.y <= 0:
            if self.barrel_direction == 0:
                self.rect = pygame.Rect(point[0][0], point[0][1], self.rect[2], self.rect[3])
            elif self.barrel_direction == 1:
                self.rect = pygame.Rect(point[1][0], point[1][1], self.rect[2], self.rect[3])
        # 如果子弹碰到敌机
        if pygame.sprite.spritecollide(self, enemy_group, False):
            # 绘制一个爆炸 增加一个敌机
            # enemy_group.add(Enemy([ENEMY_1_1], random.randint(0, random.randint(0, W / 57 - 1)),
            #                       [ENEMY1_BANG_1, ENEMY1_BANG_2, ENEMY1_BANG_3, ENEMY1_BANG_4]))
            # 子弹归位
            if self.barrel_direction == 0:
                self.rect = pygame.Rect(point[0][0], point[0][1], self.rect[2], self.rect[3])
            elif self.barrel_direction == 1:
                self.rect = pygame.Rect(point[1][0], point[1][1], self.rect[2], self.rect[3])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_file_group, i, bang_file_group):
        pygame.sprite.Sprite.__init__(self)  # 基类的init方法
        self.images = []
        self.bangs = []
        self.bang = False
        for image_file in image_file_group:
            self.images.append(pygame.image.load(image_file))

        for bang_file in bang_file_group:
            self.bangs.append(pygame.image.load(bang_file))

        self.index = 0
        self.image = self.images[self.index]
        rect = self.image.get_rect()
        self.w = rect[2]
        self.h = rect[3]
        # 运动方向 0右 1向左
        self.run_direction = 0
        # 运动速度
        self.speed = [5, get_enemy_speed()]
        # 0一号敌机
        self.type = 0
        # 初始位置
        if i == 2 or i == 3:
            self.rect = pygame.Rect(W - i * self.w - 30 + self.w, 0, self.w, self.h)
        else:
            self.rect = pygame.Rect(i * self.w + 30 + self.w, 0, self.w, self.h)

    def update(self, *args):
        speed = self.speed[1]
        if self.index >= len(self.images):
            self.index = 0
            if self.bang:
                enemy_group.remove(self)
                enemy_group.add(Enemy([ENEMY_1_1], 3, [ENEMY1_BANG_1, ENEMY1_BANG_2, ENEMY1_BANG_3, ENEMY1_BANG_4]))
        self.image = self.images[self.index]
        self.index += 1

        # 向下坠落
        if self.rect.x < 0 or self.rect.x + self.w >= W:
            self.speed[0] = -self.speed[0]
        if self.rect.y < 0 or self.rect.y + self.h >= H:
            self.speed[1] = -self.rect.y
        self.rect = pygame.Rect(self.rect.x + self.speed[0], self.rect.y + self.speed[1], self.w, self.h)
        self.speed[1] = speed

        if pygame.sprite.spritecollide(self, bullet_group, False):
            self.index = 0
            self.images = self.bangs
            self.bang = True


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))

    players = Aircraft([AIRCRAFT1_IMAGE_PATH, AIRCRAFT2_IMAGE_PATH],
                       [PLAYERS_BANG_1, PLAYERS_BANG_2, PLAYERS_BANG_3, PLAYERS_BANG_4])
    player_group = pygame.sprite.Group(players)
    background = pygame.image.load(BACK_IMAGE_PATH).convert()

    # 装载一组子弹
    # bullet_group = pygame.sprite.Group()
    for i in xrange(0, 10):
        # 左炮管装弹
        bullet_group.add(Bullet(((W - 99) / 2 + 13, H - 124 / 2 - 40 - i * 60), 0))
        # 右炮管装弹 唯独不同是炮管坐标
        bullet_group.add(Bullet(((W - 99) / 2 + 99 - 20, H - 124 / 2 - 40 - i * 60), 1))

    # 加载一组敌机
    # enemy_group = pygame.sprite.Group()
    for i in xrange(0, 10):
        en = Enemy([ENEMY_1_1], i, [ENEMY1_BANG_1, ENEMY1_BANG_2, ENEMY1_BANG_3, ENEMY1_BANG_4])
        enemy_group.add(en)

    time_passed = pygame.time.Clock()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == 119:
                players.direction = "up"
                players.speed[0] = 10
            elif event.key == 115:
                players.direction = "down"
                players.speed[1] = 10
            elif event.key == 97:
                players.direction = "left"
                players.speed[2] = 10
            elif event.key == 100:
                players.direction = "right"
                players.speed[3] = 10
        elif event.type == pygame.KEYUP:
            if event.key in [119, 115, 97, 100]:
                players.direction = None
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         # 设置飞机随鼠标移动
        #         x, y = pygame.mouse.get_pos()
        #         # 获得鼠标位置
        #         x -= players.image.get_width() / 2
        #         y -= players.image.get_height() / 2
        x, y = players.rect.x, players.rect.y,
        if players.direction == "up":
            y -= players.speed[0]
        elif players.direction == "down":
            y += players.speed[1]
        elif players.direction == "left":
            x -= players.speed[2]
        elif players.direction == "right":
            x += players.speed[3]
        screen.blit(background, (0, 0))
        # Calling the 'my_group.update' function calls the 'update' function of all
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        player_group.update(x, y)
        player_group.draw(screen)
        bullet_group.update(players.get_barrel_point())
        bullet_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)
        pygame.display.update()
        screen.blit(players.image, (0, 0))
        time_passed.tick(60)


if __name__ == '__main__':
    main()
