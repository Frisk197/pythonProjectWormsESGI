import math

from setting import *
from common_class import Position


class Rocket:
    def __init__(self, x, y, angle, force, gravity, wind, drag_coefficient):
        self.x = x
        self.y = y
        self.initialX = x
        self.initialY = y
        self.mouseInitialX = pygame.mouse.get_pos()[0]
        self.mouseInitialY = pygame.mouse.get_pos()[1]
        self.initialTime = pygame.time.get_ticks()
        self.angle = angle * math.pi / 180
        self.force = force
        self.gravity = GRAVITY
        self.wind = wind
        self.explosion_radius = 10
        self.exploded = False
        self.drag_coefficient = drag_coefficient  # Coefficient de traînée
        self.original_image = pygame.image.load("images/weapons/Rocket.png")
        self.image = pygame.transform.scale(self.original_image, (
        int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self, delta_time, bitMap):
        if not self.exploded:
            if not self.exploded:
                time = (pygame.time.get_ticks() - self.initialTime) / 1000

                force_x = 330 * math.cos(self.angle)
                force_y = 330 * math.sin(self.angle)

                drag_force_x = force_x * time + self.initialX * self.drag_coefficient
                drag_force_y = (-0.5 * (-9.8 *10) ) * (time ** 2) + force_y * time + self.initialY

                self.x = drag_force_x
                self.y = drag_force_y

            if self.y <= 0 or self.y >= SCREEN_HEIGHT or self.x <= 0 or self.x >= SCREEN_WIDTH or self.check_collision(
                    bitMap):
                self.explode()

    def check_collision(self, bitMap):
        if bitMap[int(self.x)][int(self.y)] == 1:
            return True
        return False

    def capXandY(self):
        # cap x
        if (self.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
            self.explode()
        if self.x + int(self.rect.width / 2) < 0:
            self.x = 0 - int(self.rect.width / 2)
            self.explode()
        #
        # cap y
        if self.y >= int(SCREEN_HEIGHT / TILE_SIZE) - 1:
            self.y = int(SCREEN_HEIGHT / TILE_SIZE) - 2
            self.explode()
        if self.y <= 0:
            self.y = 1
            self.explode()

    def explode(self):
        self.exploded = True

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def get_angle(viking_position, mouse_position):
    delta_x = mouse_position[0] - viking_position[0]
    delta_y = mouse_position[1] - viking_position[1]
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    if angle_degrees < 0:
        angle_degrees += 360
    return angle_degrees


class RPG7:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load("images/weapons/Rpg7.png")
        self.image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Grenade:
    def __init__(self, x, y, angle, speed_x, speed_y):
        if speed_x > 50:
            speed_x = 50
        if speed_x < 1:
            speed_x = 1

        if speed_y < 1:
            speed_y = 1

        if speed_y > 70:
            speed_y = 70

        self.position = Position(x, y, speed_x, -speed_y)
        self.damage = 50
        self.timer = 5

        self.isTimeStarted = False
        self.timeStarted = 0
        self.remainingTime = 0

        self.falling = True
        self.preview_trajectory = False
        self.preview_points = []

        self.angle = math.radians(angle)
        self.exploded = False

        self.raw_image = pygame.image.load(f"images/weapons/Grenade.png")
        self.image = pygame.transform.scale(self.raw_image, (
        int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self, map):

        if not self.isTimeStarted:
            self.isTimeStarted = True
            self.timeStarted = pygame.time.get_ticks()

        if self.isTimeStarted:
            self.remainingTime = self.timer - ((pygame.time.get_ticks() - self.timeStarted) / 1000)
            if self.remainingTime <= 0:
                self.remainingTime = 0
                self.explode()

        if self.position.y <= 0 or self.position.y >= SCREEN_HEIGHT or self.position.x <= 0 or self.position.x >= SCREEN_WIDTH or self.check_collision(
                map):
            self.falling = False
            while self.check_collision(map):
                self.position.y -= 1
            return

        # if touch the ground
        # if map[int(self.position.x / TILE_SIZE)][int(self.position.y / TILE_SIZE)] == 1:
        #    self.position.speed_x = 0
        #    self.position.speed_y = 0
        #    self.falling = False
        #    return
        if self.falling:
            self.position.speed_y += self.position.gravity
            dx = math.cos(self.angle) * self.position.speed_x
            dy = math.sin(self.angle) * self.position.speed_y - GRAVITY

            if (math.sin(self.angle) < 1):
                dy = 1 * self.position.speed_y - GRAVITY

            if (math.cos(self.angle) > 0.7):
                dx = 0.7 * self.position.speed_x
            if (math.cos(self.angle) < -0.7):
                dx = -0.7 * self.position.speed_x

            self.position.x += dx
            self.position.y += dy

            # if go outside map
            self.capXandY()

    def capXandY(self):
        # cap x
        if (self.position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
            self.explode()
        if self.position.x + int(self.rect.width / 2) < 0:
            self.position.x = 0 - int(self.rect.width / 2)
            self.explode()
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE) - 1:
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 2
            self.explode()
        if self.position.y <= 0:
            self.position.y = 1
            self.explode()

    def check_collision(self, bitMap):
        if bitMap[int(self.position.x)][int(self.position.y)] == 1:
            return True
        return False

    def explode(self):
        self.exploded = True

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y))

        if self.preview_trajectory:
            for point in self.preview_points:
                pygame.draw.circle(screen, Colors.WHITE, (int(point[0]), int(point[1])), 2)

    def start_preview_trajectory(self):
        self.preview_trajectory = True
        self.preview_points.clear()

    def stop_preview_trajectory(self):
        self.preview_trajectory = False
        self.preview_points.clear()

    def calculate_trajectory(self, map):
        simulated_position = Position(self.position.x, self.position.y, speed_x=self.position.speed_x,
                                      speed_y=self.position.speed_y, gravity=self.position.gravity)

        for i in range(50):
            # cap y
            if (simulated_position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
                simulated_position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
            if simulated_position.x + int(self.rect.width / 2) < 0:
                simulated_position.x = 0 - int(self.rect.width / 2)
            # cap y
            if simulated_position.y >= int(SCREEN_HEIGHT / TILE_SIZE) - 1:
                simulated_position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 2
            if simulated_position.y <= 0:
                simulated_position.y = 1

            simulated_position.speed_y += simulated_position.gravity
            dx = math.cos(self.angle) * simulated_position.speed_x
            dy = math.sin(self.angle) * simulated_position.speed_y - GRAVITY

            print((math.cos(self.angle), math.sin(self.angle)))

            if (math.sin(self.angle) < 1):
                dy = 1 * simulated_position.speed_y - GRAVITY

            if (math.cos(self.angle) > 0.7):
                dx = 0.7 * simulated_position.speed_x
            if (math.cos(self.angle) < -0.7):
                dx = -0.7 * simulated_position.speed_x
            # if (math.sin(self.angle) > 1):

            if map[int(simulated_position.x / TILE_SIZE)][int(simulated_position.y / TILE_SIZE)] == 1:
                simulated_position.speed_x = 0
                simulated_position.speed_y = 0
                return

            simulated_position.x += dx
            simulated_position.y += dy

            self.preview_points.append((simulated_position.x, simulated_position.y))
