import pygame, math, random

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

def get_corner_distance(corners, center):
    distances = []
    for corner in corners:
        distance = int(math.sqrt((corner[0] - center[0])**2 + (corner[1] - center[1])**2))
        distances.append(distance)
    return min(distances)
    
def handle_wall_collision(horse, field_hitboxes, direction, circle_fields):
    horse_hit_wall = True
    horse_hit_circle = False
    
    for field_hitbox in field_hitboxes:
        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(field_hitbox):
            horse_hit_wall = False
   
    for circle_field in circle_fields:
        corner_TL = (horse.location_x, horse.location_y)
        corner_BL = (horse.location_x, horse.location_y+horse.height)
        corner_TR = (horse.location_x + horse.width, horse.location_y)
        corner_BR = (horse.location_x + horse.width, horse.location_y+horse.width)
        corners = [corner_TL, corner_BL, corner_BR, corner_TR]
        
        min_distance = get_corner_distance(corners, (circle_field[0], circle_field[1]))
        
        if min_distance < circle_field[2] - 20:
            horse_hit_wall = False
            horse_hit_circle = True
            
    if horse_hit_wall == True:
        horse.past_directions.append(direction)
        
        if direction == "UP":
            horse.location_y += 8 * horse.speed
            horse.vector_down["vector_measurement"] = horse.vector_up["vector_measurement"]
            if horse_hit_circle == True:
                horse.vector_down["vector_measurement"] = random.randint(1, 6)
                horse.fit_movement_vectors()
            horse.vector_up["vector_measurement"] = 0
            
        elif direction == "DOWN":
            horse.location_y -= 8 * horse.speed
            horse.vector_up["vector_measurement"] = horse.vector_down["vector_measurement"]
            if horse_hit_circle == True:
                horse.vector_up["vector_measurement"] = random.randint(1, 6)
                horse.fit_movement_vectors()
            horse.vector_down["vector_measurement"] = 0

        elif direction == "LEFT":
            horse.location_x += 8 * horse.speed
            horse.vector_right["vector_measurement"] = horse.vector_left["vector_measurement"]
            if horse_hit_circle == True:
                horse.vector_right["vector_measurement"] = random.randint(1, 6)
                horse.fit_movement_vectors()
            horse.vector_left["vector_measurement"] = 0
            
        elif direction == "RIGHT":
            horse.location_x -= 8 * horse.speed
            horse.vector_left["vector_measurement"] = horse.vector_right["vector_measurement"]
            if horse_hit_circle == True:
                horse.vector_left["vector_measurement"] = random.randint(1, 6)
                horse.fit_movement_vectors()
            horse.vector_right["vector_measurement"] = 0
        
    return horse_hit_wall

def handle_horse_collision(horse, horses, direction, knife):
    other_horses = horses

    for other_horse in other_horses:
        if horse.name != other_horse.name:
            horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
            other_horse_rect = pygame.Rect(other_horse.location_x, other_horse.location_y, other_horse.width, other_horse.height)
            recoil_count = 1
            
            if horse_rect.colliderect(other_horse_rect):
                if horse.holding_knife == True:
                    other_horse.frames_since_last_stab = 0
                    recoil_count = 7
                    horse.holding_knife = False
                    other_horse.lives_remaining -= 1
                    knife["rect_value"][0] = other_horse.location_x
                    knife["rect_value"][1] = other_horse.location_y

                    if other_horse.lives_remaining < 1:
                        other_horse.width = 0
                        other_horse.height = 0   
                if other_horse.holding_knife == True: 
                    horse.frames_since_last_stab = 0 
                    recoil_count = 7
                    other_horse.holding_knife = False
                    horse.lives_remaining -= 1
                    knife["rect_value"][0] = horse.location_x
                    knife["rect_value"][1] = horse.location_y

                    if horse.lives_remaining < 1:
                        horse.width = 0
                        horse.height = 0    
                        
                if direction == "UP":
                    horse.location_y += 7 * recoil_count
                    horse.vector_down["vector_measurement"] = horse.vector_up["vector_measurement"]
                    horse.vector_up["vector_measurement"] = 0
                    
                    other_horse.location_y -=  7 * recoil_count
                    if other_horse.vector_down["vector_measurement"] != 0:
                        other_horse.vector_up["vector_measurement"] = other_horse.vector_down["vector_measurement"]
                        other_horse.vector_down["vector_measurement"] = 0
                        
                elif direction == "DOWN":
                    horse.location_y -= 7 * recoil_count
                    horse.vector_up["vector_measurement"] = horse.vector_down["vector_measurement"]
                    horse.vector_down["vector_measurement"] = 0
                    
                    other_horse.location_y += 7 * recoil_count
                    if other_horse.vector_up["vector_measurement"] != 0:
                        other_horse.vector_down["vector_measurement"] = other_horse.vector_up["vector_measurement"]
                        other_horse.vector_up["vector_measurement"] = 0

                elif direction == "LEFT":
                    horse.location_x += 7 * recoil_count
                    horse.vector_right["vector_measurement"] = horse.vector_left["vector_measurement"]
                    horse.vector_left["vector_measurement"] = 0
                    
                    other_horse.location_x -= 7 * recoil_count
                    if other_horse.vector_right["vector_measurement"] != 0:
                        other_horse.vector_left["vector_measurement"] = other_horse.vector_right["vector_measurement"]
                        other_horse.vector_right["vector_measurement"] = 0
                        
                elif direction == "RIGHT":
                    horse.location_x -= 7 * recoil_count
                    horse.vector_left["vector_measurement"] = horse.vector_right["vector_measurement"]
                    horse.vector_right["vector_measurement"] = 0
                    
                    other_horse.location_x += 7 * recoil_count
                    if other_horse.vector_left["vector_measurement"] != 0:
                        other_horse.vector_right["vector_measurement"] = other_horse.vector_left["vector_measurement"]
                        other_horse.vector_left["vector_measurement"] = 0
                    
                break

def get_horse_start_pos(horses, map):
    return 400, 400