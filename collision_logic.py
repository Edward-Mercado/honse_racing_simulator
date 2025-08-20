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

def handle_wall_collision(horse, fields, direction):
    horse_hit_wall = True
    for field in fields:
        if pygame.Rect((field)).colliderect(horse.rect):
            horse_hit_wall = False
            
    
def handle_horse_collision(horse, horses, direction):
    pass

def get_horse_start_pos(horses, map):
    return 400, 400