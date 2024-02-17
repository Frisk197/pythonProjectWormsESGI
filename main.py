import pygame
import character


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


def loadMainMenu(screen, teams):
    runningMenu = True
    while runningMenu:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 24)
        img = font.render('' + teams, True, (255, 0, 0))
        screen.blit(img, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return 2


def loadGame(screen, teams):
    runningGame = True
    while runningGame:
        screen.fill((0, 0, 0))
        #game here
        font = pygame.font.SysFont(None, 24)
        img = font.render('c le jeu', True, (255, 0, 0))
        screen.blit(img, (20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return 1


pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Worms ESGI")

player = pygame.Rect((300, 250, 50, 50))

scene = 1 # 1 for main menu, 2 for game

running = True

while running:

    teams = 1

    if scene == 1:
        scene = loadMainMenu(screen, teams)
    elif scene == 2:
        scene = loadGame(screen, teams)
    else:
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
