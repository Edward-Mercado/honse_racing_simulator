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
    horse_hit_hitbox = False
    
    for field_hitbox in field_hitboxes:
        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(field_hitbox):
            horse_hit_hitbox = True  
            
    if horse_hit_hitbox == False:
        horse.past_directions.append(direction)
        
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
        
    return horse_hit_hitbox

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