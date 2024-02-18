import pygame
import random

# ESGI - PARIS
# 3RVJV - 2023/2024
# G7

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

DEBUG_ENABLED = True

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Verking Project - ESGI")

UP_ARROW = pygame.image.load('images/indication_arrows/up-arrow.png')
DOWN_ARROW = pygame.image.load('images/indication_arrows/down-arrow.png')
LEFT_ARROW = pygame.image.load('images/indication_arrows/left-arrow.png')
RIGHT_ARROW = pygame.image.load('images/indication_arrows/right-arrow.png')

class Colors:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)