from random import random

import pygame


class Position:
    def __init__(self, x, y, speed_x=5, speed_y=5, gravity=9.8, wind=0):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.wind = wind

class Team:
    def __init__(self, id, nbViking):
        self.id = id
        self.vikings = []
        for i in range(nbViking):
            self.vikings.append(Viking(i, image_path=f"images/Viking{id+1}.png"))

class Viking:
    def __init__(self, id, name="", health=100, image_path="", flipped=False):
        self.id = id
        self.name = name
        self.health = health
        self.stockRocket = 5
        self.stockGrenade = 2
        self.position = Position(0,0)
        self.flipped = flipped
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y - self.rect.height))

    def shoot(self):
        if self.stockRocket > 0:
            self.stockRocket -= 1
        else:
            print(f"{self.name} has no rocket")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} die")
        else:
            print(f"{self.name} has lost health")

    def reload(self):
        self.stockRocket = 5


def movements(key, character):
    up_movement = key[pygame.K_z] or key[pygame.K_UP]
    down_movement = key[pygame.K_s] or key[pygame.K_DOWN]
    left_movement = key[pygame.K_q] or key[pygame.K_LEFT]
    right_movement = key[pygame.K_d] or key[pygame.K_RIGHT]

    if left_movement:
        if up_movement != down_movement:
            character.move_ip(-1, 0)
        else:
            character.move_ip(-2, 0)
    if right_movement:
        if up_movement != down_movement:
            character.move_ip(1, 0)
        else:
            character.move_ip(2, 0)
    if up_movement:
        if left_movement != right_movement:
            character.move_ip(0, -1)
        else:
            character.move_ip(0, -2)
    if down_movement:
        if left_movement != right_movement:
            character.move_ip(0, 1)
        else:
            character.move_ip(0, 2)
