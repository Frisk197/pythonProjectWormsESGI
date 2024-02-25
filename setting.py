import pygame
import random
import math

# ESGI - PARIS
# 3RVJV - 2023/2024
# G7

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

DEBUG_ENABLED = False

EXPLOSION_RADIUS = 50
PERFORATION_OFFSET = 15

TERRAIN_HEIGHT = 500
TILE_SIZE = 1
SEED = random.randint(900000, 99999999)
SET_SEED = 9197368
SEED_Y_OFFSET = 200
REPEAT = random.randint(999999, 999999999)

SCALE_VIKING = 0.3

MAX_VIKINGS_PER_TEAM = 4
MAX_TEAMS = 8
DEFAULT_NUMBER_TEAMS = 3
DEFAULT_NUMBER_VIKINGS = 3
GRAVITY = -9.8
MOVING_TIME = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Verking Project - ESGI")

UP_ARROW = pygame.image.load('images/indication_arrows/up-arrow.png')
DOWN_ARROW = pygame.image.load('images/indication_arrows/down-arrow.png')
LEFT_ARROW = pygame.image.load('images/indication_arrows/left-arrow.png')
RIGHT_ARROW = pygame.image.load('images/indication_arrows/right-arrow.png')

SKY_BG = pygame.image.load('images/asset/sky.png')
SKY_BG = pygame.transform.scale(SKY_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

SKY_BG_MENU = pygame.image.load('images/asset/sky_menu.png')
SKY_BG_MENU = pygame.transform.scale(SKY_BG_MENU, (SCREEN_WIDTH, SCREEN_HEIGHT))

WIN_BG = pygame.image.load('images/asset/sky_win.png')
WIN_BG = pygame.transform.scale(WIN_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

TITLE_SCREEN = pygame.image.load('images/asset/title_screen.png')
TITLE_SCREEN = pygame.transform.scale(TITLE_SCREEN, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Colors:
    RED = (255, 40, 72)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 222, 40)
    SKY_BLUE = (40, 180, 255)

    class TERRAIN:
        GRASS2 = (80, 181, 156)
        GRASS = (120, 200, 120)
        SAND = (242, 209, 107)
        SNOW = (176, 237, 246)


TERRAIN_COLOR = random.choice([
            Colors.TERRAIN.GRASS2,
            Colors.TERRAIN.GRASS,
            Colors.TERRAIN.SAND,
            Colors.TERRAIN.SNOW
        ])