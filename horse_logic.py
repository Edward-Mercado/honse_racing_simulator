import pygame, random, math
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction

class Horse:
    def __init__(self, name, speed, width, height, location_x, location_y, image_url):
        self.name = name
        self.speed = speed
        self.width = width
        self.height = height
        self.image_url = image_url
        self.location_x = location_x
        self.location_y = location_y
        self.rect = (location_x, location_y, width, height)
        
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
            
        self.fit_movement_vectors()
      
    def fit_movement_vectors(self):
        ratio_total = 10
        
        vector_measurements = [self.vector_down["vector_measurement"], 
                        self.vector_left["vector_measurement"], 
                        self.vector_right["vector_measurement"], 
                        self.vector_up["vector_measurement"]]
        
        vector_sum = sum(vector_measurements)
        
        proportion = ratio_total / vector_sum
        
        self.vector_down["vector_measurement"] *= proportion
        self.vector_down["vector_measurement"] *= self.speed
        self.vector_left["vector_measurement"] *= proportion
        self.vector_left["vector_measurement"] *= self.speed
        self.vector_right["vector_measurement"] *= proportion
        self.vector_right["vector_measurement"] *= self.speed
        self.vector_up["vector_measurement"] *= proportion
        self.vector_up["vector_measurement"] *= self.speed
      
    def movement_steps(self, field_hitboxes, horses, direction):
        global horse_hit_wall
        horse_hit_wall = handle_wall_collision(self, field_hitboxes, direction)
        handle_horse_collision(self, horses, direction)
        
    def swap_horse_vectors(horse, direction):
        opposite_direction = get_opposite_direction(direction)
        
        if opposite_direction == "UP":
            horse.vector_up = horse.vector_down
            horse.vector_down = 0
        elif opposite_direction == "DOWN":
            horse.vector_down = horse.vector_up
            horse.vector_up = 0
        
        elif opposite_direction == "LEFT":
            horse.vector_left = horse.vector_right
            horse.vector_right = 0
        elif opposite_direction == "RIGHT":
            horse.vector_right = horse.vector_left
            horse.vector_left = 0
        
    def horse_move(self, field_hitboxes, horses, carrot):
        try:
            if horse_hit_wall == "yo wsg brother":
                horse_hit_wall = True
        except UnboundLocalError:
            horse_hit_wall = True
        
        for i in range(math.ceil(self.vector_left["vector_measurement"])):
            self.location_x -= 1
            self.movement_steps(field_hitboxes, horses, "LEFT")
            if horse_hit_wall == False:
                break
        if horse_hit_wall == True:
            self.location_x -= (self.vector_left["vector_measurement"] - int(self.vector_left["vector_measurement"]))
            
        for i in range(math.ceil(self.vector_right["vector_measurement"])):
            self.location_x += 1
            self.movement_steps(field_hitboxes, horses, "RIGHT")   
            if horse_hit_wall == False:
                break
        if horse_hit_wall == True:
            self.location_x += (self.vector_right["vector_measurement"] - int(self.vector_right["vector_measurement"]))
        
        for i in range(math.ceil(self.vector_down["vector_measurement"])):
            self.location_y += 1
            self.movement_steps(field_hitboxes, horses, "DOWN")
            if horse_hit_wall == False:
                break
        if horse_hit_wall == True:
            self.location_y += (self.vector_down["vector_measurement"] - int(self.vector_down["vector_measurement"]))   
        
        for i in range(math.ceil(self.vector_up["vector_measurement"])):
            self.location_y -= 1
            self.movement_steps(field_hitboxes, horses, "UP")
            if horse_hit_wall == False:
                break
        if horse_hit_wall == True:
            self.location_y -= (self.vector_up["vector_measurement"] - int(self.vector_up["vector_measurement"]))
        
        if pygame.Rect(self.rect).colliderect(carrot):
            print(f"WINNER: {self.name}")
            quit()
            
    def get_vector_movement(self, vector_name):
        vector_movements = {
            "RIGHT" : ["X", 1],
            "LEFT" : ["X", -1],
            "UP": ["Y", -1],
            "DOWN": ["Y", 1]
        }
        return vector_movements[vector_name]
    
    def fix_vector_pair(self, type, vector_one, vector_two):
        if sum([vector_one, vector_two]) == 0:
            if type == "horizontal":
                self.vector_left["vector_measurement"] = random.randint(1, 5)
                self.fit_movement_vectors()
            elif type == "vertical":
                self.vector_up["vector_measurement"] = random.randint(1, 5)
                self.fit_movement_vectors()