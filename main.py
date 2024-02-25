import pygame

from setting import *
from terrain_generation import genWorldDestructible, drawDestructibleWorldFullOptimized
from character import Team
from weapons import Rocket, Grenade, getAngle
from menu import titleScreen, loadMainMenu, winScreen


def createTeams(teams, vikings):
    all_teams = []

    for i in range(teams):
        team = Team(i, vikings)
        all_teams.append(team)
    return all_teams


def placeVikings(teams):
    min_distance_between_players = 50
    occupied_positions = []
    low_number_viking = False
    failed_pos = 0

    all_vikings = []

    for team in teams:
        for viking in team.vikings:
            all_vikings.append(viking)

    if len(all_vikings) <= 4:
        low_number_viking = True

    for viking in all_vikings:

        while True:
            player_x = random.randint(0, SCREEN_WIDTH - viking.rect.width)
            player_y = 500
            valid_position = True
            for pos in occupied_positions:
                if abs(player_x - pos) < min_distance_between_players:
                    valid_position = False
                    failed_pos = failed_pos + 1
                    if failed_pos > 50:
                        valid_position = True
            if valid_position:
                failed_pos = 0
                if low_number_viking:
                    viking.position.speed_x = 40
                player_x = min(player_x, SCREEN_WIDTH - viking.rect.width)
                occupied_positions.append(player_x)
                viking.position.x = player_x
                viking.position.y = player_y

                break

        if random.choice([True, False]):
            viking.getFlipped(True)
            viking.rpg7.getFlipped(True)


def perforateBitMap(center, bit_map):
    for i in range(EXPLOSION_RADIUS):
        bresenhamCircle(center[0] + PERFORATION_OFFSET, center[1], i, bit_map)
        bresenhamCircle(center[0] - PERFORATION_OFFSET, center[1], i, bit_map)
        bresenhamCircle(center[0], center[1] + PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0], center[1] - PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0] - PERFORATION_OFFSET, center[1] - PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0] + PERFORATION_OFFSET, center[1] + PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0] - PERFORATION_OFFSET, center[1] + PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0] + PERFORATION_OFFSET, center[1] - PERFORATION_OFFSET, i, bit_map)
        bresenhamCircle(center[0], center[1], i, bit_map)


def bresenhamCircle(x0, y0, radius, bit_map):
    x = radius
    y = 0
    err = 0

    while x >= y:
        if not x0 + x < 0 and not x0 + x >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 + y < 0 and not y0 + y >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 + x)][int(y0 + y)] = 0
        if not x0 + y < 0 and not x0 + y >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 + x < 0 and not y0 + x >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 + y)][int(y0 + x)] = 0
        if not x0 - y < 0 and not x0 - y >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 + x < 0 and not y0 + x >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 - y)][int(y0 + x)] = 0
        if not x0 - x < 0 and not x0 - x >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 + y < 0 and not y0 + y >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 - x)][int(y0 + y)] = 0
        if not x0 - x < 0 and not x0 - x >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 - y < 0 and not y0 - y >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 - x)][int(y0 - y)] = 0
        if not x0 - y < 0 and not x0 - y >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 - y)][int(y0 - x)] = 0
        if not x0 + y < 0 and not x0 + y >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 + y)][int(y0 - x)] = 0
        if not x0 + x < 0 and not x0 + x >= int(SCREEN_WIDTH / TILE_SIZE) and not y0 - x < 0 and not y0 - x >= int(
                SCREEN_HEIGHT / TILE_SIZE):
            bit_map[int(x0 + x)][int(y0 - x)] = 0

        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x


