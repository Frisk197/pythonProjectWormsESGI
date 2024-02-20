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
    def __init__(self, id, name="", health=100, image_path="", flipped=False):
        self.falling = False
        self.id = id
        self.name = name
        self.health = health
        self.position = Position(0, 0)
        self.flipped = flipped
        self.jumping = False
        self.isMoving = False
        self.jump_height = 100
        self.jump_velocity = 0
        self.initialY = 0
        self.rpg7 = RPG7(self.position.x - 10, self.position.y - 30)
        self.rpg7_visible = False
        self.raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.raw_image, (
        int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
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
            time = (pygame.time.get_ticks() - self.initialTime) / 1000
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.position.y * time) + self.initialY)
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

    def setupFalling(self, initialY):
        self.falling = True
        self.gravity = GRAVITY
        self.initialY = initialY
        self.initialTime = pygame.time.get_ticks()

    def getFlipped(self, flipped):
        self.flipped = flipped
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, key, delta_time, timer, bitMap, rocketSelected):
        left_movement = key[pygame.K_q]
        right_movement = key[pygame.K_d]

        self.isMoving = False

        if not timer <= 0:
            if left_movement:
                self.position.x -= self.position.speed_x * delta_time
                self.isMoving: True
                if self.flipped:
                    self.getFlipped(False)
                    self.rpg7.getFlipped(False)
            if right_movement:
                self.position.x += self.position.speed_x * delta_time
                self.isMoving: True
                if not self.flipped:
                    self.getFlipped(True)
                    self.rpg7.getFlipped(True)

        if key[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.isMoving: True
            self.setupJump(self.position.y, -50)

        if self.jumping:
            self.isMoving: True
            time = (pygame.time.get_ticks() - self.initialTime) / 100
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.jump_velocity * time) + self.initialY)
            if not int(self.position.x + self.image.get_width() / 2) >= int(SCREEN_WIDTH / TILE_SIZE) - 1 and not int(
                    self.position.x + self.image.get_width() / 2) < 0 and not int(self.position.y + 2) >= int(
                    SCREEN_HEIGHT / TILE_SIZE) - 1 and not bitMap[int(self.position.x + self.image.get_width() / 2)][
                                                               int(self.position.y + 2)] == 1:
                self.thereWasGround = False

            if not self.position.y > int(
                    SCREEN_HEIGHT / TILE_SIZE) and not self.position.y < 0 and not self.thereWasGround:
                if bitMap[int(self.position.x + self.image.get_width() / 2)][int(self.position.y + 2)] == 1:
                    print('stop jumping')
                    self.jumping = False

        if rocketSelected:
            self.draw_RPG7()

    def draw_RPG7(self):
        self.rpg7.position.x = self.position.x - 10
        self.rpg7.position.y = self.position.y - 30
        self.rpg7.draw()

    def setupJump(self, initialY, jump_velocity):
        self.thereWasGround = True
        self.jumping = True
        self.initialY = initialY
        self.initialTime = pygame.time.get_ticks()
        self.gravity = GRAVITY
        self.jump_velocity = jump_velocity
