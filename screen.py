import pygame, json, os, time, math, random
from horse_logic import Horse
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction
from map_logic import Map
from shape_logic import get_circle_hitboxes, get_line_hitboxes

pygame.init()

screen = pygame.display.set_mode((1470, 820))
max_fps = 1000
fps = max_fps

pygame.display.set_caption('Python Honse Racing Simulator')
running = True

class Screen:
    def move_starting_in_rect(start_rect):
        rect = start_rect["rect"]
        directions = start_rect["directions"]
        if "UP" in directions:
            rect[1] -= 5
        if "DOWN" in directions:
            rect[1] += 5
        if "LEFT" in directions: 
            rect[0] -= 5
        if "RIGHT" in directions:
            rect[0] += 5
        
        if rect[1] < 0:
            start_rect["directions"].remove("UP")
            start_rect["directions"].append("DOWN")
        elif rect[1] > 620:
            start_rect["directions"].remove("DOWN")
            start_rect["directions"].append("UP")
        
        if rect[0] < 0:
            start_rect["directions"].remove("LEFT")
            start_rect["directions"].append("RIGHT")
        elif rect[0] > 1070:
            start_rect["directions"].remove("RIGHT")
            start_rect["directions"].append("LEFT")
        
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
                circle_fields = map["circle_fields"]
                
                return Map(name, map_fields, special_rects, max_horses, wrap_after,
                first_horse_start_pos, background_color, field_color, this_is_a_wall, goal_x, goal_y, spacing, circle_fields)
                
        if not found:
            return  Map("basic_ass_map", [pygame.Rect(50, 50, 670, 320), pygame.Rect(720, 300, 300, 200)], 
                        [], 6, 3, [100, 100], (30, 45, 70), (100, 150, 200), None, 1020, 750, 50)
    
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
        all_horse_objects = Screen.load_horse_objects(participating_horses, map)
        horse_objects = all_horse_objects[:(map.max_horses)]
        goal = pygame.Rect(map.goal_x, map.goal_y, 20, 20)
        counter_1 = 0
        game_start_time, current_time = time.time(), time.time()

        knife_mode = False
        knife = None
        for special_rect in map.special_rects:
            if special_rect["type"] == "KNIFE":
                knife = special_rect
                knife_mode = True
                break
        
        
        start_rect = {
            "rect": [random.randint(200, 1070), random.randint(200, 420), 400, 200],
            "directions": [random.choice(["UP", "DOWN"]), random.choice(["LEFT", "RIGHT"])]
        }
        
        for map_rect in map.map_fields:
            field_hitboxes.append(map_rect)

        while current_time - game_start_time < 10:
            clock = pygame.time.Clock()
            clock.tick(fps)
            current_time = time.time()
            events = pygame.event.get()
            screen.fill(map.background_color) 
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
            
            for special_rect in map.special_rects:
                special_rect_color = map.background_color
                if special_rect["type"] != "WALL":
                    special_rect_color = map.get_special_rect_color(special_rect["type"])
                if special_rect["type"] != "KNIFE":
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
            
            if knife_mode == True:
                knife_rect = knife["rect_value"]
                knife_file_path = os.path.join("images", "knife.png")
                knife_image = pygame.image.load(knife_file_path)
                scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                screen.blit(scaled_knife_image, (knife_rect[0], knife_rect[1]))
            
            pygame.draw.rect(screen, (0, 0, 0), map.this_is_a_wall)
            
            this_is_a_wall = pygame.Rect(map.this_is_a_wall[0],map.this_is_a_wall[1],map.this_is_a_wall[2],map.this_is_a_wall[3])
            
            axis = min(this_is_a_wall[2], this_is_a_wall[3])
            wall_font = pygame.font.SysFont(None, axis - 4, bold=True, italic=True)
            wall_text = wall_font.render("THIS IS A WALL", True, (255, 255, 255))
            
            if axis == this_is_a_wall[2]:
                sideways_wall_text = pygame.transform.rotate(wall_text, 90)
                wall_surface = sideways_wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(sideways_wall_text, wall_surface)
            else:
                wall_surface = wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(wall_text, wall_surface)
            
            start_rect_value = pygame.Rect(start_rect["rect"][0], start_rect["rect"][1], start_rect["rect"][2], start_rect["rect"][3])
            pygame.draw.rect(screen, (220, 0, 0), (start_rect["rect"][0]-10, start_rect["rect"][1]-10, start_rect["rect"][2]+20, start_rect["rect"][3]+20))
            pygame.draw.rect(screen, (255, 10, 10), start_rect_value)
            
            start_font = pygame.font.SysFont(None, 80, bold=True, italic=True)
            start_text_1 = start_font.render("STARTING IN", True, (255, 255, 255))
            start_text_2 = start_font.render(f"{math.ceil(10 - (current_time - game_start_time))} SECONDS...", True, (255, 255, 255))
            start_surface_1 = start_text_1.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery-40)
            start_surface_2 = start_text_2.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery+40)
            screen.blit(start_text_1, start_surface_1)
            screen.blit(start_text_2, start_surface_2)
            Screen.move_starting_in_rect(start_rect)
            
            pygame.display.update()
        
        while running:
            clock = pygame.time.Clock()
            clock.tick(max_fps)
            screen.fill(map.background_color) 
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                    
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
                
            for special_rect in map.special_rects:
                special_rect_color = map.background_color
                if knife_mode == False:
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
            
            if knife_mode == True:
                knife_rect = knife["rect_value"]
                knife_file_path = os.path.join("images", "knife.png")
                knife_image = pygame.image.load(knife_file_path)
                scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                screen.blit(scaled_knife_image, (knife_rect[0], knife_rect[1]))
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    if knife_mode == True:
                        horse.frames_since_last_stab += 0.5 # i want to half speed it but im too lazy to figure that out
                        if horse.frames_since_last_stab < 25:
                            hit_file_path = os.path.join("images", horse.win_image_url)
                            hit_image = pygame.image.load(hit_file_path)
                            hit_image.set_alpha(255*((24-horse.frames_since_last_stab)/24))
                            hit_scaled_image = pygame.transform.scale(hit_image, (1470, 820))
                            tint_hit_image = hit_scaled_image.copy()
                            tint_color = (120, 10, 15)
                            tint_hit_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
                            screen.blit(tint_hit_image, (0, 0))
                    
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    
                    if horse.holding_knife == True:
                        knife_rect = knife["rect_value"]
                        knife_file_path = os.path.join("images", "knife.png")
                        knife_image = pygame.image.load(knife_file_path)
                        scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                        screen.blit(scaled_knife_image, (horse.location_x+10, horse.location_y+10))
                    
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
                horses_remaining = 0
                for horse in horse_objects:
                    if horse.width > 0:
                        horses_remaining += 1
                if horses_remaining == 1:
                    game_done = True
                    for horse in horse_objects:
                        if horse.width > 0:
                            winning_horse = horse
                for horse in horse_objects:
                    if isinstance(horse, Horse):
                        if knife_mode == True:
                            if len(horse_objects) == 1:
                                game_done = True
                                winning_horse = horse_objects[0]
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
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
                        
                        if knife_mode == True:
                            knife_rect = knife["rect_value"]
                            if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(knife_rect):
                                horse.holding_knife = True
                                knife["rect_value"][0] = 10000
            
            pygame.display.update()
    
    def honseday_the_thirteenth(participating_horses, map_name):
        map = Screen.map_init(map_name)
        pygame.display.set_caption(f'Honse Racing Simulator: {map_name}')
        running = True
        game_done = False
        field_hitboxes = []
        all_horse_objects = Screen.load_horse_objects(participating_horses, map)
        horse_objects = all_horse_objects[:(map.max_horses)]
        goal = pygame.Rect(map.goal_x, map.goal_y, 20, 20)
        counter_1 = 0
        counter_2 = 0
        counter_3 = 0
        knife = pygame.Rect(0, 0, 0, 0)
        
        hopeless_endeavor = Horse("Hopeless Endeavor", 0.5, 40, 40, 800, 100, "hopeless_endeavor.png", "hopeless_endeavor.win.png")
        
        game_start_time, current_time = time.time(), time.time()
        current_time += 0
        frames_since_game_start = 0
        
        start_rect = {
            "rect": [random.randint(200, 1070), random.randint(200, 420), 400, 200],
            "directions": [random.choice(["UP", "DOWN"]), random.choice(["LEFT", "RIGHT"])]
        }
        
        for map_rect in map.map_fields:
            field_hitboxes.append(map_rect)

        while current_time - game_start_time < 10:
            clock = pygame.time.Clock()
            clock.tick(max_fps)
            fps = max_fps
            current_time = time.time()
            events = pygame.event.get()
            screen.fill(map.background_color) 
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
            
            for special_rect in map.special_rects:
                special_rect_color = map.background_color
                if special_rect["type"] != "WALL":
                    special_rect_color = map.get_special_rect_color(special_rect["type"])
                if special_rect["type"] != "KNIFE":
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
                    
                    heart_x = horse.location_x
                    heart_y = horse.location_y
                    hearts_drawn = 0
                    
                    for i in range(int(horse.lives_remaining)):
                        pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                        hearts_drawn += 1
                    
                    for i in range(3 - hearts_drawn):
                        pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                    
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
                        
            file_path = os.path.join("images", hopeless_endeavor.image_url)
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (hopeless_endeavor.width, hopeless_endeavor.height))
            screen.blit(scaled_image, (hopeless_endeavor.location_x, hopeless_endeavor.location_y))
            
            knife_file_path = os.path.join("images", "knife.png")
            knife_image = pygame.image.load(knife_file_path)
            scaled_knife_image = pygame.transform.scale(knife_image, (30, 30))
            screen.blit(scaled_knife_image, (hopeless_endeavor.location_x + 20, hopeless_endeavor.location_y + 10))
            
            pygame.draw.rect(screen, (0, 0, 0), map.this_is_a_wall)
            
            this_is_a_wall = pygame.Rect(map.this_is_a_wall[0],map.this_is_a_wall[1],map.this_is_a_wall[2],map.this_is_a_wall[3])
            
            axis = min(this_is_a_wall[2], this_is_a_wall[3])
            wall_font = pygame.font.SysFont(None, axis - 4, bold=True, italic=True)
            wall_text = wall_font.render("THIS IS A WALL", True, (255, 255, 255))
            
            if axis == this_is_a_wall[2]:
                sideways_wall_text = pygame.transform.rotate(wall_text, 90)
                wall_surface = sideways_wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(sideways_wall_text, wall_surface)
            else:
                wall_surface = wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(wall_text, wall_surface)
            
            start_rect_value = pygame.Rect(start_rect["rect"][0], start_rect["rect"][1], start_rect["rect"][2], start_rect["rect"][3])
            pygame.draw.rect(screen, (220, 0, 0), (start_rect["rect"][0]-10, start_rect["rect"][1]-10, start_rect["rect"][2]+20, start_rect["rect"][3]+20))
            pygame.draw.rect(screen, (255, 10, 10), start_rect_value)
            
            start_font = pygame.font.SysFont(None, 80, bold=True, italic=True)
            start_text_1 = start_font.render("STARTING IN", True, (255, 255, 255))
            start_text_2 = start_font.render(f"{math.ceil(10 - (current_time - game_start_time))} SECONDS...", True, (255, 255, 255))
            start_surface_1 = start_text_1.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery-40)
            start_surface_2 = start_text_2.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery+40)
            screen.blit(start_text_1, start_surface_1)
            screen.blit(start_text_2, start_surface_2)
            Screen.move_starting_in_rect(start_rect)
            
            pygame.display.update()
            
            
        while running:
            frames_since_game_start += 1
            
            alive_horses = 0
            for horse in horse_objects:
                if horse.width != 0:
                    alive_horses+=1
            
            if alive_horses == 1 and counter_2 == 0:
                if counter_3 < 1:
                    for horse in horse_objects:
                        horse.speed /= 4
                        horse.fit_movement_vectors()
                    hopeless_endeavor.speed /= 4
                    hopeless_endeavor.fit_movement_vectors()
                
                counter_3 += 1    
                if counter_3 == 72:
                    for horse in horse_objects:
                        horse.speed *= 4
                        horse.fit_movement_vectors()
                    hopeless_endeavor.speed *= 4
                    hopeless_endeavor.fit_movement_vectors()
                    map.background_color = (80, 00, 00)
                    map.field_color = (30, 0, 0)
                    counter_2 += 1
                    counter_3 += 1
        
            if frames_since_game_start % 3660 == 0:
                hopeless_endeavor.speed *= 2
                hopeless_endeavor.vector_left["vector_measurement"] *= 2
                hopeless_endeavor.vector_right["vector_measurement"] *= 2
                hopeless_endeavor.vector_up["vector_measurement"] *= 2
                hopeless_endeavor.vector_down["vector_measurement"] *= 2
            
            clock = pygame.time.Clock()
            clock.tick(fps)
            screen.fill(map.background_color) 
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                    
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
                
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
                    
                    heart_x = horse.location_x
                    heart_y = horse.location_y
                    hearts_drawn = 0
                    
                    for i in range(int(horse.lives_remaining)):
                        pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                        hearts_drawn += 1
                    
                    if horse.width != 0:
                        for i in range(3 - hearts_drawn):
                            pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                            heart_x += 10
                        
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            file_path = os.path.join("images", hopeless_endeavor.image_url)
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (hopeless_endeavor.width, hopeless_endeavor.height))
            tinted_image = scaled_image.copy()
            tint_color = (160, 12, 20)
            tinted_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
            if frames_since_game_start < 3600:
                used_image = scaled_image
            else:
                used_image = tinted_image
            screen.blit(used_image, (hopeless_endeavor.location_x, hopeless_endeavor.location_y))
            
            knife_file_path = os.path.join("images", "knife.png")
            knife_image = pygame.image.load(knife_file_path)
            scaled_knife_image = pygame.transform.scale(knife_image, (30, 30))
            screen.blit(scaled_knife_image, (hopeless_endeavor.location_x + 20, hopeless_endeavor.location_y + 10))
            
            if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(hopeless_endeavor.location_x, 
                                    hopeless_endeavor.location_y, hopeless_endeavor.width, hopeless_endeavor.height)):
                
                hopeless_endeavor.location_x, hopeless_endeavor.location_y = 40, 40
            
            hopeless_endeavor.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields, True)
            hopeless_endeavor.fix_vector_pair("horizontal", hopeless_endeavor.vector_left["vector_measurement"], hopeless_endeavor.vector_right["vector_measurement"])
            hopeless_endeavor.fix_vector_pair("vertical", hopeless_endeavor.vector_up["vector_measurement"], hopeless_endeavor.vector_down["vector_measurement"])         
            
            alive_horses = 0
            for horse in horse_objects:
                if horse.width != 0:
                    alive_horses += 1
            
            if alive_horses == 0:
                game_done = True
                winning_horse = hopeless_endeavor
            
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
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
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
                        
                        horse.frames_since_last_stab += 0.5 # i want to half speed it but im too lazy to figure that out
                        if horse.frames_since_last_stab < 25:
                            hit_file_path = os.path.join("images", horse.win_image_url)
                            hit_image = pygame.image.load(hit_file_path)
                            hit_image.set_alpha(255*((24-horse.frames_since_last_stab)/24))
                            hit_scaled_image = pygame.transform.scale(hit_image, (1470, 820))
                            tint_hit_image = hit_scaled_image.copy()
                            tint_color = (120, 10, 15)
                            tint_hit_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
                            screen.blit(tint_hit_image, (0, 0))
                        
                        if horse.frames_since_last_stab == 24:
                            horse.vector_left["vector_measurement"] *= 4
                            horse.vector_right["vector_measurement"] *= 4
                            horse.vector_up["vector_measurement"] *= 4
                            horse.vector_down["vector_measurement"] *= 4
                        
                        
            
            pygame.display.update()