def explosion(holes_coordinates, weapon, teams, map):
    perforateBitMap((weapon.position.x, weapon.position.y), map)
    holes_coordinates.append((weapon.position.x, weapon.position.y))
    for vikings2 in teams:
        for viking2 in vikings2.vikings:
            if (abs(viking2.position.x - weapon.position.x) < (EXPLOSION_RADIUS + PERFORATION_OFFSET) and
                    abs(viking2.position.y - weapon.position.y) < EXPLOSION_RADIUS):
                viking2.position.x = viking2.position.x + ((viking2.position.x - weapon.position.x) * 2.5)
                viking2.position.y = viking2.position.y + ((viking2.position.y - weapon.position.y) * 2.5)
                viking2.health -= abs((weapon.damage - int(
                    (abs(viking2.position.x - weapon.position.x) + abs(
                        viking2.position.y - weapon.position.y)) / 2)))
    return holes_coordinates


def winCheck(number_teams, number_vikings, teams):
    last_team_alive = None
    team_count = []
    for i in range(number_teams):
        count = 0
        for j in range(number_vikings):
            if teams[i].vikings[j].health > 0:
                count += 1
        team_count.append(count)
    teams_lasting = 0
    for i in range(number_teams):
        if team_count[i] > 0:
            teams_lasting += 1
    if teams_lasting == 1:
        for i in range(number_teams):
            if team_count[i] > 0:
                last_team_alive = teams[i]
    return last_team_alive


