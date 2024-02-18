from setting import *
import noise


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


def drawDestructibleWorldFullOptimized(bitMap):
    screen.fill(Colors.BLACK)
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
