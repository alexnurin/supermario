import pygame
from pygame import *
from player import *
from blocks import *
from camera import *

gameover = False
SIZE = WIDTH, HEIGHT = 800, 600
screen = None
bg = None


def init():
    global screen, bg
    pygame.init()
    bg = (100, 200, 100)
    screen = pygame.display.set_mode(SIZE)
    display.set_caption("It’s-a Me, Mario!")


def main():
    global gameover
    init()

    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    level = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-                                -",
        "-            --                  -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--     ------                    -",
        "-                                -",
        "-                            --- -",
        "-                                -",
        "-                   ----         -",
        "-      ---                       -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-         ----------             -",
        "-                                -",
        "----------------------------------"]

    timer = pygame.time.Clock()

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not gameover:  # Основной цикл
        timer.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            if event.type == pygame.KEYDOWN and (event.key == ord('a') or event.key == 276):
                left = True
            if event.type == pygame.KEYDOWN and (event.key == ord('d') or event.key == 275):
                right = True

            if event.type == pygame.KEYUP and (event.key == ord('d') or event.key == 275):
                right = False
            if event.type == pygame.KEYUP and (event.key == ord('a') or event.key == 276):
                left = False

            if event.type == pygame.KEYDOWN and (event.key == ord('w') or event.key == 273 or event.key == 32):
                up = True
            if event.type == pygame.KEYUP and (event.key == ord('w') or event.key == 273 or event.key == 32):
                up = False
            print(event)

        screen.fill(bg)
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms) # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.flip()


if __name__ == "__main__":
    main()
