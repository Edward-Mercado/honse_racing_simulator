import pygame

def get_opposite_direction(direction):
    opposite_directions = {
        "UP" : "DOWN",
        "DOWN" : "UP",
        "LEFT" : "RIGHT",
        "RIGHT" : "LEFT",
    }
    
    try:
        return opposite_directions[direction]
    except KeyError:
        return "INVALID"

def handle_wall_collision(horse, walls, direction):
    for wall in walls:
        if pygame.Rect(wall).colliderect(horse.rect):
            horse.swap_horse_vectors(direction)
            
    
def handle_horse_collision(horse, horses, direction):
    pass