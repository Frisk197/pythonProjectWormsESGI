import os.path

import pygame
from character import *
import random
import noise
from TerrainTest import Terrain


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

        screen.blit(line1,
                    ((SCREEN_WIDTH / 2) - (line1.get_width() / 2) - 50, (SCREEN_HEIGHT / 2) - (line1.get_height())))
        screen.blit(upArrow,
                    ((SCREEN_WIDTH / 2) + (line1.get_width() / 2), (SCREEN_HEIGHT / 2) - (line1.get_height() * 1.5)))
        screen.blit(downArrow,
                    ((SCREEN_WIDTH / 2) + (line1.get_width() / 2), (SCREEN_HEIGHT / 2) - (line1.get_height() / 1.5)))

        screen.blit(line2, ((SCREEN_WIDTH / 2) - (line2.get_width() / 2), (SCREEN_HEIGHT / 2) + (line2.get_height())))
        screen.blit(leftArrow,
                    ((SCREEN_WIDTH / 2) + (line2.get_width() / 2), (SCREEN_HEIGHT / 2) + (line2.get_height())))
        screen.blit(rightArrow,
                    ((SCREEN_WIDTH / 2) + (line2.get_width() / 2) + 50, (SCREEN_HEIGHT / 2) + (line2.get_height())))

        line3 = font.render('Appuyez sur ENTRER pour commencer', True, (255 * opacity, 0, 0))
        screen.blit(line3,
                    ((SCREEN_WIDTH / 2) - (line3.get_width() / 2), (SCREEN_HEIGHT / 2) + (line3.get_height() * 3)))

        key = pygame.key.get_pressed()

        # Team Selection
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



def createTeams(teams, worms):
    allTeams = []
    for i in range(teams):
        team = Team(i, worms)
        for j in range(worms):
            team.vikings[j].position.y = 500
        allTeams.append(team)
    return allTeams

def placeWorms(teams):


    # Définir la largeur minimale entre les joueurs
    min_distance_between_players = 50  # Largeur minimale entre les joueurs

    # Liste pour stocker les positions occupées
    occupied_positions = []

    # Positionnement aléatoire des joueurs pour chaque équipe

    allVikings = []

    for i in teams:
        for j in i.vikings:
            allVikings.append(j)

    for viking in allVikings:

        while True:
            player_x = random.randint(0,
                                        SCREEN_WIDTH - viking.rect.width)  # Utilisation de la largeur du rectangle de l'image du joueur
            valid_position = True
            for pos in occupied_positions:
                if abs(player_x - pos) < min_distance_between_players:
                    valid_position = False
                    break
            if valid_position:
                player_x = min(player_x,
                                SCREEN_WIDTH - viking.rect.width)  # Ajustement pour éviter de sortir de l'écran
                occupied_positions.append(player_x)
                viking.position.x = player_x
                break


        # Flip aléatoirement tous les joueurs de l'équipe
        if random.choice([True, False]):
            for viking in allVikings:
                viking.flipped = True
                # player.image = pygame.transform.flip(player.image, True, False)


def loadGame(screen, teams, worms):
    runningGame = True

    map = genWorldDestructible()
    polygoneMap = drawDestructibleWorldFullOptimized(screen, map)

    clock = pygame.time.Clock()

    createdTeams = createTeams(teams, worms)
    placeWorms(createdTeams)

    vikings = []
    for i in createdTeams:
        for j in i.vikings:
            vikings.append(j)

    while runningGame:

        screen.fill((0, 0, 0))
        pygame.draw.polygon(screen, (255, 0, 0), polygoneMap)

        clock.tick()
        # print(clock.get_fps())
        font = pygame.font.SysFont(None, 70)
        text = font.render(str(int(clock.get_fps())), True, (0, 255, 0))
        screen.blit(text, (0, 0))

        # game here
        # pygame.draw.rect(screen, (255, 255, 0), player)
        # character.movements(pygame.key.get_pressed(), player)

        for i in vikings:
            # print('tkt')
            i.draw(screen)

        #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def genWorldDestructible():
    heightMap = []
    for y in range(0, SCREEN_WIDTH, TILE_SIZE):
        height = int(noise.pnoise1(y * (SEED * 0.00000000007), repeat=REPEAT) * TERRAIN_HEIGHT / 2) + SEED_Y_OFFSET
        heightMap.append(height)
    # print(heightMap)
    bitMap = []
    for x in range(0, int(SCREEN_WIDTH / TILE_SIZE)):
        bitMapY = []
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            if y > SCREEN_HEIGHT - heightMap[x]:
                bitMapY.append(1)
            else:
                bitMapY.append(0)
        # print(bitMapY)
        bitMap.append(bitMapY)
    # print(bitMap)
    return bitMap


def drawDestructibleWorldFullOptimized(screen, bitMap):
    # print(len(bitMap))
    # print(SCREEN_WIDTH/TILE_SIZE)
    screen.fill((0, 0, 0))
    polygoneMap = []
    x = 0
    y = int(SCREEN_HEIGHT / TILE_SIZE) - 1
    polygoneMap.append((x, y))
    for x in range(int(SCREEN_WIDTH / TILE_SIZE)):
        while bitMap[x][y]:
            y -= 1
        while not bitMap[x][y]:
            y += 1
        polygoneMap.append((x * TILE_SIZE, y * TILE_SIZE))
    polygoneMap.append((SCREEN_WIDTH, SCREEN_HEIGHT))
    polygoneMap.append((0, SCREEN_HEIGHT))
    return polygoneMap


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

terrain = Terrain(SCREEN_WIDTH, SCREEN_HEIGHT, (0, 255, 0), 24)  # Exemple de terrain vert
clock = pygame.time.Clock()

# Nombre d'équipes
teams = 3

worms = 3  # Nombre de joueurs par équipe

running = True
while running:

    teamsAndWorms = loadMainMenu(screen, teams, worms)
    loadGame(screen, teamsAndWorms[0], teamsAndWorms[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
