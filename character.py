import pygame

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
