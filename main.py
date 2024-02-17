import pygame
import character
import random
import noise


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
    if DESTRUCTIBLE:
        map = genWorldDestructible()
        drawDestructibleWorldFull(screen, map)
    else:
        map = genWorld()

    clock = pygame.time.Clock()
    while runningGame:
        if DESTRUCTIBLE:
            drawDestructibleWorldOptimized(screen, map)
        else:
            screen.fill((0,0,0))
            drawWorld(screen, map)

        clock.tick()
        # print(clock.get_fps())
        font = pygame.font.SysFont(None, 70)
        text = font.render(str(int(clock.get_fps())), True, (0, 255, 0))
        screen.blit(text, (0, 0))

        #game here
        pygame.draw.rect(screen, (255, 0, 0), player)
        character.movements(pygame.key.get_pressed(), player)
        #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def genWorld():
    heightMap = []
    for y in range(0, int(SCREEN_WIDTH/TILE_SIZE)):
        height = int(noise.pnoise1(y * (SEED*0.00000000007), repeat=REPEAT) * TERRAIN_HEIGHT/2) + SEED_Y_OFFSET
        heightMap.append(height)
    print(heightMap)
    return heightMap

def genWorldDestructible():
    heightMap = []
    for y in range(0, SCREEN_WIDTH, TILE_SIZE):
        height = int(noise.pnoise1(y * (SEED * 0.00000000007), repeat=REPEAT) * TERRAIN_HEIGHT / 2) + SEED_Y_OFFSET
        heightMap.append(height)
    # print(heightMap)
    bitMap = []
    for x in range(0, int(SCREEN_WIDTH/TILE_SIZE)):
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

def drawWorld(screen, heightMap):
    for x in range(0, len(heightMap)):
        for y in range(0, heightMap[x], TILE_SIZE):
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((x * TILE_SIZE, SCREEN_HEIGHT - y, TILE_SIZE, TILE_SIZE)))


def drawDestructibleWorldFull(screen, bitMap):
    for x in range(0, int(SCREEN_WIDTH/TILE_SIZE)):
        for y in range(0, int(SCREEN_HEIGHT/TILE_SIZE)):
            if bitMap[x][y]:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)))
            else:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)))

def drawDestructibleWorldOptimized(screen, bitMap):
    print(len(bitMap))
    print(SCREEN_WIDTH/TILE_SIZE)
    screen.fill((0, 0, 0))
    polygoneMap = []
    x = 0
    y = int(SCREEN_HEIGHT/TILE_SIZE)-1
    polygoneMap.append((x, y))
    for x in range(int(SCREEN_WIDTH/TILE_SIZE)):
        while bitMap[x][y]:
            y -= 1
        while not bitMap[x][y]:
            y += 1
        polygoneMap.append((x*TILE_SIZE, y*TILE_SIZE))
    polygoneMap.append((SCREEN_WIDTH, SCREEN_HEIGHT))
    polygoneMap.append((0, SCREEN_HEIGHT))
    pygame.draw.polygon(screen, (255, 0, 0), polygoneMap)



def drawDestructibleWorld(screen, bitMap):
    for x in range(0, int(SCREEN_WIDTH/TILE_SIZE)):
        for y in range(0, int(SCREEN_HEIGHT/TILE_SIZE)):
            if not bitMap[x][y]:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)))

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TERRAIN_HEIGHT = 500
TILE_SIZE = 1
SEED = random.randint(900000, 99999999)
SET_SEED = 9197368
SEED_Y_OFFSET = 200
REPEAT = random.randint(999999, 999999999)
DESTRUCTIBLE = True

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
