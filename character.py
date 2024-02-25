from setting import *
from common_class import Position
from weapons import RPG7


class Team:
    def __init__(self, id, nb_viking):
        self.id = id
        self.vikings = []
        for i in range(nb_viking):
            self.vikings.append(Viking(i, image_path=f"images/player/Viking{id + 1}.png"))


class Viking:
    def __init__(self, id, name="", health=100, image_path="", flipped=False, speed_x=10):
        self.id = id
        self.name = name
        self.health = health

        self.position = Position(0, 0, speed_x=speed_x)
        self.flipped = flipped
        self.jumping = False
        self.falling = False
        self.there_was_ground = False
        self.jump_height = 100
        self.jump_velocity = 0
        self.initial_y = 0

        self.gravity = GRAVITY
        self.initial_time = 0

        self.rpg7 = RPG7(self.position.x - 10, self.position.y - 30)
        self.rpg7_visible = False

        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image,
                                            (int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.image = pygame.transform.flip(self.image, True, False) if self.flipped else self.image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y - self.rect.height))

    def capXandY(self):
        # cap x
        if (self.position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
            self.health = 0
        if self.position.x + int(self.rect.width / 2) < 0:
            self.position.x = 0 - int(self.rect.width / 2)
            self.health = 0
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE) - 1:
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 2
            self.health = 0
        if self.position.y <= 0:
            self.position.y = 1
            self.health = 0
        #

    def doMath(self, map):  # not meth
        self.capXandY()
        # falling calculations
        if map[int(self.position.x + int(self.rect.width / 2))][int(self.position.y + 1)] == 0 and not self.jumping:
            if not self.falling:
                self.setupFalling(self.position.y)
            time = (pygame.time.get_ticks() - self.initial_time) / 1000
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.position.y * time) + self.initial_y)
        #
        self.capXandY()
        # go above the ground
        while map[int(self.position.x + int(self.rect.width / 2))][int(self.position.y)] == 1:
            self.position.y -= TILE_SIZE
        #
        self.capXandY()
        # stop the fall
        if map[int(self.position.x + int(self.rect.width / 2))][
            int(self.position.y + 1)] == 1 and self.falling and not self.jumping:
            self.falling = False

    def setupFalling(self, initial_y):
        self.falling = True
        self.gravity = GRAVITY
        self.initial_y = initial_y
        self.initial_time = pygame.time.get_ticks()

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, key, delta_time, timer, bit_map, rocket_selected):
        left_movement = key[pygame.K_q]
        right_movement = key[pygame.K_d]

        if not timer <= 0:
            if left_movement:
                self.position.x -= self.position.speed_x * delta_time
                if self.flipped:
                    self.getFlipped(False)
                    self.rpg7.getFlipped(False)
            if right_movement:
                self.position.x += self.position.speed_x * delta_time
                if not self.flipped:
                    self.getFlipped(True)
                    self.rpg7.getFlipped(True)

        if key[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.setupJump(self.position.y, -50)

        if self.jumping:
            time = (pygame.time.get_ticks() - self.initial_time) / 100
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.jump_velocity * time) + self.initial_y)
            if not int(self.position.x + self.image.get_width() / 2) >= int(SCREEN_WIDTH / TILE_SIZE) - 1 and not int(
                    self.position.x + self.image.get_width() / 2) < 0 and not int(self.position.y + 2) >= int(
                    SCREEN_HEIGHT / TILE_SIZE) - 1 and not bit_map[int(self.position.x + self.image.get_width() / 2)][
                                                               int(self.position.y + 2)] == 1:
                self.there_was_ground = False

            if not self.position.y > int(
                    SCREEN_HEIGHT / TILE_SIZE) and not self.position.y < 0 and not self.there_was_ground:
                if bit_map[int(self.position.x + self.image.get_width() / 2)][int(self.position.y + 2)] == 1:
                    self.jumping = False

        if rocket_selected:
            self.draw_RPG7()

    def draw_RPG7(self):
        self.rpg7.position.x = self.position.x - 10
        self.rpg7.position.y = self.position.y - 30
        self.rpg7.draw()

    def setupJump(self, initial_y, jump_velocity):
        self.there_was_ground = True
        self.jumping = True
        self.initial_y = initial_y
        self.initial_time = pygame.time.get_ticks()
        self.gravity = GRAVITY
        self.jump_velocity = jump_velocity
