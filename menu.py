from setting import *

def drawText(x, y, string, color, size=70, outshift=0):
    font = pygame.font.SysFont("Tahoma", size, bold=True)
    text = font.render(string, True, color)
    textbox = x - (text.get_width() / 2), (y + (text.get_height()) + outshift)

    screen.blit(text, textbox)
    return text

# TEXT OUTLINE
def drawTextOutline(text, main_color, outline_color, x, y, outshift=0, size=70):
    # top left
    drawText(x - 2, y - 2, text, outline_color, size, outshift)
    # top right
    drawText(x + 2, y - 2, text, outline_color, size, outshift)
    # btm left
    drawText(x - 2, y + 2, text, outline_color, size, outshift)
    # btm right
    drawText(x + 2, y + 2, text, outline_color, size, outshift)

    return drawText(x, y, text, main_color, size, outshift=outshift,)

def titleScreen():
    running_title_screen = True

    while running_title_screen:
        screen.blit(TITLE_SCREEN, TITLE_SCREEN.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                running_title_screen = False
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


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

        screen.blit(SKY_BG_MENU, SKY_BG_MENU.get_rect())

        line1_text = f"Équipes: {teams}"
        line2_text = f"Vikings par équipes: {vikings} "
        line3_text = "Appuyez sur ENTRER pour commencer"

        clipping_color = (255 * opacity, 255 * opacity, 255 * opacity)

        line1_label = drawTextOutline(line1_text, Colors.WHITE, Colors.BLACK, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), -300)
        line2_label = drawTextOutline(line2_text, Colors.WHITE, Colors.BLACK, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), -200)
        drawText((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), line3_text, clipping_color, size=50, outshift=100)

        screen.blit(UP_ARROW, ((SCREEN_WIDTH / 2) + (line1_label.get_width() / 2) + 25,
                               (SCREEN_HEIGHT / 2) - (line1_label.get_height() + 1.5) - 120))
        screen.blit(DOWN_ARROW, ((SCREEN_WIDTH / 2) + (line1_label.get_width() / 2) + 25,
                                 (SCREEN_HEIGHT / 2) - (line1_label.get_height() / 1.5) - 120))

        screen.blit(LEFT_ARROW, ((SCREEN_WIDTH / 2) + (line2_label.get_width() / 2),
                                 (SCREEN_HEIGHT / 2) + (line2_label.get_height()) - 180))
        screen.blit(RIGHT_ARROW, ((SCREEN_WIDTH / 2) + (line2_label.get_width() / 2) + 30,
                                  (SCREEN_HEIGHT / 2) + (line2_label.get_height()) - 180))

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


def winScreen(team):
    running_win_screen = True

    while running_win_screen:
        screen.blit(WIN_BG, WIN_BG.get_rect())

        line1_text = f"Victoire Team {team.id + 1}"
        line2_text = "Play again ? [SPACE]"
        line3_text = "Stop ? [DEL]"

        drawTextOutline(line1_text, Colors.YELLOW, Colors.BLACK, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), outshift=-300)
        drawTextOutline(line2_text, Colors.WHITE, Colors.BLACK, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), outshift=0, size=50)
        drawTextOutline(line3_text, Colors.WHITE, Colors.BLACK, (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), outshift=100, size=50)

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            running_win_screen = False

        for event in pygame.event.get():
            if key[pygame.K_DELETE]:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
