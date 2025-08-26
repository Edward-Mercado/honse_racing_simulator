import pygame, random
from shape_logic import get_circle_hitboxes, get_line_hitboxes

class Map:
    def __init__(self, name, map_fields, special_rects, max_horses, 
                wrap_after, first_horse_starting_pos, background_color, field_color, 
                this_is_a_wall, goal_x, goal_y, spacing, circle_fields):
        
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
        self.circle_fields = circle_fields
        self.circle_hitboxes = []
        
        # get the circle hitboxes
        for circle_field in self.circle_fields:
            circle_hitboxes = get_circle_hitboxes((circle_field[0], circle_field[1]), circle_field[2])
            
            for circle_hitbox in circle_hitboxes:
                self.circle_hitboxes.append(circle_hitbox)

    def get_horses_start_pos(self, horses): # this will give all the horses starting positions based on the map
        x_start_pos, y_start_pos = self.first_horse_starting_pos[0], self.first_horse_starting_pos[1]
        horse_count = 0
        
        for horse in horses:
            # assign the horse locations to the starting positions
            horse.location_x, horse.location_y = x_start_pos, y_start_pos
            horse_count += 1
            
            x_start_pos += self.spacing
            if horse_count % self.wrap_after == 0: # if we are at the end of a row go to the next row and start again
                y_start_pos += self.spacing
                x_start_pos -= (self.spacing*self.wrap_after)
           
            if horse_count == self.max_horses: # if we put too many horses break the loop
                break
            
        for horse in horses: # and after the loop is broken the unassigned horses are eliminated
            if horse.location_x == None:
                horses.remove(horse)
                
        return horses
    
    def get_special_rect_color(self, special_rect_type): # returns the color based on the type of the special_rect
        color_values = {
            "KILLBRICK": (255, 0, 0),
            "BOUNCE": (0, 255, 0),
            "TELEPORT" : (0, 255, 255),
            "MOVING": (70, 70, 70),
            "KNIFE": (20, 20, 20) # we never call the knife but this was for development to get a blank gray square
        }
        return color_values[special_rect_type]
    
    def get_single_start_pos(self, horse): # to get a single horses start position, get a random number from the first row and place him there
        spawn_number = random.randint(1, self.wrap_after)
        horse.location_x, horse.location_y = self.first_horse_starting_pos[0] + spawn_number*self.spacing, self.first_horse_starting_pos[1]
        return horse
    
    def handle_special_collision(self, horse, direction): # this will route a collision to a special point to a different function
        for special_rect in self.special_rects:
            if special_rect["type"] != "KNIFE": # checking the knife is a different function entirely
                if special_rect["shape"] == "RECT":
                    special_rect_value = pygame.Rect(special_rect["rect_value"][0], special_rect["rect_value"][1], special_rect["rect_value"][2], special_rect["rect_value"][3])
                    horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
                    if special_rect_value.colliderect(horse_rect):
                        rect_type = special_rect["type"]
                        # routing
                        if rect_type == "KILLBRICK":
                            self.collide_killbrick(horse)
                        elif rect_type == "BOUNCE":
                            self.collide_bounce_pad(horse, direction, special_rect)
                        elif rect_type == "TELEPORT":
                            self.collide_teleporter(horse, special_rect)
                        elif rect_type == "MOVING":
                            self.collide_moving_wall(horse, direction)
                        elif rect_type == "WALL":
                            self.collide_moving_wall(horse, direction) # i am not making two functions that do the same thing
                
                elif special_rect["shape"] == "CIRCLE":
                    # another use of the circle hitboxes funciton
                    circle_hitboxes = get_circle_hitboxes(special_rect["center"], special_rect["base_radius"])
                    horse_rect = pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)
                    for circle_hitbox in circle_hitboxes: # if we hit any hitbox then do the collision function
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

    def collide_moving_wall(self, horse, direction): # standard wall collision function
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
    
    def collide_killbrick(self, horse): # returns the horse to its starting position
        self.get_single_start_pos(horse)
        return horse
    
    def collide_bounce_pad(self, horse, direction, special_rect):
        if special_rect["shape"] == "CIRCLE": # if the shape is a circle increase the radius and it will slowly shrink
            special_rect["radius"] += 5
            if special_rect["radius"] > (special_rect["base_radius"] + 10):
                special_rect["radius"] = (special_rect["base_radius"] + 10)
        horse.turns_until_speed = 10 # speeds up the horses so it takes two actioins
        
        # standard collision function
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
    
    def get_paired_teleporter(self, teleporter): # determines which teleporter is paired with the one the horse collided with
        # teleport id is the id of the teleporter pair (so the first pair is 0, second pair is 1, etc.)
        # the pair id is which teleporter it is, so one pair will have teleporter A and teleporter B
        # this is so that the paired teleporter doesnt return the same value as the input teleporter
        for special_rect in self.special_rects:
            if special_rect["type"] == "TELEPORT":
                if special_rect["teleport_id"] == teleporter["teleport_id"] and special_rect["pair_id"] != teleporter["pair_id"]:
                    return special_rect
        
        return "ERROR" # this will never happen as my code doesnt bug but yk
            
    def collide_teleporter(self, horse, teleporter):
        paired_teleporter = self.get_paired_teleporter(teleporter)
        
        if paired_teleporter != "ERROR": # this will never happen because i wrote perfect code yk
            if paired_teleporter["shape"] == "RECT":
                horse.location_x = paired_teleporter["rect_value"][0]
                horse.location_y = paired_teleporter["rect_value"][1]
                
                # the teleporters have sides and it will spawn you on that side so that a horse going up into a teleporter wont immediately
                # go back the way it went, for general purposes
                if "UP" in paired_teleporter["teleport_sides"]:
                    horse.vector_down["vector_measurement"] = 0
                    horse.vector_up["vector_measurement"] = random.randint(1, 6)
                    horse.location_y = paired_teleporter["rect_value"][1] - (horse.height)
                if "DOWN" in paired_teleporter["teleport_sides"]:
                    horse.vector_up["vector_measurement"] = 0
                    horse.vector_down["vector_measurement"] = random.randint(1, 6)
                    horse.location_y =( paired_teleporter["rect_value"][1] + paired_teleporter["rect_value"][3])
                
                if "LEFT" in paired_teleporter["teleport_sides"]:
                    horse.vector_right["vector_measurement"] = 0
                    horse.vector_left["vector_measurement"] = random.randint(1, 6)
                    horse.location_x = paired_teleporter["rect_value"][0] - (horse.height)
                if "RIGHT" in paired_teleporter["teleport_sides"]:
                    horse.vector_left["vector_measurement"] = 0
                    horse.vector_right["vector_measurement"] = random.randint(1, 6)
                    horse.location_x =( paired_teleporter["rect_value"][0] + paired_teleporter["rect_value"][2])
            
            if paired_teleporter["shape"] == "CIRCLE":

                # if the teleporter is a circle then the animation will be similar to the bounce pad animation
                teleporter["radius"] += 5
                if teleporter["radius"] > (teleporter["base_radius"] + 10):
                    teleporter["radius"] = (teleporter["base_radius"] + 10)
                    
                paired_teleporter["radius"] += 5
                if paired_teleporter["radius"] > (teleporter["base_radius"] + 10):
                    paired_teleporter["radius"] = (teleporter["base_radius"] + 10)
                
                horse.location_x = paired_teleporter["center"][0]
                horse.location_y = paired_teleporter["center"][1]
                
                # same sort of distance calculation as the rect teleporter one
                if "UP" in paired_teleporter["teleport_sides"]:
                    horse.vector_down["vector_measurement"] = 0
                    horse.vector_up["vector_measurement"] = random.randint(1, 6)
                    horse.location_y = (paired_teleporter["center"][1] - paired_teleporter["radius"]) - (horse.height)
                    
                if "DOWN" in paired_teleporter["teleport_sides"]:
                    horse.vector_up["vector_measurement"] = 0
                    horse.vector_down["vector_measurement"] = random.randint(1, 6)
                    horse.location_y =( paired_teleporter["center"][1] + paired_teleporter["radius"])
                
                if "LEFT" in paired_teleporter["teleport_sides"]:
                    horse.vector_right["vector_measurement"] = 0
                    horse.vector_left["vector_measurement"] = random.randint(1, 6)
                    horse.location_x = (paired_teleporter["center"][0] - paired_teleporter["radius"]) - (horse.height)
                    
                if "RIGHT" in paired_teleporter["teleport_sides"]:
                    horse.vector_left["vector_measurement"] = 0
                    horse.vector_right["vector_measurement"] = random.randint(1, 6)
                    horse.location_x =( paired_teleporter["center"][0] + paired_teleporter["radius"])
                    
            horse.fit_movement_vectors()
    
    def move_moving_wall(self, moving_wall):
        # each frame the moving wall will move
        # there are two directions for the moving wall, max and min
        # if it goes in the max direction the location will increase in value (so either going right or dowm)
        # if it goes in the min direction the location will decrease in value (so either going left or up)
        
        # if we are past the bounds of the moving wall's path limits then the direction will reverse
        
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