import os.path
import random

import pygame
from character import Player
import character
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


def loadGame(screen, teams, worms):
    runningGame = True
    while runningGame:
        screen.fill((0, 0, 0))
        # game here
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

terrain = Terrain(SCREEN_WIDTH, SCREEN_HEIGHT, (0, 255, 0), 24)  # Exemple de terrain vert
clock = pygame.time.Clock()

# Nombre d'équipes
num_teams = 2

# Liste des chemins d'accès aux images des joueurs pour chaque équipe
team_image_paths = [f"images/Viking{i}.png" for i in range(1, num_teams + 1)]  # Ajoutez des chemins pour chaque équipe supplémentaire

num_players_per_team = 4  # Nombre de joueurs par équipe

# Liste pour stocker les joueurs de chaque équipe
teams_players = []

# Définir la largeur minimale entre les joueurs
min_distance_between_players = 50  # Largeur minimale entre les joueurs

# Liste pour stocker les positions occupées
occupied_positions = []

# Positionnement aléatoire des joueurs pour chaque équipe
for team_image_path in team_image_paths:
    team_players = []

    for _ in range(num_players_per_team):
        player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, team_image_path)
        player_y = SCREEN_HEIGHT - terrain.cube_height
        player.position.y = player_y

        while True:
            player_x = random.randint(0, SCREEN_WIDTH - player.rect.width)  # Utilisation de la largeur du rectangle de l'image du joueur
            valid_position = True
            for pos in occupied_positions:
                if abs(player_x - pos) < min_distance_between_players:
                    valid_position = False
                    break
            if valid_position:
                player_x = min(player_x, SCREEN_WIDTH - player.rect.width)  # Ajustement pour éviter de sortir de l'écran
                occupied_positions.append(player_x)
                player.position.x = player_x
                break

        team_players.append(player)

    # Flip aléatoirement tous les joueurs de l'équipe
    if random.choice([True, False]):
        for player in team_players:
            player.image = pygame.transform.flip(player.image, True, False)

    teams_players.append(team_players)

# Liste pour stocker tous les joueurs
all_players = sum(teams_players, [])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Efface l'écran
    terrain.draw(screen)  # Dessine le terrain

    # Dessine tous les joueurs sur le terrain
    for team_players in teams_players:
        # Dessiner les joueurs de l'équipe
        for player in team_players:
            player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()