from setting import *
from terrain_generation import genWorldDestructible, drawDestructibleWorldFullOptimized
from character import Team


def loadMainMenu(teams, vikings):
    running_menu = True

    up_pressed = False
    down_pressed = False
    right_pressed = False
    left_pressed = False

    opacity_up = True
    opacity = 0
    while running_menu:

        if opacity_up and opacity < 1:
            opacity += 0.005
        elif not opacity_up and opacity > 0:
            opacity -= 0.005
        elif opacity_up and opacity >= 1:
            opacity = 1
            opacity_up = False
        elif not opacity_up and opacity <= 0:
            opacity = 0
            opacity_up = True

        screen.fill(Colors.BLACK)

        font = pygame.font.SysFont('', 70)

        line1 = font.render(f"équipes: {teams} ", True, Colors.RED)
        line2 = font.render(f"vikings par équipes: {vikings} ", True, Colors.RED)
        line3 = font.render('Appuyez sur ENTRER pour commencer', True, (Colors.RED[0] * opacity, 0, 0))

        screen.blit(line1, ((SCREEN_WIDTH / 2) - (line1.get_width() / 2) - 50, (SCREEN_HEIGHT / 2) - (line1.get_height())))
        screen.blit(UP_ARROW, ((SCREEN_WIDTH / 2) + (line1.get_width() / 2), (SCREEN_HEIGHT / 2) - (line1.get_height() * 1.5)))
        screen.blit(DOWN_ARROW, ((SCREEN_WIDTH / 2) + (line1.get_width() / 2), (SCREEN_HEIGHT / 2) - (line1.get_height() / 1.5)))

        screen.blit(line2, ((SCREEN_WIDTH / 2) - (line2.get_width() / 2), (SCREEN_HEIGHT / 2) + (line2.get_height())))
        screen.blit(LEFT_ARROW, ((SCREEN_WIDTH / 2) + (line2.get_width() / 2), (SCREEN_HEIGHT / 2) + (line2.get_height())))
        screen.blit(RIGHT_ARROW, ((SCREEN_WIDTH / 2) + (line2.get_width() / 2) + 50, (SCREEN_HEIGHT / 2) + (line2.get_height())))

        screen.blit(line3, ((SCREEN_WIDTH / 2) - (line3.get_width() / 2), (SCREEN_HEIGHT / 2) + (line3.get_height() * 3)))

        key = pygame.key.get_pressed()

        # Team Selection
        if key[pygame.K_UP] and not up_pressed:
            up_pressed = True
            teams += 1
            if teams > MAX_TEAMS:
                teams = MAX_TEAMS
        elif key[pygame.K_DOWN] and not down_pressed:
            down_pressed = True
            teams -= 1
            if teams < 2:
                teams = 2
        if not key[pygame.K_UP]:
            up_pressed = False
        if not key[pygame.K_DOWN]:
            down_pressed = False

        # Viking Selection
        if key[pygame.K_RIGHT] and not right_pressed:
            right_pressed = True
            vikings += 1
            if vikings > MAX_VIKINGS_PER_TEAM:
                vikings = MAX_VIKINGS_PER_TEAM
        elif key[pygame.K_LEFT] and not left_pressed:
            left_pressed = True
            vikings -= 1
            if vikings < 1:
                vikings = 1
        if not key[pygame.K_RIGHT]:
            right_pressed = False
        if not key[pygame.K_LEFT]:
            left_pressed = False

        if key[pygame.K_RETURN]:
            running_menu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return teams, vikings


def createTeams(teams, vikings):
    all_teams = []
    for i in range(teams):
        team = Team(i, vikings)
        for j in range(vikings):
            team.vikings[j].position.y = 500
        all_teams.append(team)
    return all_teams


def placeVikings(teams):
    min_distance_between_players = 50

    occupied_positions = []

    all_vikings = []

    for team in teams:
        for viking in team.vikings:
            all_vikings.append(viking)

    for viking in all_vikings:

        while True:
            player_x = random.randint(0, SCREEN_WIDTH - viking.rect.width)
            valid_position = True
            for pos in occupied_positions:
                if abs(player_x - pos) < min_distance_between_players:
                    valid_position = False
                    break
            if valid_position:
                player_x = min(player_x, SCREEN_WIDTH - viking.rect.width)
                occupied_positions.append(player_x)
                viking.position.x = player_x
                break

        if random.choice([True, False]):
            viking.getFlipped()


