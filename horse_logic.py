import pygame, random 
from collision_logic import handle_horse_collision, handle_wall_collision

class Horse:
    def __init__(self, speed, width, height, location_x, location_y, image_url):
        self.name = self
        self.speed = speed
        self.width = width
        self.height = height
        self.image_url = image_url
        self.location_x = location_x
        self.location_y = location_y
        
        self.vector_up = 0
        self.vector_down = 0
        self.vector_left = 0
        self.vector_right = 0
        
        vertical_directions = ["UP", "DOWN"]
        horizontal_directions = ["LEFT", "RIGHT"] 
        
        vertical_direction = random.choice(vertical_directions)
        horizontal_direction = random.choice(horizontal_directions)
        
        self.directions = [vertical_direction, horizontal_direction]
        
        if vertical_direction == "UP":
            self.vector_up = self.speed * random.randint(1, 6)
        else:
            self.vector_down = self.speed * random.randint(1, 6)
            
        if horizontal_direction == "DOWN":
            self.vector_left = self.speed * random.randint(1, 6)
        else:
            self.vector_right = self.speed * random.randint(1, 6)
            
    def horse_move(self, walls, horses, carrot):
        for i in range(self.vector_left):
            self.location_x -= 1
            handle_wall_collision(self, walls)
            handle_horse_collision(self, horses)
        for i in range(self.vector_right):
            self.locationx += 1
            handle_wall_collision(self, walls)
            handle_horse_collision(self, horses)
        for i in range(self.vector_down):
            self.locationy -= 1
            handle_wall_collision(self, walls)
            handle_horse_collision(self, horses)
        for i in range(self.vector_up):
            self.locationy += 1
            handle_wall_collision(self, walls)
            handle_horse_collision(self, horses)