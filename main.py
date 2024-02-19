import pygame

from setting import *
from terrain_generation import genWorldDestructible, drawDestructibleWorldFullOptimized
from character import Team, Rocket, get_angle


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


def winCheck(number_teams, number_vikings, teams):
    lastTeamAlive = None
    teamCount = []
    for i in range(number_teams):
        count = 0
        for j in range(number_vikings):
            if teams[i].vikings[j].health > 0:
                count += 1
        teamCount.append(count)
    teamsLasting = 0
    for i in range(number_teams):
        if teamCount[i] > 0:
            teamsLasting += 1
    if teamsLasting == 1:
        for i in range(number_teams):
            if teamCount[i] > 0:
                lastTeamAlive = teams[i]
    return lastTeamAlive


def winScreen(team):
    runningWinScreen = True

    while runningWinScreen:
        screen.fill(Colors.BLACK)
        font = pygame.font.SysFont('', 70)
        text = font.render("GG Team " + str(team.id+1), True, Colors.GREEN)
        text2 = font.render("Play again ? [SPACE]", True, Colors.GREEN)
        text3 = font.render("Stop ? [DEL]", True, Colors.GREEN)
        screen.blit(text, (int(SCREEN_WIDTH/2) - int(text.get_width()/2), int(SCREEN_HEIGHT/2) - text.get_height()*2))
        screen.blit(text2, (int(SCREEN_WIDTH/2) - int(text2.get_width()/2), int(SCREEN_HEIGHT/2)))
        screen.blit(text3, (int(SCREEN_WIDTH/2) - int(text3.get_width()/2), int(SCREEN_HEIGHT/2) + text3.get_height()*2))

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            runningWinScreen = False

        for event in pygame.event.get():
            if key[pygame.K_DELETE]:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()