def perforateBitMap(center, bitMap):
    for i in range(EXPLOSION_RADIUS):
        bresenham_circle(center[0] + PERFORATION_OFFSET, center[1], i, bitMap)
        bresenham_circle(center[0] - PERFORATION_OFFSET, center[1], i, bitMap)
        bresenham_circle(center[0], center[1] + PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0], center[1] - PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0] - PERFORATION_OFFSET, center[1] - PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0] + PERFORATION_OFFSET, center[1] + PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0] - PERFORATION_OFFSET, center[1] + PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0] + PERFORATION_OFFSET, center[1] - PERFORATION_OFFSET, i, bitMap)
        bresenham_circle(center[0], center[1], i, bitMap)

def bresenham_circle(x0, y0, radius, bitMap):
    x = radius
    y = 0
    err = 0

    while x >= y:
        if not x0 + x < 0 and not x0 + x >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 + y < 0 and not y0 + y >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 + x)][int(y0 + y)] = 0
        if not x0 + y < 0 and not x0 + y >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 + x < 0 and not y0 + x >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 + y)][int(y0 + x)] = 0
        if not x0 - y < 0 and not x0 - y >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 + x < 0 and not y0 + x >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 - y)][int(y0 + x)] = 0
        if not x0 - x < 0 and not x0 - x >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 + y < 0 and not y0 + y >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 - x)][int(y0 + y)] = 0
        if not x0 - x < 0 and not x0 - x >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 - y < 0 and not y0 - y >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 - x)][int(y0 - y)] = 0
        if not x0 - y < 0 and not x0 - y >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 - y)][int(y0 - x)] = 0
        if not x0 + y < 0 and not x0 + y >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 + y)][int(y0 - x)] = 0
        if not x0 + x < 0 and not x0 + x >= int(SCREEN_WIDTH/TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(SCREEN_HEIGHT/TILE_SIZE):
            bitMap[int(x0 + x)][int(y0 - x)] = 0

        y += 1
        err += 1 + 2*y
        if 2*(err-x) + 1 > 0:
            x -= 1
            err += 1 - 2*x


def loadGame(number_teams, number_vikings):
    running_game = True

    map = genWorldDestructible()
    polygone_map = drawDestructibleWorldFullOptimized(map)

    holesCoordinates = []

    created_teams = createTeams(number_teams, number_vikings)
    placeVikings(created_teams)

    vikings = []
    for team in created_teams:
        for viking in team.vikings:
            vikings.append(viking)

    if DEBUG_ENABLED:
        mouse0Pressed = False

    while running_game:

        # draw full map
        screen.fill(Colors.BLACK)
        pygame.draw.polygon(screen, Colors.RED, polygone_map)
        #

        # draw holes
        for hole in holesCoordinates:
            pygame.draw.circle(screen, Colors.BLACK, hole, EXPLOSION_RADIUS + PERFORATION_OFFSET)
        #


        # debug mode to create holes with mouse left click
        if DEBUG_ENABLED:
            mousePressed = pygame.mouse.get_pressed(num_buttons=3)
            if mousePressed[0] and not mouse0Pressed:
                mouse0Pressed = True
                mouseCoordinates = pygame.mouse.get_pos()
                holesCoordinates.append(mouseCoordinates)
                perforateBitMap(mouseCoordinates, map)
            if not mousePressed[0] and mouse0Pressed:
                mouse0Pressed = False
        #

        # clock update and fps counter
        clock.tick()
        font = pygame.font.SysFont('', 70)
        fps_text = font.render(str(int(clock.get_fps())), True, Colors.GREEN)
        screen.blit(fps_text, (0, 0))
        #

        key = pygame.key.get_pressed()

        #
        #   GAME
        vikings[0].move(key)
        #



        for viking in vikings:
            viking.doMath(map)
            viking.draw()

        for event in pygame.event.get():
            if key[pygame.K_DELETE]:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


running = True
while running:

    number_teams_and_vikings = loadMainMenu(DEFAULT_NUMBER_TEAMS, DEFAULT_NUMBER_VIKINGS)
    loadGame(number_teams_and_vikings[0], number_teams_and_vikings[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
