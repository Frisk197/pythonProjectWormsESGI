import pygame
import character

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Worms ESGI")

player = pygame.Rect((300, 250, 50, 50))

running = True

while running:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), player)

    character.movements(pygame.key.get_pressed(), player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
