import pygame, random 
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
        horizontal_direction = random.choice(horizontal_directions)
        
        self.directions = [vertical_direction, horizontal_direction]
        
        self.vectors = [self.vector_left, self.vector_right, self.vector_up, self.vector_down]
        
        for vector in self.vectors:
            if vector["vector_name"] in self.directions:
                vector = random.randint(1, 6) * self.speed
        
    def movement_steps(self, walls, horses, direction):
        handle_wall_collision(self, walls, direction)
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
        
    def horse_move(self, walls, horses, carrot):
        for i in range(self.vector_left):
            self.location_x -= 1
            self.movement_steps(self, walls, horses, "LEFT")
        for i in range(self.vector_right):
            self.locationx += 1
            self.movement_steps(self, walls, horses, "RIGHT")
        for i in range(self.vector_down):
            self.locationy -= 1
            self.movement_steps(self, walls, horses, "DOWN")
        for i in range(self.vector_up):
            self.locationy += 1
            self.movement_steps(self, walls, horses, "UP")
            
        if pygame.Rect(self.rect).colliderect(carrot):
            print(f"WINNER: {self.name}")
            quit()