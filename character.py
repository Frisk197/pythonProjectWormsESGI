from pygame import Vector2

from setting import *


class Position:
    def __init__(self, x, y, speed_x=2, speed_y=1, direction=1, gravity=1, wind=0):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed_x = speed_x
        self.speed_y = speed_y
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
        self.id = id
        self.name = name
        self.health = health
        self.stock_rocket = 5
        self.stock_grenade = 2
        self.position = Position(0, 0)

        self.send_grenade = False

        self.flipped = flipped
        self.raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.image = pygame.transform.flip(self.image, True, False) if self.flipped else self.image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y - self.rect.height))

    def shoot(self):
        if self.stock_rocket > 0:
            self.stock_rocket -= 1
        else:
            print(f"{self.name} has no rocket")

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} die")
        else:
            print(f"{self.name} has lost health")

    def reload(self):
        self.stock_rocket = 5

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)

    def moveTest(self, x, y):
        pygame.mouse.set_pos(x, y)

    def move(self, key):
        up_movement = key[pygame.K_z] or key[pygame.K_UP]
        down_movement = key[pygame.K_s] or key[pygame.K_DOWN]
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

        if up_movement:
           dy -= self.position.speed_y
        if down_movement:
            dy += self.position.speed_y

        if self.position.y + dy > 700:
            dy = 700 - self.rect.bottom

        self.position.x += dx
        self.position.y += dy


class Grenade:
    def __init__(self, name, damage, timer=0, x=0, y=0, direction=1):
        self.position = Position(x, y, speed_x=10, speed_y=-15, gravity=0.80, direction=direction)
        self.damage = damage
        self.timer = timer

        self.preview_trajectory = False
        self.preview_points = []
        self.raw_image = pygame.image.load(f"images/weapons/{name}.png")
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self):
        self.position.speed_y += self.position.gravity
        dx = self.position.direction * self.position.speed_x
        dy = self.position.speed_y

        # update grenade position
        self.position.x += dx
        self.position.y += dy

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y))

        if self.preview_trajectory:
            for point in self.preview_points:
                pygame.draw.circle(screen, (255, 0, 0), (int(point[0]), int(point[1])), 2)

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
