import pygame, math, random

def get_opposite_direction(direction): # useless ass function that i think never gets called
    # this was one of the first functions i wrote for the game and i expected to use it a lot more
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

def get_corner_distance(corners, center): # gets the max distance from a horse corner to the center of a circle field
    distances = []
    for corner in corners:
        distance = int(math.sqrt((corner[0] - center[0])**2 + (corner[1] - center[1])**2))
        distances.append(distance)
    return max(distances)
    
def handle_wall_collision(horse, field_hitboxes, direction, circle_fields):
    horse_hit_hitbox = True
    horse_hit_circle = False
    
    # if a horse doesnt hit the hitbox then it hit a wall
    for field_hitbox in field_hitboxes:
        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(field_hitbox):
            horse_hit_hitbox = False
   
    for circle_field in circle_fields:
        # this will get the topleft, bottomleft, topright, and bottomright corners
        corner_TL = (horse.location_x, horse.location_y)
        corner_BL = (horse.location_x, horse.location_y+horse.height)
        corner_TR = (horse.location_x + horse.width, horse.location_y)
        corner_BR = (horse.location_x + horse.width, horse.location_y+horse.width)
        corners = [corner_TL, corner_BL, corner_BR, corner_TR]
        
        max_distance = get_corner_distance(corners, (circle_field[0], circle_field[1]))
        
        # if the max distance is greater than the radius the horse hit the wall
        if max_distance < circle_field[2]:
            horse_hit_hitbox = False
            # this is a distinction that needs to be made for later
            horse_hit_circle = True
            
    if horse_hit_hitbox == True:
        # past_directions is for a different debugging function
        horse.past_directions.append(direction)
        
        # for all of these:
        # if the horse was going some direction,
        # swap the direction for its opposite 
        # if the horse hit a circle, then randomize the direction so it doesnt get stuck
        # move the horse back a little bit
        
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
        
    return horse_hit_hitbox

def handle_horse_collision(horse, horses, direction, knife, honseday):
    other_horses = horses

    for other_horse in other_horses:
        if horse.name != other_horse.name: # if the horses arent the same
            horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
            other_horse_rect = pygame.Rect(other_horse.location_x, other_horse.location_y, other_horse.width, other_horse.height)
            recoil_count = 1
            
            if horse_rect.colliderect(other_horse_rect):
                # if one of the horses is holding a knife,
                # resets the frames since last stab, lower speed, disable knife holding, boost recoil count
                # if the horse dies then it's width and height are set to zero
                # recoil count multiplies the amount the horses are launced away post collision
                if horse.holding_knife == True or (honseday == True and horse.name == "Hopeless Endeavor"):
                    other_horse.frames_since_last_stab = 0
                    
                    other_horse.speed /= 4
                    other_horse.fit_movement_vectors()
                    
                    horse.holding_knife = False
                    other_horse.lives_remaining -= 1
                    
                    if horse.holding_knife == True:
                        knife["rect_value"][0] = other_horse.location_x
                        knife["rect_value"][1] = other_horse.location_y
                        recoil_count = 7
                    else:
                        recoil_count = 3
                    
                    if other_horse.lives_remaining < 1:
                        other_horse.width = 0
                        other_horse.height = 0   
                        
                if other_horse.holding_knife == True or (honseday == True and other_horse.name == "Hopeless Endeavor"): 
                    horse.frames_since_last_stab = 0 
                    other_horse.holding_knife = False
                    horse.lives_remaining -= 1
                    
                    horse.speed /= 4
                    horse.fit_movement_vectors()
                    
                    horse.vector_left["vector_measurement"] /= 4
                    horse.vector_right["vector_measurement"] /= 4
                    horse.vector_up["vector_measurement"] /= 4
                    horse.vector_down["vector_measurement"] /= 4
                    
                    if other_horse.holding_knife == True:
                        knife["rect_value"][0] = horse.location_x
                        knife["rect_value"][1] = horse.location_y
                        recoil_count = 7
                    else:
                        recoil_count = 3
                        
                    if horse.lives_remaining < 1:
                        horse.width = 0
                        horse.height = 0    
                
                # same collision logic as the walls except the other horse moves away    
                # if the horses were already going towards each other then both are flipped, if not then just the horse
                # whose turn it already is that gets flipped    
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