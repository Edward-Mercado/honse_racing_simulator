import pygame, random
from shape_logic import get_circle_hitboxes, get_line_hitboxes

class Map:
    def __init__(self, name, map_fields, special_rects, max_horses, 
                wrap_after, first_horse_starting_pos, background_color, field_color, 
                this_is_a_wall, goal_x, goal_y, spacing):
        
        self.name = name
        self.map_fields = map_fields
        self.special_rects = special_rects
        self.max_horses = max_horses
        self.wrap_after = wrap_after
        self.first_horse_starting_pos = first_horse_starting_pos
        self.background_color = background_color
        self.field_color = field_color
        self.this_is_a_wall = this_is_a_wall
        self.spacing = spacing
        self.goal_x = goal_x
        self.goal_y = goal_y
        
    def get_horses_start_pos(self, horses):
        x_start_pos, y_start_pos = self.first_horse_starting_pos[0], self.first_horse_starting_pos[1]
        horse_count = 0
        
        for horse in horses:
            horse.location_x, horse.location_y = x_start_pos, y_start_pos
            horse_count += 1
            
            x_start_pos += self.spacing
            if horse_count % self.wrap_after == 0:
                y_start_pos += self.spacing
                x_start_pos -= (self.spacing*self.wrap_after)
           
            if horse_count == self.max_horses:
                break
            
        for horse in horses:
            if horse.location_x == None:
                horses.remove(horse)
                
        return horses
    
    def get_special_rect_color(self, special_rect_type):
        color_values = {
            "KILLBRICK": (255, 0, 0),
            "BOUNCE": (0, 255, 0),
            "TELEPORT" : (0, 255, 255),
            "MOVING": (70, 70, 70),
        }
        return color_values[special_rect_type]
    
    def get_single_start_pos(self, horse):
        horse.location_x, horse.location_y = self.first_horse_starting_pos[0], self.first_horse_starting_pos[1]
        return horse
    
    def handle_special_collision(self, horse, direction):
        for special_rect in self.special_rects:
            if special_rect["shape"] == "RECT":
                special_rect_value = pygame.Rect(special_rect["rect_value"][0], special_rect["rect_value"][1], special_rect["rect_value"][2], special_rect["rect_value"][3])
                horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
                if special_rect_value.colliderect(horse_rect):
                    rect_type = special_rect["type"]
                    if rect_type == "KILLBRICK":
                        self.collide_killbrick(horse)
                    elif rect_type == "BOUNCE":
                        self.collide_bounce_pad(horse, direction)
                    elif rect_type == "TELEPORT":
                        self.collide_teleporter(horse, special_rect)
                    elif rect_type == "MOVING":
                        self.collide_moving_wall(horse, direction)
                    elif rect_type == "WALL":
                        self.collide_moving_wall(horse, direction) # i am not making two functions that do the same thing
            elif special_rect["shape"] == "CIRCLE":
                circle_hitboxes = get_circle_hitboxes(special_rect["center"], special_rect["base_radius"])
                horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
                for circle_hitbox in circle_hitboxes:
                    if circle_hitbox.colliderect(horse_rect):
                        rect_type = special_rect["type"]
                        if rect_type == "KILLBRICK":
                            self.collide_killbrick(horse)
                        elif rect_type == "BOUNCE":
                            self.collide_bounce_pad(horse, direction, special_rect)
                        elif rect_type == "TELEPORT":
                            self.collide_teleporter(horse, special_rect)
                        elif rect_type == "MOVING":
                            self.collide_moving_wall(horse, direction)
                        elif rect_type == "WALL":
                            self.collide_moving_wall(horse, direction)

    def collide_moving_wall(self, horse, direction):
        if direction == "UP":
            horse.location_y += 12 * horse.speed
            horse.vector_down["vector_measurement"] = horse.vector_up["vector_measurement"]
            horse.vector_up["vector_measurement"] = 0
            
        elif direction == "DOWN":
            horse.location_y -= 12 * horse.speed
            horse.vector_up["vector_measurement"] = horse.vector_down["vector_measurement"]
            horse.vector_down["vector_measurement"] = 0

        elif direction == "LEFT":
            horse.location_x += 12 * horse.speed
            horse.vector_right["vector_measurement"] = horse.vector_left["vector_measurement"]
            horse.vector_left["vector_measurement"] = 0
            
        elif direction == "RIGHT":
            horse.location_x -= 12 * horse.speed
            horse.vector_left["vector_measurement"] = horse.vector_right["vector_measurement"]
            horse.vector_right["vector_measurement"] = 0
    
    def collide_killbrick(self, horse):
        self.get_single_start_pos(horse)
        return horse
    
    def collide_bounce_pad(self, horse, direction, special_rect):
        if special_rect["shape"] == "CIRCLE":
            special_rect["radius"] += 5
            if special_rect["radius"] > 24:
                special_rect["radius"] = 25
        horse.turns_until_speed = 10
        if direction == "UP":
            horse.location_y += 7 * horse.speed
            horse.vector_down["vector_measurement"] = horse.vector_up["vector_measurement"]
            horse.vector_up["vector_measurement"] = 0
            
        elif direction == "DOWN":
            horse.location_y -= 7 * horse.speed
            horse.vector_up["vector_measurement"] = horse.vector_down["vector_measurement"]
            horse.vector_down["vector_measurement"] = 0

        elif direction == "LEFT":
            horse.location_x += 7 * horse.speed
            horse.vector_right["vector_measurement"] = horse.vector_left["vector_measurement"]
            horse.vector_left["vector_measurement"] = 0
            
        elif direction == "RIGHT":
            horse.location_x -= 7 * horse.speed
            horse.vector_left["vector_measurement"] = horse.vector_right["vector_measurement"]
            horse.vector_right["vector_measurement"] = 0
    
    def get_paired_teleporter(self, teleporter):
        for special_rect in self.special_rects:
            if special_rect["type"] == "TELEPORT":
                if special_rect["teleport_id"] == teleporter["teleport_id"] and special_rect["pair_id"] != teleporter["pair_id"]:
                    return special_rect
        
        return "ERROR"
            
    def collide_teleporter(self, horse, teleporter):
        paired_teleporter = self.get_paired_teleporter(teleporter)
        
        if paired_teleporter != "ERROR":
            if "UP" in paired_teleporter["teleport_sides"]:
                horse.vector_down["vector_measurement"] = 0
                horse.vector_up["vector_measurement"] = random.randint(1, 6)
                horse.location_y = paired_teleporter["rect_value"][1] - (horse.height + 5)
            if "DOWN" in paired_teleporter["teleport_sides"]:
                horse.vector_up["vector_measurement"] = 0
                horse.vector_down["vector_measurement"] = random.randint(1, 6)
                horse.location_y =( paired_teleporter["rect_value"][1] + paired_teleporter["rect_value"][3]) + 5
            
            if "LEFT" in paired_teleporter["teleport_sides"]:
                horse.vector_right["vector_measurement"] = 0
                horse.vector_left["vector_measurement"] = random.randint(1, 6)
                horse.location_x = paired_teleporter["rect_value"][0] - (horse.height + 5)
            if "RIGHT" in paired_teleporter["teleport_sides"]:
                horse.vector_left["vector_measurement"] = 0
                horse.vector_right["vector_measurement"] = random.randint(1, 6)
                horse.location_x =( paired_teleporter["rect_value"][0] + paired_teleporter["rect_value"][2]) + 5
            horse.fit_movement_vectors()
    
    def move_moving_wall(self, moving_wall):
        if moving_wall["movement_direction"] == "HORIZONTAL":
            
            if moving_wall["animation_direction"] == "max":
                moving_wall["rect_value"][0] += moving_wall["distance_per_frame"]
                
                if moving_wall["rect_value"][0] >= moving_wall["max"]:
                    moving_wall["animation_direction"] = "min"
            
            if moving_wall["animation_direction"] == "min":
                moving_wall["rect_value"][0] -= moving_wall["distance_per_frame"]
                
                if moving_wall["rect_value"][0] <= moving_wall["min"]:
                    moving_wall["animation_direction"] = "max"

        if moving_wall["movement_direction"] == "VERTICAL":
            
            if moving_wall["animation_direction"] == "max":
                moving_wall["rect_value"][1] += moving_wall["distance_per_frame"]
                
                if moving_wall["rect_value"][1] >= moving_wall["max"]:
                    moving_wall["animation_direction"] = "min"
            
            if moving_wall["animation_direction"] == "min":
                moving_wall["rect_value"][1] -= moving_wall["distance_per_frame"]
                
                if moving_wall["rect_value"][1] <= moving_wall["min"]:
                    moving_wall["animation_direction"] = "max"
        
standard_moving_id = {
    "type": "MOVING",
    "rect_value": [300, 50, 10, 30],
    "movement_direction": "VERTICAL", # or horizontal
    "max": 100,
    "min": 50,
    "animation_direction": "max", # or min, working towards the max value or the min value
    "distance_per_frame": 2
}