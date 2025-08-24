import pygame, json, os, time
from horse_logic import Horse
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction
from map_logic import Map
from shape_logic import get_circle_hitboxes, get_line_hitboxes

pygame.init()

screen = pygame.display.set_mode((1470, 820))
pygame.display.set_caption('Python Honse Racing Simulator')
running = True

mover = {
    "type": "MOVING",
    "rect_value": [300, 50, 10, 100],
    "movement_direction": "VERTICAL", # or horizontal
    "max": 300,
    "min": 50,
    "animation_direction": "max", # or min, working towards the max value or the min value
    "distance_per_frame": 2
}
teleporter = {
    "type": "TELEPORT",
    "rect_value" : [0, 0, 0, 0],
    "teleport_id": 0,
    "pair_id": "A", # or b
    "teleport_sides": ["UP", "RIGHT"],
}

class Screen:
    def map_init(map_name):
        with open("maps.json") as file:
            maps_json = json.load(file)
        
        found = False
        for map in maps_json:
            if map["name"] == map_name:
                found = True
                name = map["name"]
                map_fields = map["map_fields"]
                special_rects = map["special_rects"]
                max_horses = map["max_horses"]
                wrap_after = map["wrap_after"]
                first_horse_start_pos = map["first_horse_start_pos"]
                background_color = map["background_color"]
                field_color = map["field_color"]
                this_is_a_wall = map["this_is_a_wall"]
                goal_x = map["goal_x"]
                goal_y = map["goal_y"]
                spacing = map["spacing"]
                
                return Map(name, map_fields, special_rects, max_horses, wrap_after,
                first_horse_start_pos, background_color, field_color, this_is_a_wall, goal_x, goal_y, spacing)
                
        if not found:
            return  Map("basic_ass_map", [pygame.Rect(50, 50, 670, 320), pygame.Rect(720, 300, 300, 200)], 
                        [mover], 6, 3, [100, 100], (30, 45, 70), (100, 150, 200), None, 1020, 750)
    
    def load_horse_objects(selected_horses, map):
        with open("horses.json") as file:
            horses_json = json.load(file)
        
        horse_objects = []
        for horse in horses_json:
            if horse["name"] in selected_horses:
                name = horse["name"]
                speed = horse["speed"]
                width = horse["width"]
                height = horse["height"]
                location_x = None
                location_y = None
                image_url = horse["image_url"]
                win_image_url = horse["win_image_url"]
                horse_objects.append(Horse(name, speed, width, height, location_x, location_y, image_url, win_image_url))
        
        unpacked_horses = map.get_horses_start_pos(horse_objects)
        
        return unpacked_horses
    
    def game(participating_horses, map_name):
        map = Screen.map_init(map_name)
        pygame.display.set_caption(f'Honse Racing Simulator: {map_name}')
        running = True
        game_done = False
        field_hitboxes = []
        horse_objects = Screen.load_horse_objects(participating_horses, map)
        goal = pygame.Rect(map.goal_x, map.goal_y, 20, 20)
        counter_1 = 0
        
        for map_rect in map.map_fields:
            field_hitboxes.append(map_rect)
            
        while running:
            clock = pygame.time.Clock()
            clock.tick(24)
            screen.fill(map.background_color) 
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                    
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for special_rect in map.special_rects:
                special_rect_color = map.background_color
                if special_rect["type"] != "WALL":
                    special_rect_color = map.get_special_rect_color(special_rect["type"])
                if special_rect["shape"] == "RECT":
                    srv = special_rect["rect_value"] # shorthand purposes
            
                    if special_rect["type"] == "MOVING":
                        map.move_moving_wall(special_rect)
                        pygame.draw.rect(screen, special_rect_color, (srv[0], srv[1], srv[2], srv[3]))
                    else:
                        pygame.draw.rect(screen, special_rect_color, (srv[0] - 20, srv[1] - 20, srv[2] + 40, srv[3] + 40))
                
                elif special_rect["shape"] == "CIRCLE":
                    pygame.draw.circle(screen, special_rect_color, special_rect["center"], special_rect["radius"])
                    if special_rect["radius"] != special_rect["base_radius"]:
                        special_rect["radius"] -= 1
                
            file_path = os.path.join("images", "carrot.png")
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (20, 20))
            screen.blit(scaled_image, (map.goal_x, map.goal_y)) 
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            if game_done == True:
                if counter_1 == 0:
                    time.sleep(4)
                    counter_1 += 1
                win_file_path = os.path.join("images", winning_horse.win_image_url)
                win_image = pygame.image.load(win_file_path)
                win_scaled_image = pygame.transform.scale(win_image, (1470, 820))
                screen.blit(win_scaled_image, (0, 0))
                
            if game_done == False:
                for horse in horse_objects:
                    if isinstance(horse, Horse):
                        horse.horse_move(field_hitboxes, horse_objects, map)
                        horse.fix_vector_pair("horizontal", horse.vector_left["vector_measurement"], horse.vector_right["vector_measurement"])
                        horse.fix_vector_pair("vertical", horse.vector_up["vector_measurement"], horse.vector_down["vector_measurement"])
                    
                        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(goal):
                            game_done = True
                            if horse.vector_up["vector_measurement"] != 0: 
                                horse.location_y -= 10
                            if horse.vector_down["vector_measurement"] != 0: 
                                horse.location_y += 10    
                            if horse.vector_right["vector_measurement"] != 0: 
                                horse.location_x += 10 
                            if horse.vector_left["vector_measurement"] != 0: 
                                horse.location_x -= 10     
                            winning_horse = horse   
            
            pygame.display.update()
            
            
participating_horses = ["John Horse", "Aquamarine Gambit", "Jovial Merryment", "Slow 'n' Steady", "Hopeless Endeavor", "Maiden O'Luck", "The Sweetest Treat", "Cherry Jubilee", "Ellsee Reins"]
Screen.game(participating_horses, "Teleporting Mess")