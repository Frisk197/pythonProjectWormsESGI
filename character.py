import math

from setting import *


class Position:
    def __init__(self, x, y, speed_x=10, speed_y=10, gravity=9.8, wind=0):
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
class Rocket:
    def __init__(self, x, y, angle, force, gravity, wind, drag_coefficient):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)  # Convertir l'angle en radians
        self.force = force
        self.gravity = gravity
        self.wind = wind
        self.explosion_radius = 10
        self.exploded = False
        self.drag_coefficient = drag_coefficient  # Coefficient de traînée
        self.original_image = pygame.image.load("images/weapons/Rocket.png")
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def update(self, delta_time, bitMap):
        if not self.exploded:
            if not self.exploded:
                time = pygame.time.get_ticks() / 1000  # Convertir le temps en secondes

                # Calculer les composantes x et y de la force initiale
                force_x = self.force * math.cos(self.angle)
                force_y = self.force * math.sin(self.angle)

                # Calculer la force de traînée en fonction de la vitesse
                drag_force_x = -0.5 * self.drag_coefficient * self.force * self.force * math.cos(self.angle)
                drag_force_y = -0.5 * self.drag_coefficient * self.force * self.force * math.sin(self.angle)

                # Mettre à jour les composantes x et y de la vitesse en fonction de la force, de la gravité, du vent et de la traînée
                self.x += (force_x + drag_force_x) * delta_time
                self.y += (force_y + drag_force_y + self.gravity) * delta_time + self.wind * delta_time

            # Vérifier si la roquette a atteint le sol, les bords de l'écran ou s'il y a une collision avec un obstacle
            if self.y <= 0 or self.y >= SCREEN_HEIGHT or self.x <= 0 or self.x >= SCREEN_WIDTH or self.check_collision(bitMap):
                self.explode()
    def check_collision(self, bitMap):
        # Insérer le code pour vérifier s'il y a collision avec un obstacle
        if bitMap[int(self.x)][int(self.y)] == 1:
            return True
        return False

    def explode(self):
        # Insérer le code pour gérer l'explosion de la roquette
        self.exploded = True
    def draw(self, screen):
        # Dessinez l'image de la roquette à sa position actuelle sur l'écran
        screen.blit(self.image, (self.x, self.y))

# Exemple d'utilisation :
def get_angle(viking_position, mouse_position):
    # Calculer la différence entre les coordonnées x des deux points
    delta_x = mouse_position[0] - viking_position[0]
    # Calculer la différence entre les coordonnées y des deux points
    delta_y = mouse_position[1] - viking_position[1]
    # Calculer l'angle en radians entre les deux points
    angle_radians = math.atan2(delta_y, delta_x)
    # Convertir l'angle en degrés
    angle_degrees = math.degrees(angle_radians)
    # Ajuster l'angle pour qu'il soit dans le bon intervalle
    if angle_degrees < 0:
        angle_degrees += 360
    return angle_degrees
class RPG7:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load("images/weapons/Rpg7.png")
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * SCALE_VIKING), int(self.original_image.get_height() * SCALE_VIKING)))
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

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
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE)-1:
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE)-2
        if self.position.y <= 0:
            self.position.y = 1
        #
        # falling calculations
        if map[int(self.position.x + int(self.rect.width/2))][int(self.position.y+1)] == 0 and not self.jumping:
            if not self.falling:
                print('start falling')
                self.setupFalling(self.position.y)
            time = (pygame.time.get_ticks() - self.initialTime) / 1000
            self.position.y = int((-0.5 * self.gravity) * (time * time) + (self.position.y * time) + self.initialY)
        #
        # go above the ground
        while map[int(self.position.x + int(self.rect.width / 2))][int(self.position.y)] == 1:
            self.position.y -= TILE_SIZE
        #
        # cap x
        if (self.position.x + int(self.rect.width / 2)) >= int(SCREEN_WIDTH / TILE_SIZE):
            self.position.x = int(SCREEN_WIDTH / TILE_SIZE) - int(self.rect.width / 2) - 1
        if self.position.x + int(self.rect.width / 2) < 0:
            self.position.x = 0 - int(self.rect.width / 2)
        #
        # cap y
        if self.position.y >= int(SCREEN_HEIGHT / TILE_SIZE)-1:
            self.position.y = int(SCREEN_HEIGHT / TILE_SIZE)-2
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

    def move(self, key, delta_time, timer, bitMap):
        up_movement = key[pygame.K_z]
        down_movement = key[pygame.K_s]
        left_movement = key[pygame.K_q]
        right_movement = key[pygame.K_d]

        # Vitesse de déplacement par seconde
        speed_x = self.position.speed_x
        speed_y = self.position.speed_y

        # Calcule les déplacements en fonction du delta_time et des touches enfoncées
        if not timer <= 0:
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
            if not int(self.position.x + self.image.get_width()/2) >= int(SCREEN_WIDTH/TILE_SIZE)-1 and not int(self.position.x + self.image.get_width()/2) < 0 and not int(self.position.y+2) >= int(SCREEN_HEIGHT/TILE_SIZE)-1 and not bitMap[int(self.position.x + self.image.get_width()/2)][int(self.position.y+2)] == 1:
                self.thereWasGround = False


            if not self.position.y > int(SCREEN_HEIGHT/TILE_SIZE) and not self.position.y < 0 and not self.thereWasGround:
                if bitMap[int(self.position.x + self.image.get_width()/2)][int(self.position.y+2)] == 1:
                    print('stop jumping')
                    self.jumping = False

        if key[pygame.K_UP]:
            self.draw_RPG7()

    def draw_RPG7(self):
        # Créer un objet de rocket à la position du viking
        LaunchRPG7=RPG7(self.position.x, self.position.y-40)
        # Dessiner le rocket à l'écran
        LaunchRPG7.draw()

    def setupJump(self, initialY, jump_velocity):
        self.thereWasGround = True
        self.jumping = True
        self.initialY = initialY
        self.initialTime = pygame.time.get_ticks()
        self.gravity = GRAVITY
        self.jump_velocity = jump_velocity  # Vitesse initiale du saut