def loadGame(number_teams, number_vikings):
    map = genWorldDestructible()
    polygone_map = drawDestructibleWorldFullOptimized(map)

    holesCoordinates = []

    created_teams = createTeams(number_teams, number_vikings)
    placeVikings(created_teams)

    vikings = [viking for team in created_teams for viking in team.vikings]

    teamPlaying = 0

    movingStartTime = 0
    timerStarted = False

    selectedWorm = 0

    rightPressed = False
    leftPressed = False

    ePressed = False

    if DEBUG_ENABLED:
        mouse0Pressed = False

    last_time = pygame.time.get_ticks()
    running_game = True

    rocketSelected = True

    rocketLaunched = False

    endRound = False


    while running_game:
        mousePressed = pygame.mouse.get_pressed(num_buttons=3)
        if mousePressed[0] and not rocketLaunched:
            # print('ça clique fort')
            # Récupérer la position du clic de souris
            mouse_position = pygame.mouse.get_pos()
            # Calculer l'angle entre le Viking et la position du clic de souris
            angle = get_angle((created_teams[teamPlaying].vikings[selectedWorm].position.x, created_teams[teamPlaying].vikings[selectedWorm].position.y), mouse_position)
            # Créer la roquette avec l'angle sélectionné
            rocket = Rocket(created_teams[teamPlaying].vikings[selectedWorm].position.x, created_teams[teamPlaying].vikings[selectedWorm].position.y - created_teams[teamPlaying].vikings[selectedWorm].image.get_height(), angle+180, 20, 9.8, 2, 0.75)
            rocketLaunched = True




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
            if mousePressed[2] and not mouse0Pressed:
                mouse0Pressed = True
                mouseCoordinates = pygame.mouse.get_pos()
                holesCoordinates.append(mouseCoordinates)
                perforateBitMap(mouseCoordinates, map)
            if not mousePressed[2] and mouse0Pressed:
                mouse0Pressed = False
        #

        # clock update and fps counter
        clock.tick()
        font = pygame.font.SysFont('', 70)
        fps_text = font.render(str(int(clock.get_fps())), True, Colors.GREEN)
        screen.blit(fps_text, (0, 0))
        #

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0
        last_time = current_time

        if rocketLaunched:
            rocket.update(delta_time, map)
            rocket.draw(screen)
            if rocket.exploded:
                perforateBitMap((rocket.x, rocket.y), map)
                holesCoordinates.append((rocket.x, rocket.y))
                for vikings2 in created_teams:
                    for viking2 in vikings2.vikings:
                        if abs(viking2.position.x - rocket.x) < (EXPLOSION_RADIUS + PERFORATION_OFFSET) and abs(viking2.position.y - rocket.y) < EXPLOSION_RADIUS:
                            viking2.health -= (100 - int((abs(viking2.position.x - rocket.x) + abs(viking2.position.y - rocket.y))/2))
                rocketLaunched = False
                rocket = None
                endRound = True
            # print(f"Position : ({rocket.x}, {rocket.y})")

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            rocketSelected = True
        if key[pygame.K_DOWN]:
            rocketSelected = False

        if key[pygame.K_DELETE]:
            vikings[0].thereWasGround = False
            vikings[0].jumping = False

        # check for a winner
        win = winCheck(number_teams, number_vikings, created_teams)
        # print(win)
        if win is not None:
            running_game = False
            winScreen(win)
        #

        # end round and select next team
        if endRound:
            endRound = False
            timerStarted = False
            teamPlaying += 1
            if teamPlaying > number_teams - 1:
                teamPlaying = 0
            oldSelectedWorm = selectedWorm
            while created_teams[teamPlaying].vikings[selectedWorm].health <= 0:
                selectedWorm += 1
                if selectedWorm > number_vikings - 1:
                    selectedWorm = 0
                if selectedWorm == oldSelectedWorm:
                    teamPlaying += 1
                    if teamPlaying > number_teams - 1:
                        teamPlaying = 0
            nbVikingsOK = 0
            while nbVikingsOK == 0:
                for eVikings in created_teams[teamPlaying].vikings:
                    if eVikings.health > 0:
                        nbVikingsOK += 1
                if nbVikingsOK == 0:
                    teamPlaying += 1
                    if teamPlaying > number_teams - 1:
                        teamPlaying = 0
        #

        # handle timer
        if (key[pygame.K_q] or key[pygame.K_d] or key[pygame.K_z] or key[pygame.K_SPACE]) and not timerStarted:
            timerStarted = True
            movingStartTime = pygame.time.get_ticks()

        remainingTime = MOVING_TIME
        if timerStarted:
            remainingTime = MOVING_TIME - ((pygame.time.get_ticks() - movingStartTime)/1000)
        if remainingTime <= 0:
            remainingTime = 0
        if rocketLaunched:
            remainingTime = 0
        timerText = font.render(str(int(remainingTime)), True, Colors.BLUE)
        screen.blit(timerText, (SCREEN_WIDTH - timerText.get_width(), 0))
        #

        #
        if not timerStarted and (not rightPressed or not leftPressed) and (key[pygame.K_RIGHT] or key[pygame.K_LEFT]):
            if not rightPressed and key[pygame.K_RIGHT]:
                rightPressed = True
                selectedWorm += 1
                if selectedWorm > number_vikings - 1:
                    selectedWorm = 0
                oldSelectedWorm = selectedWorm
                while created_teams[teamPlaying].vikings[selectedWorm].health <= 0:
                    selectedWorm += 1
                    if selectedWorm > number_vikings - 1:
                        selectedWorm = 0
                    if selectedWorm == oldSelectedWorm:
                        teamPlaying += 1
                        if teamPlaying > number_teams - 1:
                            teamPlaying = 0
            if not leftPressed and key[pygame.K_LEFT]:
                leftPressed = True
                selectedWorm -= 1
                if selectedWorm < 0:
                    selectedWorm = number_vikings - 1
                oldSelectedWorm = selectedWorm
                while created_teams[teamPlaying].vikings[selectedWorm].health <= 0:
                    selectedWorm -= 1
                    if selectedWorm < 0:
                        selectedWorm = number_vikings - 1
                    if selectedWorm == oldSelectedWorm:
                        teamPlaying += 1
                        if teamPlaying > number_teams - 1:
                            teamPlaying = 0
        if not key[pygame.K_RIGHT]:
            rightPressed = False
        if not key[pygame.K_LEFT]:
            leftPressed = False
        #

        oldSelectedWorm = selectedWorm
        while created_teams[teamPlaying].vikings[selectedWorm].health <= 0:
            selectedWorm += 1
            if selectedWorm > number_vikings - 1:
                selectedWorm = 0
            if selectedWorm == oldSelectedWorm:
                teamPlaying += 1
                if teamPlaying > number_teams - 1:
                    teamPlaying = 0

        ###

        hp = font.render(str(created_teams[teamPlaying].vikings[selectedWorm].health), True, Colors.GREEN)
        screen.blit(hp, (SCREEN_WIDTH - hp.get_width(), hp.get_height() - hp.get_height()))


        for viking in vikings:
            if not viking.health <= 0:
                created_teams[teamPlaying].vikings[selectedWorm].move(key, delta_time, remainingTime, map)
                viking.doMath(map)
                viking.draw()

        screen.blit(DOWN_ARROW, ((created_teams[teamPlaying].vikings[selectedWorm].position.x + int(created_teams[teamPlaying].vikings[selectedWorm].image.get_width()/2)) - int(DOWN_ARROW.get_width()/2), created_teams[teamPlaying].vikings[selectedWorm].position.y - created_teams[teamPlaying].vikings[selectedWorm].image.get_height()*2))



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
