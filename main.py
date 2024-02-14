import pygame


def characterMovements(key, character):
    if key[pygame.K_q]:
        if key[pygame.K_z] != key[pygame.K_s]:
            character.move_ip(-1, 0)
        else:
            character.move_ip(-2, 0)
    if key[pygame.K_d]:
        if key[pygame.K_z] != key[pygame.K_s]:
            character.move_ip(1, 0)
        else:
            character.move_ip(2, 0)
    if key[pygame.K_z]:
        if key[pygame.K_q] != key[pygame.K_d]:
            character.move_ip(0, -1)
        else:
            character.move_ip(0, -2)
    if key[pygame.K_s]:
        if key[pygame.K_q] != key[pygame.K_d]:
            character.move_ip(0, 1)
        else:
            character.move_ip(0, 2)


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

    characterMovements(pygame.key.get_pressed(), player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
