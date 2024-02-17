import pygame

class Terrain:
    def __init__(self, width, height, color, num_cubes):
        self.width = width
        self.height = height
        self.color = color
        self.num_cubes = num_cubes
        self.cube_height = height // num_cubes

    def draw(self, screen):
        # Dessiner la plateforme
        pygame.draw.rect(screen, self.color, (0, self.height - self.cube_height, self.width, self.cube_height))

        # Dessiner les cubes
        for i in range(self.num_cubes):
            pygame.draw.rect(screen, (255, 0, 0), (i * (self.width // self.num_cubes), self.height - self.cube_height, self.width // self.num_cubes, self.cube_height))