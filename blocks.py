import pygame
from pygame import *
from player import *
from blocks import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("textures/platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)