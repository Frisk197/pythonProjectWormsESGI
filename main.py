import os.path

import pygame
from character import Player
import character


def loadMainMenu(screen, teams, worms):
    upPressed = False
    downPressed = False
    rightPressed = False
    leftPressed = False
    runningMenu = True
    opacityUp = True
    opacity = 0
    while runningMenu:

        if opacityUp and opacity < 1:
            opacity += 0.005
        elif not opacityUp and opacity > 0:
            opacity -= 0.005
        elif opacityUp and opacity >= 1:
            opacity = 1
            opacityUp = False
        elif not opacityUp and opacity <= 0:
            opacity = 0
            opacityUp = True

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont(None, 70)

        line1 = font.render('équipes: ' + str(teams) + '', True, (255, 0, 0))
        line2 = font.render('worms par équipes: ' + str(worms), True, (255, 0, 0))

        upArrow = pygame.image.load('images/up-arrow.png')
        downArrow = pygame.image.load('images/down-arrow.png')
        leftArrow = pygame.image.load('images/left-arrow.png')
        rightArrow = pygame.image.load('images/right-arrow.png')

        screen.blit(line1, ((SCREEN_WIDTH/2) - (line1.get_width()/2) - 50, (SCREEN_HEIGHT/2) - (line1.get_height())))
        screen.blit(upArrow, ((SCREEN_WIDTH/2) + (line1.get_width()/2), (SCREEN_HEIGHT/2) - (line1.get_height()*1.5)))
        screen.blit(downArrow, ((SCREEN_WIDTH/2) + (line1.get_width()/2), (SCREEN_HEIGHT/2) - (line1.get_height()/1.5)))

        screen.blit(line2, ((SCREEN_WIDTH/2) - (line2.get_width()/2), (SCREEN_HEIGHT/2) + (line2.get_height())))
        screen.blit(leftArrow, ((SCREEN_WIDTH / 2) + (line2.get_width() / 2), (SCREEN_HEIGHT / 2) + (line2.get_height())))
        screen.blit(rightArrow, ((SCREEN_WIDTH / 2) + (line2.get_width() / 2) + 50, (SCREEN_HEIGHT / 2) + (line2.get_height())))

        line3 = font.render('Appuyez sur ENTRER pour commencer', True, (255 * opacity, 0, 0))
        screen.blit(line3, ((SCREEN_WIDTH / 2) - (line3.get_width() / 2), (SCREEN_HEIGHT / 2) + (line3.get_height()*3)))

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

player1 = Player("Player 1")
print("Player 1 position:", player1.position.x, player1.position.y)


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
