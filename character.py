from setting import *


class Position:
    def __init__(self, x, y, speed_x=100, speed_y=100, gravity=9.8, wind=0):
        self.x = x
        self.y = y
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
        self.falling = False
        self.id = id
        self.name = name
        self.health = health
        self.stock_rocket = 5
        self.stock_grenade = 2
        self.position = Position(0, 0)
        self.flipped = flipped
        self.jumping = False
        self.jump_height = 100  # Hauteur maximale du saut (à ajuster selon vos besoins)
        self.jump_velocity = 0  # Vélocité initiale du saut
        self.initialY = 0  # Initialisez la position initiale du saut
        self.raw_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * SCALE_VIKING), int(self.raw_image.get_height() * SCALE_VIKING)))
        self.image = pygame.transform.flip(self.image, True, False) if self.flipped else self.image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.position.x, self.position.y - self.rect.height))

    def doMath(self, map): # not meth
        # cap x
        if (self.position.x + int(self.rect.width/2)) >= int(SCREEN_WIDTH/TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH/TILE_SIZE) - int(self.rect.width/2)-1
        if self.position.x + int(self.rect.width/2) < 0:
            self.position.x = 0 - int(self.rect.width/2)
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE):
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 10
        if self.position.y <= 0:
            self.position.y = 1
        #
        # go above the ground
        while map[int(self.position.x + int(self.rect.width/2))][int(self.position.y)] == 1:
            self.position.y -= TILE_SIZE
        #
        # falling calculations
        if map[int(self.position.x + int(self.rect.width/2))][int(self.position.y+1)] == 0 and not self.jumping:
            if not self.falling:
                print('start falling')
                self.setupFalling(self.position.y)
            time = (pygame.time.get_ticks() - self.initialTime) / 1000
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.position.y * time) + self.initialY)
        #
        # cap x
        if (self.position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
        if self.position.x + int(self.rect.width / 2) < 0:
            self.position.x = 0 - int(self.rect.width / 2)
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE):
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE) - 10
        if self.position.y <= 0:
            self.position.y = 1
        #
        # stop the fall
        if map[int(self.position.x + int(self.rect.width / 2))][int(self.position.y + 1)] == 1 and self.falling and not self.jumping:
            self.falling = False
            print('stop falling')


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

    def getFlipped(self):
        self.flipped = True
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, key, delta_time, map):

        # Vitesse de déplacement par seconde
        speed_x = self.position.speed_x
        speed_y = self.position.speed_y

        # Calcule les déplacements en fonction du delta_time et des touches enfoncées
        if key[pygame.K_q]:
            self.position.x -= speed_x * delta_time
            # print('gauche')
        if key[pygame.K_d]:
            self.position.x += speed_x * delta_time
            # print('droite')

        if key[pygame.K_SPACE] and not self.jumping and not self.falling:
            print(self.falling)
            print('start jumping')
            self.setupJump(self.position.y, -50)

        if self.jumping:
            time = (pygame.time.get_ticks() - self.initialTime)/100
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.jump_velocity * time) + self.initialY)
            if not int(self.position.x + self.image.get_width()/2) >= int(SCREEN_WIDTH/TILE_SIZE)-1 and not int(self.position.x + self.image.get_width()/2) < 0 and not int(self.position.y+2) >= int(SCREEN_HEIGHT/TILE_SIZE)-1 and not map[int(self.position.x + self.image.get_width()/2)][int(self.position.y+2)] == 1:
                self.thereWasGround = False


            if not self.position.y > int(SCREEN_HEIGHT/TILE_SIZE) and not self.position.y < 0 and not self.thereWasGround:
                if map[int(self.position.x + self.image.get_width()/2)][int(self.position.y+2)] == 1:
                    print('stop jumping')
                    self.jumping = False



    def setupJump(self, initialY, jump_velocity):
        self.thereWasGround = True
        self.jumping = True
        self.initialY = initialY
        self.initialTime = pygame.time.get_ticks()
        self.gravity = GRAVITY
        self.jump_velocity = jump_velocity  # Vitesse initiale du saut