import pygame, random, math, json
from collision_logic import handle_horse_collision, handle_wall_collision

class Horse:
    def __init__(self, name, speed, width, height, location_x, location_y, image_url, win_image_url, win_song_url, grave_color):
        self.name = name
        self.speed = speed
        self.base_speed = speed
        self.turns_until_speed = 0
        self.width = width
        self.height = height
        self.image_url = image_url
        
        self.dead_x = 1000
        self.dead_y = 1000
        
        self.location_x = location_x
        self.location_y = location_y
        self.win_image_url = win_image_url
        self.win_song_url = win_song_url
        self.grave_color = grave_color
        
        self.consecutive_wall_hits = 0
        self.rect = (location_x, location_y, width, height)
        self.past_directions = []
        self.holding_knife = False
        self.lives_remaining = 1
        self.frames_since_last_stab = 24
        
        # i was going to originally have some function that returns the attribute based on vector name and then never did that
        self.vector_up = {
            "vector_name" : "UP",
            "vector_measurement" : 0    
        }
        self.vector_down = {
            "vector_name" : "DOWN",
            "vector_measurement" : 0    
        }
        self.vector_left = {
            "vector_name" : "LEFT",
            "vector_measurement" : 0    
        }
        self.vector_right = {
            "vector_name" : "RIGHT",
            "vector_measurement" : 0    
        }
        
        # these are to select random vectors when the game starts, and then assign them random values
        vertical_directions = ["UP", "DOWN"]
        horizontal_directions = ["LEFT", "RIGHT"] 
        
        vertical_direction = random.choice(vertical_directions)
        if vertical_direction == "UP":
            self.vector_up["vector_measurement"] = random.randint(1, 6)
        elif vertical_direction == "DOWN":
            self.vector_down["vector_measurement"] = random.randint(1, 6)
            
        horizontal_direction = random.choice(horizontal_directions)
        if horizontal_direction == "LEFT":
            self.vector_left["vector_measurement"] = random.randint(1, 6)
        elif horizontal_direction == "RIGHT":
            self.vector_right["vector_measurement"] = random.randint(1, 6)
        
        # this is to ensure the total distance a horse moves is the same for all horses of a given speed
        self.fit_movement_vectors()
      
    def fit_movement_vectors(self): # this is to ensure the total distance a horse moves is the same for all horses of a given speed
        ratio_total = 10 * self.speed # this is how much the total should be
        
        vector_measurements = [self.vector_down["vector_measurement"], 
                        self.vector_left["vector_measurement"], 
                        self.vector_right["vector_measurement"], 
                        self.vector_up["vector_measurement"]]
        
        # get the sum of the vectors
        vector_sum = sum(vector_measurements)
        
        try:
            # multiply each vector by the proportion and of they should be
            proportion = ratio_total / vector_sum
            self.vector_down["vector_measurement"] *= proportion
            self.vector_left["vector_measurement"] *= proportion
            self.vector_right["vector_measurement"] *= proportion
            self.vector_up["vector_measurement"] *= proportion
            
        except ZeroDivisionError:
            # if our vectors are messed up then reassign them to random values
            if random.choice(["UP", "DOWN"]) == "UP":
                self.vector_up["vector_measurement"] = random.randint(1, 6)
            else:
                self.vector_down["vector_measurement"] = random.randint(1, 6)
                
            if random.choice(["LEFT", "RIGHT"]) == "LEFT":
                self.vector_left["vector_measurement"] = random.randint(1, 6)
            else:
                self.vector_right["vector_measurement"] = random.randint(1, 6)
            
            vector_measurements = [self.vector_down["vector_measurement"], 
                        self.vector_left["vector_measurement"], 
                        self.vector_right["vector_measurement"], 
                        self.vector_up["vector_measurement"]]
            vector_sum = sum(vector_measurements)
            
            # same function as the try statement
            proportion = ratio_total / vector_sum
            self.vector_down["vector_measurement"] *= proportion
            self.vector_left["vector_measurement"] *= proportion
            self.vector_right["vector_measurement"] *= proportion
            self.vector_up["vector_measurement"] *= proportion
      
    def movement_steps(self, field_hitboxes, horses, direction, map, knife, circle_fields, honseday):
        global horse_hit_wall # i dont know why i put this here, but im afraid that the code may not work if i remove it so it stays
        
        # handle collisions
        horse_hit_wall = handle_wall_collision(self, field_hitboxes, direction, circle_fields)
        handle_horse_collision(self, horses, direction, knife, honseday)
        
        # handle the collision of special fields (moving walls, teleporters, bounce pads, etc.)
        map.handle_special_collision(self, direction)
        
    def horse_move(self, field_hitboxes, horses, map, knife, circle_fields, honseday = False):
        if self.consecutive_wall_hits > 1: # no cheating by clipping through the walls
            map.get_single_start_pos(self)
            self.consecutive_wall_hits = 0
        
        try: # sometimes horse_hit_wall gets assigned as some funky None value so i put this here to check
            if horse_hit_wall == "yo wsg brother":
                horse_hit_wall = True
        except UnboundLocalError:
            horse_hit_wall = True
        
        # for all of these
        # go one pixel for the amount of times the the vector measurement says
        # if we hit the wall, break the loop and increment the wall hits
        
        for i in range(math.ceil(self.vector_left["vector_measurement"])):
            self.location_x -= 1
            self.movement_steps(field_hitboxes, horses, "LEFT", map, knife, circle_fields, honseday)
            if horse_hit_wall == False:
                self.consecutive_wall_hits += 1
                break
        if horse_hit_wall == True:
            self.consecutive_wall_hits = 0
            self.location_x -= (self.vector_left["vector_measurement"] - int(self.vector_left["vector_measurement"]))
            
        for i in range(math.ceil(self.vector_right["vector_measurement"])):
            self.location_x += 1
            self.movement_steps(field_hitboxes, horses, "RIGHT", map, knife, circle_fields, honseday)   
            if horse_hit_wall == False:
                self.consecutive_wall_hits += 1
                break
        if horse_hit_wall == True:
            self.consecutive_wall_hits = 0
            self.location_x += (self.vector_right["vector_measurement"] - int(self.vector_right["vector_measurement"]))
        
        for i in range(math.ceil(self.vector_down["vector_measurement"])):
            self.location_y += 1
            self.movement_steps(field_hitboxes, horses, "DOWN", map, knife, circle_fields, honseday)
            if horse_hit_wall == False:
                self.consecutive_wall_hits += 1
                break
        if horse_hit_wall == True:
            self.consecutive_wall_hits = 0
            self.location_y += (self.vector_down["vector_measurement"] - int(self.vector_down["vector_measurement"]))   
        
        for i in range(math.ceil(self.vector_up["vector_measurement"])):
            self.location_y -= 1
            self.movement_steps(field_hitboxes, horses, "UP", map, knife, circle_fields, honseday)
            if horse_hit_wall == False:
                self.consecutive_wall_hits += 1
                break
        if horse_hit_wall == True:
            self.consecutive_wall_hits = 0
            self.location_y -= (self.vector_up["vector_measurement"] - int(self.vector_up["vector_measurement"]))
        
        
        # if we have a speed boost like after the bouncepad, then just move again
        if self.turns_until_speed != 0:            
            self.turns_until_speed -= 1
            for i in range(math.ceil(self.vector_left["vector_measurement"])):
                self.location_x -= 1
                self.movement_steps(field_hitboxes, horses, "LEFT", map, knife, circle_fields, honseday)
                if horse_hit_wall == False:
                    self.consecutive_wall_hits += 1
                    break
            if horse_hit_wall == True:
                self.consecutive_wall_hits = 0
                self.location_x -= (self.vector_left["vector_measurement"] - int(self.vector_left["vector_measurement"]))
                
            for i in range(math.ceil(self.vector_right["vector_measurement"])):
                self.location_x += 1
                self.movement_steps(field_hitboxes, horses, "RIGHT", map, knife, circle_fields, honseday)  
                if horse_hit_wall == False:
                    self.consecutive_wall_hits += 1
                    break
            if horse_hit_wall == True:
                self.consecutive_wall_hits = 0
                self.location_x += (self.vector_right["vector_measurement"] - int(self.vector_right["vector_measurement"]))
            
            for i in range(math.ceil(self.vector_down["vector_measurement"])):
                self.location_y += 1
                self.movement_steps(field_hitboxes, horses, "DOWN", map, knife, circle_fields, honseday)
                if horse_hit_wall == False:
                    self.consecutive_wall_hits += 1
                    break
            if horse_hit_wall == True:
                self.consecutive_wall_hits = 0
                self.location_y += (self.vector_down["vector_measurement"] - int(self.vector_down["vector_measurement"]))   
            
            for i in range(math.ceil(self.vector_up["vector_measurement"])):
                self.location_y -= 1
                self.movement_steps(field_hitboxes, horses, "UP", map, knife, circle_fields, honseday)
                if horse_hit_wall == False:
                    self.consecutive_wall_hits += 1
                    break
            if horse_hit_wall == True:
                self.consecutive_wall_hits = 0
                self.location_y -= (self.vector_up["vector_measurement"] - int(self.vector_up["vector_measurement"]))
    
    def fix_vector_pair(self, type, vector_one, vector_two):
        if sum([vector_one, vector_two]) == 0: # if both vectors equal zero, then get the past directions
            past_directions_reversed = self.past_directions[::-1]
        
            # we will loop through past directions to see if which vector comes first and then assign it to a random value
            # then fit it
            
            if type == "horizontal": 
                for previous_direction in past_directions_reversed:
                    if previous_direction == "LEFT":
                        self.vector_left["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                        break
                    elif previous_direction == "RIGHT":
                        self.vector_right["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                        break
                    
                if "LEFT" not in past_directions_reversed and "RIGHT" not in past_directions_reversed:
                    if random.choice(["LEFT, RIGHT"]) == "LEFT":
                        self.vector_left["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                    else:
                        self.vector_right["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                        
            elif type == "vertical":
                for previous_direction in past_directions_reversed:
                    if previous_direction == "UP":
                        self.vector_up["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                        break
                    elif previous_direction == "DOWN":
                        self.vector_down["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                        break
                    
                if "UP" not in past_directions_reversed and "DOWN" not in past_directions_reversed:
                    if random.choice(["UP", "DOWN"]) == "UP":
                        self.vector_up["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()
                    else:
                        self.vector_down["vector_measurement"] = random.randint(1, 5)
                        self.fit_movement_vectors()