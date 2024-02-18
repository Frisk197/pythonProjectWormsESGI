from setting import *


class Position:
    def __init__(self, x, y, speed_x=5, speed_y=5, direction=1, gravity=9.8, wind=0):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = direction
        self.gravity = gravity
        self.wind = wind


class Team:
    def __init__(self, id, nb_viking):
        self.id = id
        self.vikings = []
        for i in range(nb_viking):
            self.vikings.append(Viking(i, image_path=f"images/player/Viking{id + 1}.png"))


class Viking:
    def __init__(self, id, name="", health=100, image_path="", flipped=False):
        self.falling = False
        self.id = id
        self.name = name
        self.health = health
        self.position = Position(0, 0)
        self.flipped = flipped

        self.stock_rocket = 5
        self.stock_grenade = 2
        self.is_aiming = False
        self.send_grenade = False
        self.grenade = Grenade(10, x=self.position.x, y=self.position.y - 50, direction=self.position.direction)

        self.raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.image = pygame.transform.flip(self.image, True, False) if self.flipped else self.image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y - self.rect.height))

    def doMath(self, map):  # not meth
        # cap x
        if (self.position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
        if self.position.x + int(self.rect.width / 2) < 0:
            self.position.x = 0 - int(self.rect.width / 2)
        #
        # go above the ground
        while map[self.position.x + int(self.rect.width / 2)][self.position.y] == 1:
            self.position.y -= TILE_SIZE
        #
        # falling calculations
        if map[self.position.x + int(self.rect.width / 2)][self.position.y + 1] == 0:
            if not self.falling:
                self.setupFalling(self.position.y)
            time = (pygame.time.get_ticks() - self.initialTime) / 1000
            self.position.y = int(-0.5 * self.gravity * time * time + self.position.y * time + self.initialY)
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE):
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 10
        if self.position.y <= 0:
            self.position.y = 1
        #
        # stop the fall
        if map[self.position.x + int(self.rect.width / 2)][self.position.y + 1] == 1:
            self.falling = False
        #

    def setupFalling(self, initialY):
        self.falling = True
        self.gravity = GRAVITY
        self.initialY = initialY
        self.initialTime = pygame.time.get_ticks()

    def shoot(self):
        if self.stock_rocket > 0:
            self.stock_rocket -= 1
        else:
            print(f"{self.name} has no rocket")

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} died")
        else:
            print(f"{self.name} has lost {damage} health")

    def reload(self):
        self.stock_rocket = 5

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, key):
        left_movement = key[pygame.K_q] or key[pygame.K_LEFT]
        right_movement = key[pygame.K_d] or key[pygame.K_RIGHT]
        dx = 0
        dy = 0

        if left_movement:
            if self.flipped:
                self.getFlipped(flipped=False)
                self.position.direction = -1
            dx -= self.position.speed_x
        if right_movement:
            if not self.flipped:
                self.getFlipped(flipped=True)
                self.position.direction = 1
            dx += self.position.speed_x

        self.position.x += dx
        self.position.y += dy


class Grenade:
    def __init__(self, damage, timer=15, x=0, y=0, direction=1):
        self.position = Position(x, y, speed_x=50, speed_y=-50, direction=direction)
        self.damage = damage
        self.timer = timer

        self.falling = False
        self.preview_trajectory = False
        self.preview_points = []

        self.raw_image = pygame.image.load(f"images/weapons/Grenade.png")
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

        self.angle = math.pi / 4

    def update(self, map):
        if map[int(self.position.x / TILE_SIZE)][int(self.position.y / TILE_SIZE)] == 1:
            self.position.speed_x = 0
            self.position.speed_y = 0
            self.falling = False
            return

        self.position.speed_y += self.position.gravity
        dx = math.cos(self.angle) * self.position.speed_x
        dy = math.sin(self.angle) * self.position.speed_y - GRAVITY

        self.position.x += dx * self.position.direction
        self.position.y += dy

        if (self.position.y + int(self.rect.height / 2)) >= int(SCREEN_HEIGHT / TILE_SIZE):
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - int(self.rect.height / 2) - 1

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

    def calculate_trajectory(self):
        simulated_position = Position(self.position.x, self.position.y, speed_x=self.position.speed_x,
                                      speed_y=self.position.speed_y, gravity=self.position.gravity,
                                      direction=self.position.direction)

        for i in range(100):
            simulated_position.speed_y += simulated_position.gravity
            dx = simulated_position.direction * simulated_position.speed_x
            dy = simulated_position.speed_y

            simulated_position.x += dx
            simulated_position.y += dy

            self.preview_points.append((simulated_position.x, simulated_position.y))
