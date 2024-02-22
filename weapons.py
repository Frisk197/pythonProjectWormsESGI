from setting import *
from common_class import Position


def getAngle(viking_position, mouse_position):
    delta_x = mouse_position[0] - viking_position[0]
    delta_y = mouse_position[1] - viking_position[1]
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    if angle_degrees < 0:
        angle_degrees += 360
    return angle_degrees


class Rocket:
    def __init__(self, x, y, angle, force=35, gravity=9.8, wind=2, drag_coefficient=0.75):
        self.position = Position(x, y)
        self.angle = math.radians(angle)

        self.force = force
        self.gravity = gravity
        self.wind = wind
        self.drag_coefficient = drag_coefficient  # Coefficient de traînée

        self.damage = 100
        self.explosion_radius = 10
        self.exploded = False

        self.flipped = False
        self.original_image = pygame.image.load("images/weapons/Rocket.png")
        self.image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self, delta_time, bit_map):
        if not self.exploded:
            if not self.exploded:
                force_x = self.force * math.cos(self.angle)
                force_y = self.force * math.sin(self.angle)

                drag_force_x = -0.5 * self.drag_coefficient * self.force * self.force * math.cos(self.angle)
                drag_force_y = -0.5 * self.drag_coefficient * self.force * self.force * math.sin(self.angle)

                self.position.x += (force_x + drag_force_x) * delta_time
                self.position.y += (force_y + drag_force_y + self.gravity) * delta_time + self.wind * delta_time

            if (self.position.y <= 0 or self.position.x <= 0 or
                    self.position.y >= SCREEN_HEIGHT or self.position.x >= SCREEN_WIDTH or
                    self.checkCollision(bit_map)):
                self.explode()

    def checkCollision(self, bit_map):
        if bit_map[int(self.position.x)][int(self.position.y)] == 1:
            return True
        return False

    def explode(self):
        self.exploded = True

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y))

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)


class RPG7:
    def __init__(self, x, y):
        self.position = Position(x, y)
        self.flipped = False
        self.original_image = pygame.image.load("images/weapons/Rpg7.png")
        self.image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y))

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)


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

        self.is_time_started = False
        self.time_started = 0
        self.remaining_time = 0

        self.falling = True
        self.preview_trajectory = False
        self.preview_points = []

        self.angle = math.radians(angle)
        self.exploded = False

        self.original_image = pygame.image.load(f"images/weapons/Grenade.png")
        self.image = pygame.transform.scale(self.original_image, (
            int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self, map):

        if not self.is_time_started:
            self.is_time_started = True
            self.time_started = pygame.time.get_ticks()

        if self.is_time_started:
            self.remaining_time = self.timer - ((pygame.time.get_ticks() - self.time_started) / 1000)
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.explode()

        if (self.position.y <= 0 or self.position.x <= 0 or
                self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE) or self.position.x >= int(SCREEN_WIDTH / TILE_SIZE) or
                self.checkCollision(map)):
            self.falling = False
            while self.checkCollision(map):
                self.position.y -= 1
            return

        if self.falling and not self.exploded:
            self.position.speed_y += self.position.gravity
            dx = math.cos(self.angle) * self.position.speed_x
            dy = math.sin(self.angle) * self.position.speed_y - GRAVITY

            if math.sin(self.angle) < 1:
                dy = 1 * self.position.speed_y - GRAVITY

            if math.cos(self.angle) > 0.7:
                dx = 0.7 * self.position.speed_x
            if math.cos(self.angle) < -0.7:
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

    def checkCollision(self, bit_map):
        if bit_map[int(self.position.x)][int(self.position.y)] == 1:
            return True
        return False

    def explode(self):
        self.exploded = True

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y))

        if self.preview_trajectory:
            for point in self.preview_points:
                pygame.draw.circle(screen, Colors.WHITE, (int(point[0]), int(point[1])), 2)

    def startPreviewTrajectory(self):
        self.preview_trajectory = True
        self.preview_points.clear()

    def stopPreviewTrajectory(self):
        self.preview_trajectory = False
        self.preview_points.clear()

    def calculateTrajectory(self, map):
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

            # print((math.cos(self.angle), math.sin(self.angle)))

            if math.sin(self.angle) < 1:
                dy = 1 * simulated_position.speed_y - GRAVITY

            if math.cos(self.angle) > 0.7:
                dx = 0.7 * simulated_position.speed_x
            if math.cos(self.angle) < -0.7:
                dx = -0.7 * simulated_position.speed_x

            if map[int(simulated_position.x / TILE_SIZE)][int(simulated_position.y / TILE_SIZE)] == 1:
                simulated_position.speed_x = 0
                simulated_position.speed_y = 0
                return

            simulated_position.x += dx
            simulated_position.y += dy

            self.preview_points.append((simulated_position.x, simulated_position.y))
