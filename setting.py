import pygame
import random

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

TERRAIN_HEIGHT = 500
TILE_SIZE = 1
SEED = random.randint(900000, 99999999)
SET_SEED = 9197368
SEED_Y_OFFSET = 200
REPEAT = random.randint(999999, 999999999)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Worms ESGI")