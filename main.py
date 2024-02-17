import pygame
import character


def loadMainMenu(screen, teams, worms):
    upPressed = False
    downPressed = False
    rightPressed = False
    leftPressed = False
    runningMenu = True
    while runningMenu:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 24)
        img = font.render('' + str(teams) + ' ' + str(worms), True, (255, 0, 0))
        screen.blit(img, (20, 20))
        key = pygame.key.get_pressed()

        #Team Selection
        if key[pygame.K_UP] and not upPressed:
            upPressed = True
            teams += 1
            if teams > 8:
                teams = 8
        elif key[pygame.K_DOWN] and not downPressed:
            downPressed = True
            teams -= 1
            if teams < 2:
                teams = 2
        if not key[pygame.K_UP]:
            upPressed = False
        if not key[pygame.K_DOWN]:
            downPressed = False
        #

        # Worms Selection
        if key[pygame.K_RIGHT] and not rightPressed:
            rightPressed = True
            worms += 1
            if worms > 4:
                worms = 4
        elif key[pygame.K_LEFT] and not leftPressed:
            leftPressed = True
            worms -= 1
            if worms < 1:
                worms = 1
        if not key[pygame.K_RIGHT]:
            rightPressed = False
        if not key[pygame.K_LEFT]:
            leftPressed = False
        #

        if key[pygame.K_RETURN]:
            runningMenu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return (teams, worms)


def loadGame(screen, teams, worms):
    runningGame = True
    while runningGame:
        screen.fill((0, 0, 0))
        #game here
        font = pygame.font.SysFont(None, 24)
        img = font.render('c le jeu ' + str(teams) + ' teams et ' + str(worms) + ' worms', True, (255, 0, 0))
        screen.blit(img, (20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Worms ESGI")

player = pygame.Rect((300, 250, 50, 50))

scene = 1 # 1 for main menu, 2 for game

running = True

teams = 2
worms = 4

while running:

    teamsAndWorms = loadMainMenu(screen, teams, worms)
    loadGame(screen, teamsAndWorms[0], teamsAndWorms[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
