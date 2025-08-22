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

def handle_wall_collision(horse, field_hitboxes, direction):
    horse_hit_wall = False
    
    for field_hitbox in field_hitboxes:
        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(field_hitbox):
            horse_hit_wall = True  
            
    if horse_hit_wall == False:
        if direction == "UP":
            horse.location_y += 8 * horse.speed
            horse.vector_down["vector_measurement"] = horse.vector_up["vector_measurement"]
            horse.vector_up["vector_measurement"] = 0
            
        elif direction == "DOWN":
            horse.location_y -= 8 * horse.speed
            horse.vector_up["vector_measurement"] = horse.vector_down["vector_measurement"]
            horse.vector_down["vector_measurement"] = 0

        elif direction == "LEFT":
            horse.location_x += 8 * horse.speed
            horse.vector_right["vector_measurement"] = horse.vector_left["vector_measurement"]
            horse.vector_left["vector_measurement"] = 0
            
        elif direction == "RIGHT":
            horse.location_x -= 8 * horse.speed
            horse.vector_left["vector_measurement"] = horse.vector_right["vector_measurement"]
            horse.vector_right["vector_measurement"] = 0
        
    return horse_hit_wall

def handle_horse_collision(horse, horses, direction):
    pass

def get_horse_start_pos(horses, map):
    return 400, 400