def loadGame(number_teams, number_vikings):
    map = genWorldDestructible()
    polygone_map = drawDestructibleWorldFullOptimized(map)

    holes_coordinates = []

    created_teams = createTeams(number_teams, number_vikings)
    placeVikings(created_teams)

    vikings = [viking for team in created_teams for viking in team.vikings]

    team_playing = 0

    moving_start_time = 0
    timer_started = False

    selected_viking = 0

    right_pressed = False
    left_pressed = False

    if DEBUG_ENABLED:
        mouse0_pressed = False

    last_time = pygame.time.get_ticks()
    running_game = True

    rocket_selected = False

    rocket_launched = False
    grenade_launched = False
    aim_grenade_launched = False

    end_round = False

    while running_game:
        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
        if mouse_pressed:
            mouse_position = pygame.mouse.get_pos()

            angle = getAngle((created_teams[team_playing].vikings[selected_viking].position.x,
                              created_teams[team_playing].vikings[selected_viking].position.y), mouse_position)

            if mouse_pressed[0] and not rocket_launched and not grenade_launched and rocket_selected and not end_round:
                rocket = Rocket(created_teams[team_playing].vikings[selected_viking].position.x,
                                created_teams[team_playing].vikings[selected_viking].position.y -
                                created_teams[team_playing].vikings[selected_viking].image.get_height(),
                                angle + 180)

                if angle < 75 or angle > 270:
                    if not created_teams[team_playing].vikings[selected_viking].flipped:
                        created_teams[team_playing].vikings[selected_viking].getFlipped(True)
                        created_teams[team_playing].vikings[selected_viking].rpg7.getFlipped(True)
                    rocket.getFlipped(True)
                elif created_teams[team_playing].vikings[selected_viking].flipped:
                        created_teams[team_playing].vikings[selected_viking].getFlipped(False)
                        created_teams[team_playing].vikings[selected_viking].rpg7.getFlipped(False)
                rocket_launched = True

            elif mouse_pressed[
                0] and not rocket_launched and not grenade_launched and not rocket_selected and not end_round:
                grenade = Grenade(created_teams[team_playing].vikings[selected_viking].position.x,
                                  created_teams[team_playing].vikings[selected_viking].position.y + 10 -
                                  created_teams[team_playing].vikings[selected_viking].image.get_height(), angle,
                                  abs(created_teams[team_playing].vikings[selected_viking].position.x - mouse_position[
                                      0]),
                                  abs(created_teams[team_playing].vikings[selected_viking].position.y - mouse_position[
                                      1]))
                grenade_launched = True

            if mouse_pressed[2] and not grenade_launched and not rocket_launched and not rocket_selected:
                fake_grenade = Grenade(created_teams[team_playing].vikings[selected_viking].position.x,
                                       created_teams[team_playing].vikings[selected_viking].position.y + 10 -
                                       created_teams[team_playing].vikings[selected_viking].image.get_height(), angle,
                                       abs(created_teams[team_playing].vikings[selected_viking].position.x -
                                           mouse_position[0]),
                                       abs(created_teams[team_playing].vikings[selected_viking].position.y -
                                           mouse_position[1]))
                aim_grenade_launched = True

        # screen.blit(SKY_BG, SKY_BG.get_rect())
        screen.fill(Colors.SKY_BLUE)
        pygame.draw.polygon(screen, TERRAIN_COLOR, polygone_map)

        # draw holes
        for hole in holes_coordinates:
            pygame.draw.circle(screen, Colors.SKY_BLUE, hole, EXPLOSION_RADIUS + PERFORATION_OFFSET)

        # debug mode to create holes with mouse left click
        if DEBUG_ENABLED:
            mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
            if mouse_pressed[2] and not mouse0_pressed:
                mouse0_pressed = True
                mouse_coordinates = pygame.mouse.get_pos()
                holes_coordinates.append(mouse_coordinates)
                perforateBitMap(mouse_coordinates, map)
            if not mouse_pressed[2] and mouse0_pressed:
                mouse0_pressed = False

        # clock update and fps counter
        clock.tick()
        font = pygame.font.SysFont('Tahoma', 50, bold=True)
        fps_text = font.render(str(int(clock.get_fps())), True, Colors.GREEN)
        screen.blit(fps_text, (10, 5))

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0
        last_time = current_time

        if rocket_launched:
            rocket.update(delta_time, map)
            rocket.draw()
            if rocket.exploded:
                holes_coordinates = explosion(holes_coordinates, rocket, created_teams, map)
                rocket_launched = False
                rocket = None
                end_round = True

        if aim_grenade_launched:
            fake_grenade.startPreviewTrajectory()
            fake_grenade.calculateTrajectory(map)
            fake_grenade.draw()
            if ((not (created_teams[team_playing].vikings[selected_viking].position.x == fake_grenade.position.x)) or
                    (not ((created_teams[team_playing].vikings[
                               selected_viking].position.y == fake_grenade.position.y + 35)))):
                fake_grenade.stopPreviewTrajectory()
                fake_grenade = None
                aim_grenade_launched = False

        if grenade_launched:
            if aim_grenade_launched:
                fake_grenade.stopPreviewTrajectory()
                fake_grenade = None
                aim_grenade_launched = False
            grenade.update(map)
            grenade.draw()
            if grenade.exploded:
                holes_coordinates = explosion(holes_coordinates, grenade, created_teams, map)
                grenade_launched = False
                grenade = None
                end_round = True

        key = pygame.key.get_pressed()
        GET_RPG_OUT = key[pygame.K_UP] or key[pygame.K_r]
        GET_GRENADE_OUT = key[pygame.K_DOWN] or key[pygame.K_f]

        if GET_RPG_OUT:
            if aim_grenade_launched:
                fake_grenade.stopPreviewTrajectory()
                fake_grenade = None
                aim_grenade_launched = False
            rocket_selected = True
        if GET_GRENADE_OUT:
            rocket_selected = False

        if key[pygame.K_DELETE]:
            vikings[0].there_was_ground = False
            vikings[0].jumping = False

        # check for a winner
        win = winCheck(number_teams, number_vikings, created_teams)
        # print(win)
        if win is not None:
            running_game = False
            winScreen(win)

        if end_round:
            end_round = False
            timer_started = False
            team_playing += 1

            if team_playing > number_teams - 1:
                team_playing = 0
            old_selected_viking = selected_viking
            while created_teams[team_playing].vikings[selected_viking].health <= 0:
                selected_viking += 1
                if selected_viking > number_vikings - 1:
                    selected_viking = 0
                if selected_viking == old_selected_viking:
                    team_playing += 1
                    if team_playing > number_teams - 1:
                        team_playing = 0
            nb_vikings_ok = 0
            while nb_vikings_ok == 0:
                for e_vikings in created_teams[team_playing].vikings:
                    if e_vikings.health > 0:
                        nb_vikings_ok += 1
                if nb_vikings_ok == 0:
                    team_playing += 1
                    if team_playing > number_teams - 1:
                        team_playing = 0

        # handle timer
        if (key[pygame.K_q] or key[pygame.K_d] or key[pygame.K_z] or key[pygame.K_SPACE] or mouse_pressed[1] or
            mouse_pressed[2]) and not timer_started:
            timer_started = True
            moving_start_time = pygame.time.get_ticks()

        remaining_time = MOVING_TIME
        if timer_started:
            remaining_time = MOVING_TIME - ((pygame.time.get_ticks() - moving_start_time) / 1000)
        if remaining_time <= 0:
            remaining_time = 0
            end_round = True
        if rocket_launched or grenade_launched:
            remaining_time = 0
        timer_text = font.render(str(int(remaining_time)), True, Colors.WHITE)
        screen.blit(timer_text, ((SCREEN_WIDTH / 2) - timer_text.get_width(), 5))

        left_select_viking = key[pygame.K_LEFT] or key[pygame.K_a]
        right_select_viking = key[pygame.K_RIGHT] or key[pygame.K_e]

        if (not timer_started and (not right_pressed or not left_pressed)
                and (right_select_viking or left_select_viking)):
            if not right_pressed and right_select_viking:
                right_pressed = True
                selected_viking += 1
                if selected_viking > number_vikings - 1:
                    selected_viking = 0
                old_selected_viking = selected_viking
                while created_teams[team_playing].vikings[selected_viking].health <= 0:
                    selected_viking += 1
                    if selected_viking > number_vikings - 1:
                        selected_viking = 0
                    if selected_viking == old_selected_viking:
                        team_playing += 1
                        if team_playing > number_teams - 1:
                            team_playing = 0
            if not left_pressed and left_select_viking:
                left_pressed = True
                selected_viking -= 1
                if selected_viking < 0:
                    selected_viking = number_vikings - 1
                old_selected_viking = selected_viking
                while created_teams[team_playing].vikings[selected_viking].health <= 0:
                    selected_viking -= 1
                    if selected_viking < 0:
                        selected_viking = number_vikings - 1
                    if selected_viking == old_selected_viking:
                        team_playing += 1
                        if team_playing > number_teams - 1:
                            team_playing = 0
        if not right_select_viking:
            right_pressed = False
        if not left_select_viking:
            left_pressed = False

        old_selected_viking = selected_viking
        while created_teams[team_playing].vikings[selected_viking].health <= 0:
            selected_viking += 1
            if selected_viking > number_vikings - 1:
                selected_viking = 0
            if selected_viking == old_selected_viking:
                team_playing += 1
                if team_playing > number_teams - 1:
                    team_playing = 0

        hp = font.render(str(created_teams[team_playing].vikings[selected_viking].health), True, Colors.RED)
        screen.blit(hp, (SCREEN_WIDTH - hp.get_width() - 10, 5))

        are_they_falling = []
        for viking in vikings:
            are_they_falling.append(viking.falling)
            if not viking.health <= 0:
                created_teams[team_playing].vikings[selected_viking].move(key, delta_time, remaining_time, map,
                                                                          rocket_selected)

                viking.doMath(map)
                viking.draw()

        screen.blit(DOWN_ARROW, ((created_teams[team_playing].vikings[selected_viking].position.x +
                                  int(created_teams[team_playing].vikings[selected_viking].image.get_width() / 2)) -
                                 int(DOWN_ARROW.get_width() / 2),
                                 created_teams[team_playing].vikings[selected_viking].position.y -
                                 created_teams[team_playing].vikings[selected_viking].image.get_height() * 2))

        for event in pygame.event.get():
            if key[pygame.K_DELETE]:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


running = True
while running:

    titleScreen()
    number_teams_and_vikings = loadMainMenu(DEFAULT_NUMBER_TEAMS, DEFAULT_NUMBER_VIKINGS)
    loadGame(number_teams_and_vikings[0], number_teams_and_vikings[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
