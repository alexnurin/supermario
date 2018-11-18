import pygame
import pyganim
from pygame import *

MOVE_SPEED = 8
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 0.4 # Сила, которая будет тянуть нас вниз
COLOR = "#888888"

ANIMATION_DELAY = 1  # скорость смены кадров
ANIMATION_RIGHT = [ 'textures/mario/r1.png',
                    'textures/mario/r2.png',
                    'textures/mario/r3.png',
                    'textures/mario/r4.png',
                    'textures/mario/r5.png']
ANIMATION_LEFT = ['textures/mario/l1.png',
                  'textures/mario/l2.png',
                  'textures/mario/l3.png',
                  'textures/mario/l4.png',
                  'textures/mario/l5.png']
ANIMATION_JUMP_LEFT = [('textures/mario/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('textures/mario/jr.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('textures/mario/j.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('textures/mario/0.png', ANIMATION_DELAY)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            print(boltAnim)
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            print(boltAnim)
        print(boltAnim[0])
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)



    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает