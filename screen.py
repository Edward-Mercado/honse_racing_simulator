import pygame, json, os, time, math, random
from horse_logic import Horse
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction
from map_logic import Map
from shape_logic import get_circle_hitboxes, get_line_hitboxes

pygame.init()

screen = pygame.display.set_mode((1470, 820))
max_fps = 48
fps = max_fps

pygame.display.set_caption('Python Honse Racing Simulator')
running = True

class Screen:
    def move_starting_in_rect(start_rect): # this allows the rectangle that says "GAME STARTS IN..." to move across the screen
        rect = start_rect["rect"] # this takes the rect_value tuple and allows us to change its location 
        directions = start_rect["directions"] # the directions the rect is currently moving
        if "UP" in directions:
            rect[1] -= 5 # move y up 5 pixels
        if "DOWN" in directions:
            rect[1] += 5 # move y down 5 pixels
        if "LEFT" in directions: 
            rect[0] -= 5 # move x left 5 pixels
        if "RIGHT" in directions:
            rect[0] += 5 # move x right 5 pixels
        
        if rect[1] < 0: # if we are at the top of the screen, swap up command for down
            start_rect["directions"].remove("UP") 
            start_rect["directions"].append("DOWN")
        elif rect[1] > 620: # if we are at the bottom, swap down command for up
            start_rect["directions"].remove("DOWN")
            start_rect["directions"].append("UP")
        
        if rect[0] < 0: # if we are on the left, swap left for right
            start_rect["directions"].remove("LEFT")
            start_rect["directions"].append("RIGHT")
        elif rect[0] > 1070: # if we are on the right, swap right for left
            start_rect["directions"].remove("RIGHT")
            start_rect["directions"].append("LEFT")
        
    def map_init(map_name): # pulls the json data for the map given the map's name
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
                # initialize a map object based off the json dictionary
                return Map(name, map_fields, special_rects, max_horses, wrap_after,
                first_horse_start_pos, background_color, field_color, this_is_a_wall, goal_x, goal_y, spacing, circle_fields)
                
        if not found: # if we cant find it in the json datafile then load a very basic indev map 
            return  Map("basic_ass_map", [pygame.Rect(50, 50, 670, 320), pygame.Rect(720, 300, 300, 200)], 
                        [], 6, 3, [100, 100], (30, 45, 70), (100, 150, 200), None, 1020, 750, 50)
    
    def load_horse_objects(selected_horses, map): # pulls the json data for the horses given the horses we want
        with open("horses.json") as file:
            horses_json = json.load(file)
        
        horse_objects = [] # we currently have 0 horses
        for horse in horses_json: # loop through the list
            if horse["name"] in selected_horses: # if we find a horse the player selected
                name = horse["name"]
                speed = horse["speed"]
                width = horse["width"]
                height = horse["height"]
                location_x = None
                location_y = None
                image_url = horse["image_url"]
                win_image_url = horse["win_image_url"]
                win_song_url = horse["win_song_url"]
                # initalize the horse and append it to our horse_objects list
                horse_objects.append(Horse(name, speed, width, height, location_x, location_y, image_url, win_image_url, win_song_url))
        
        # this will give all the horse objects starting positions 
        # the map object has variables that can dictate how each horse will load in
        unpacked_horses = map.get_horses_start_pos(horse_objects)
        
        return unpacked_horses
    
    def game(participating_horses, map_name):
        map = Screen.map_init(map_name)
        pygame.display.set_caption(f'Honse Racing Simulator: {map_name}')
        running = True
        game_done = False
        field_hitboxes = []
        all_horse_objects = Screen.load_horse_objects(participating_horses, map) # loads the horse names into horse objects
        horse_objects = all_horse_objects[:(map.max_horses)] # cuts off the excess horses (if for some reason the user loads too many)
        goal = pygame.Rect(map.goal_x, map.goal_y, 20, 20) # initializes the goal as a Rect object
        counter_1 = 0 # this counter will increment by one, so the time delay after a horse hits the carrot
        # only happens once
        # this is for the starting cutscene so the horses move after 10 seconds
        counter_10 = 0
        game_start_time, current_time = time.time(), time.time()

        # this is for knife battlegrounds
        knife_mode = False
        knife = None
        for special_rect in map.special_rects:
            if special_rect["type"] == "KNIFE": # if there is a knife then it will set the gamemode to knife
                knife = special_rect
                knife_mode = True
                break
        ###
        
        # initializes the start rect as a dictionary, whose location is random and whose directions are also random
        start_rect = {
            "rect": [random.randint(200, 1070), random.randint(200, 420), 400, 200],
            "directions": [random.choice(["UP", "DOWN"]), random.choice(["LEFT", "RIGHT"])]
        }
        
        
        for map_rect in map.map_fields: # allows us to load and check for just the field_hitboxes
            field_hitboxes.append(map_rect)

        while current_time - game_start_time < 10:
            clock = pygame.time.Clock() 
            clock.tick(fps) # sets the max fps of the game to the variable at the top
            current_time = time.time() # changes current time variable every frame
            events = pygame.event.get()
            screen.fill(map.background_color) 
            
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            for hitbox in field_hitboxes: # draw all the fields for the horses 
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for hitbox in map.circle_hitboxes: # for circular fields this will add the hitboxes onto the space
                pygame.draw.rect(screen, map.field_color, hitbox)
            
            for special_rect in map.special_rects: # this will load the map features with properties (wall, killbrick, bounce, etc.)
                special_rect_color = map.background_color # if it doesnt have a special color (like wall) then it wil be the bg color
                if special_rect["type"] != "WALL":
                    special_rect_color = map.get_special_rect_color(special_rect["type"]) # this will return a special color
                if special_rect["type"] != "KNIFE": # if the type isnt knife (which is drawn differently)
                    if special_rect["shape"] == "RECT": # draws it if its a rect
                        srv = special_rect["rect_value"] # shorthand purposes
                
                        if special_rect["type"] == "MOVING": # moving walls have different collision factors so they are drawn differently
                            map.move_moving_wall(special_rect)
                            pygame.draw.rect(screen, special_rect_color, (srv[0], srv[1], srv[2], srv[3]))
                        else:
                            pygame.draw.rect(screen, special_rect_color, (srv[0] - 20, srv[1] - 20, srv[2] + 40, srv[3] + 40))
                    
                    elif special_rect["shape"] == "CIRCLE":
                        pygame.draw.circle(screen, special_rect_color, special_rect["center"], special_rect["radius"])
                        if special_rect["radius"] != special_rect["base_radius"]:
                            special_rect["radius"] -= 1
            
            # draws carrot
            file_path = os.path.join("images", "carrot.png")
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (20, 20))
            screen.blit(scaled_image, (map.goal_x, map.goal_y)) 
            
            # draws horses
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    # this will draw the hearts for the life bar
                    heart_x = horse.location_x
                    heart_y = horse.location_y
                    
                    # for the amount of lives we have, draw red circles
                    for i in range(int(horse.lives_remaining)):
                        pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10 # move us over
                        
                    
                    # for the amount of lives we dont have draw black circles
                    for i in range(3 - horse.lives_remaining):
                        pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                        
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    
                    # if the horse is not on screen it will reset the horse location to the map's starting position
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            # draws the knife
            if knife_mode == True:
                knife_rect = knife["rect_value"]
                knife_file_path = os.path.join("images", "knife.png")
                knife_image = pygame.image.load(knife_file_path)
                scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                screen.blit(scaled_knife_image, (knife_rect[0], knife_rect[1]))
            
            # draws the "THIS IS A WALL"
            pygame.draw.rect(screen, (0, 0, 0), map.this_is_a_wall)
            
            this_is_a_wall = pygame.Rect(map.this_is_a_wall[0],map.this_is_a_wall[1],map.this_is_a_wall[2],map.this_is_a_wall[3])
            
            
            axis = min(this_is_a_wall[2], this_is_a_wall[3])
            wall_font = pygame.font.SysFont(None, axis - 4, bold=True, italic=True)
            wall_text = wall_font.render("THIS IS A WALL", True, (255, 255, 255))
            
            if axis == this_is_a_wall[2]: # this conditional decides whether the wall is vertical or horizontal
            # if the wall is vertical the text on the wall is drawn on its side
                sideways_wall_text = pygame.transform.rotate(wall_text, 90)
                wall_surface = sideways_wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(sideways_wall_text, wall_surface)
            else:
                wall_surface = wall_text.get_rect(center=this_is_a_wall.center)
                screen.blit(wall_text, wall_surface)
            
            # define the starting rect as a rect object
            start_rect_value = pygame.Rect(start_rect["rect"][0], start_rect["rect"][1], start_rect["rect"][2], start_rect["rect"][3])
            
            # the border is slightly up and left and is slightly bigger so it goes around it
            pygame.draw.rect(screen, (220, 0, 0), (start_rect["rect"][0]-10, start_rect["rect"][1]-10, start_rect["rect"][2]+20, start_rect["rect"][3]+20))
            
            # draw the rect
            pygame.draw.rect(screen, (255, 10, 10), start_rect_value)
            
            # this draws all the text for both lines 
            start_font = pygame.font.SysFont(None, 80, bold=True, italic=True)
            start_text_1 = start_font.render("STARTING IN", True, (255, 255, 255))
            start_text_2 = start_font.render(f"{math.ceil(10 - (current_time - game_start_time))} SECONDS...", True, (255, 255, 255))
            start_surface_1 = start_text_1.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery-40)
            start_surface_2 = start_text_2.get_rect(centerx=start_rect_value.centerx, centery=start_rect_value.centery+40)
            screen.blit(start_text_1, start_surface_1)
            screen.blit(start_text_2, start_surface_2)
            Screen.move_starting_in_rect(start_rect)
            
            pygame.display.update()
        
        while running: # most comments here will be similar to/short versions of the starting while loop comments
            # set max_fps
            clock = pygame.time.Clock()
            clock.tick(max_fps)
            screen.fill(map.background_color) 
            knife_can_pick_up = True
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            # draws the various hitboxes for the field        
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
            
            for horse in horse_objects:
                if horse.frames_since_last_stab <= 72:
                    knife_can_pick_up = False
                
            # draws all the special rects
            for special_rect in map.special_rects:
                special_rect_color = map.background_color
                if knife_mode == False: # if there are no knives
                    if special_rect["type"] != "WALL": 
                        special_rect_color = map.get_special_rect_color(special_rect["type"])
                    if special_rect["shape"] == "RECT":
                        srv = special_rect["rect_value"] # shorthand purposes (short for special rect value)
                
                        if special_rect["type"] == "MOVING": # moving rects are drawn differently
                            map.move_moving_wall(special_rect)
                            pygame.draw.rect(screen, special_rect_color, (srv[0], srv[1], srv[2], srv[3]))
                        else:
                            pygame.draw.rect(screen, special_rect_color, (srv[0] - 20, srv[1] - 20, srv[2] + 40, srv[3] + 40))
                    
                    elif special_rect["shape"] == "CIRCLE": # if the shpae is a circle just draw the circle instead
                        pygame.draw.circle(screen, special_rect_color, special_rect["center"], special_rect["radius"])
                        if special_rect["radius"] != special_rect["base_radius"]:
                            # some instances (like teleport or bounce collision) have a small animation to which the 
                            # circle appears to grow, this is to animate it returning back to normal
                            special_rect["radius"] -= 1
                else:
                    if special_rect["type"] != "KNIFE":
                        if special_rect["type"] != "WALL": 
                            special_rect_color = map.get_special_rect_color(special_rect["type"])
                        if special_rect["shape"] == "RECT":
                            srv = special_rect["rect_value"] # shorthand purposes (short for special rect value)
                            
                            if special_rect["type"] == "MOVING": # moving rects are drawn differently
                                map.move_moving_wall(special_rect)
                                pygame.draw.rect(screen, special_rect_color, (srv[0], srv[1], srv[2], srv[3]))
                            else:
                                pygame.draw.rect(screen, special_rect_color, (srv[0] - 20, srv[1] - 20, srv[2] + 40, srv[3] + 40))
                        
                        elif special_rect["shape"] == "CIRCLE": # if the shpae is a circle just draw the circle instead
                            pygame.draw.circle(screen, special_rect_color, special_rect["center"], special_rect["radius"])
                            if special_rect["radius"] != special_rect["base_radius"]:
                                # some instances (like teleport or bounce collision) have a small animation to which the 
                                # circle appears to grow, this is to animate it returning back to normal
                                special_rect["radius"] -= 1
            
            # draws carrot
            file_path = os.path.join("images", "carrot.png")
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (20, 20))
            screen.blit(scaled_image, (map.goal_x, map.goal_y)) 
            
            for horse in horse_objects:
                if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(pygame.Rect(map.goal_x, map.goal_y, 20, 20)):
                    game_done = True
                    winning_horse = horse
                    for horse in horse_objects:
                        horse.base_speed /= 10
                        horse.speed /= 10
                        horse.fit_movement_vectors()
            
            # this is to make the game more interesting if there are two horses left:
            if knife_mode == True:
                alive_horses = 0
                horses_critical_health = 0
                for horse in horse_objects:
                    if horse.width > 0:
                        alive_horses += 1
            
                        if horse.lives_remaining < 2:
                            horses_critical_health += 1
                
                if alive_horses == 2 and counter_10 == 0 and horses_critical_health > 0:
                    counter_10 += 1
                    map.background_color = (80, 0, 0)
                    map.field_color = (30, 0, 0)
                    
                    map.goal_x = 1400
                    map.goal_y = 410
                    
            ###    
            
            # if there is a knife, blit the knife image to the screen
            if knife_mode == True:                   
                knife_rect = knife["rect_value"]
                knife_file_path = os.path.join("images", "knife.png")
                knife_image = pygame.image.load(knife_file_path)
                scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                screen.blit(scaled_knife_image, (knife_rect[0], knife_rect[1]))
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    if knife_mode == True: # if there are knives
                        # this will draw the hearts for the life bar
                        if horse.speed < 0.1:
                            horse.speed = horse.base_speed
                            horse.fit_movement_vectors()
                        if horse.width != 0:
                            heart_x = horse.location_x
                            heart_y = horse.location_y
                            
                            # for the amount of lives we have, draw red circles
                            for i in range(int(horse.lives_remaining)):
                                pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                                heart_x += 10 # move us over
                                
                            
                            # for the amount of lives we dont have draw black circles
                            for i in range(3 - horse.lives_remaining):
                                pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                                heart_x += 10
                                
                        horse.frames_since_last_stab += 0.5 # i want to half speed this animation but im too lazy to fix this function
                        if horse.frames_since_last_stab < 25: # if its been less than one game second (24 frames) since the horse got stabbed
                            # get the image for the hit (which is the same as its winning image)
                            hit_file_path = os.path.join("images", horse.win_image_url) 
                            hit_image = pygame.image.load(hit_file_path)
                            hit_image.set_alpha(255*((24-horse.frames_since_last_stab)/24))
                            hit_scaled_image = pygame.transform.scale(hit_image, (1470, 820))
                            
                            # tint the image red and blit it to the screen
                            tint_hit_image = hit_scaled_image.copy()
                            tint_color = (120, 10, 15)
                            tint_hit_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
                            screen.blit(tint_hit_image, (0, 0))
                    
                    # get the image for the horse and blit it
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    
                    # if the horse is holding the knife then blit a knife image in the lower right of the screen
                    if horse.holding_knife == True:
                        knife_rect = knife["rect_value"]
                        knife_file_path = os.path.join("images", "knife.png")
                        knife_image = pygame.image.load(knife_file_path)
                        scaled_knife_image = pygame.transform.scale(knife_image, (knife_rect[2], knife_rect[3]))
                        screen.blit(scaled_knife_image, (horse.location_x+10, horse.location_y+10))
                    
                    # this will bring the horse back to the game if it is off the screen
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            if game_done == True: # if a horse hits the food then the game is done
                if counter_1 == 0: 
                    for horse in horse_objects:
                        horse.speed /= 1000
                        horse.fit_movement_vectors()
                    
                counter_1 += 1 # this will ensure the slow down only occurs once
                if counter_1 <= 48: # for the first two in game seconds move at very slow speed
                    for horse in horse_objects:
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
                if counter_1 > 48: # then blit the winning image
                    win_file_path = os.path.join("images", winning_horse.win_image_url)
                    win_image = pygame.image.load(win_file_path)
                    win_scaled_image = pygame.transform.scale(win_image, (1470, 820))
                    screen.blit(win_scaled_image, (0, 0))
            
            if game_done == False: # if the game isnt done 
                # knife mode stuff
                horses_remaining = 0
                for horse in horse_objects:
                    if horse.width > 0: # dead horses arent removed and just have a width of 0 to prevent bugs
                        horses_remaining += 1 # this will test of the horse is dead or not
                if horses_remaining == 1: # if only one horse remains, the game is done and the last one standing is the winner
                    game_done = True
                    for horse in horse_objects: 
                        if horse.width > 0:
                            winning_horse = horse
                # ---
                
                for horse in horse_objects: # this will move the horses
                    if isinstance(horse, Horse):
                        # move horse function, then it will fix the vectors if randomly both opposing pairs get set to 0
                        if horse.frames_since_last_stab > 96:
                            horse.speed = horse.base_speed
                            horse.fit_movement_vectors()
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
                        horse.fix_vector_pair("horizontal", horse.vector_left["vector_measurement"], horse.vector_right["vector_measurement"])
                        horse.fix_vector_pair("vertical", horse.vector_up["vector_measurement"], horse.vector_down["vector_measurement"])         
                        
                        # if a horse hits the goal then they win yay
                        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(goal):
                            game_done = True
                            
                            # this moves the winning horse closer to the goal
                            if horse.vector_up["vector_measurement"] != 0: 
                                horse.location_y -= 10
                            if horse.vector_down["vector_measurement"] != 0: 
                                horse.location_y += 10    
                            if horse.vector_right["vector_measurement"] != 0: 
                                horse.location_x += 10 
                            if horse.vector_left["vector_measurement"] != 0: 
                                horse.location_x -= 10     
                            winning_horse = horse   
                        
                        # for knife mode
                        if knife_mode == True:
                            knife_rect = knife["rect_value"]
                            # if a horse touches the knife it picks it up and the knife gets sent over yonder (so no one can pick it up in the meantime)
                            if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(knife_rect) and knife_can_pick_up == True:
                                horse.holding_knife = True
                                knife["rect_value"][0] = 100000
                        #
            
            pygame.display.update()
    
    def honseday_the_thirteenth(participating_horses, map_name): # a lot of copied code from regular game but yk
        # same assigning variables
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
        
        # load hopeless endeavor as his own horse
        hopeless_endeavor = Horse("Hopeless Endeavor", 0.5, 40, 40, 800, 100, "hopeless_endeavor.png", "hopeless_endeavor.win.png", "")
        
        game_start_time, current_time = time.time(), time.time()
        current_time += 0
        
        # variable name self explanatory, this will increment to trigger different game phases
        frames_since_game_start = 0
        
        # same starting rect assignment
        start_rect = {
            "rect": [random.randint(200, 1070), random.randint(200, 420), 400, 200],
            "directions": [random.choice(["UP", "DOWN"]), random.choice(["LEFT", "RIGHT"])]
        }
        
        # load field hitboxes
        for map_rect in map.map_fields:
            field_hitboxes.append(map_rect)

        # starting phase
        while current_time - game_start_time < 10:
            # fps setting
            clock = pygame.time.Clock()
            clock.tick(max_fps)
            fps = max_fps
            
            current_time = time.time()
            events = pygame.event.get()
            screen.fill(map.background_color) 
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            # draw hitboxes
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
            
            
            # draw special rects
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
            
            # draw the carrot
            file_path = os.path.join("images", "carrot.png")
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (20, 20))
            screen.blit(scaled_image, (map.goal_x, map.goal_y)) 
            
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    # draw the horses
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    
                    # this will draw the hearts for the life bar
                    heart_x = horse.location_x
                    heart_y = horse.location_y
                    
                    # for the amount of lives we have, draw red circles
                    for i in range(int(horse.lives_remaining)):
                        pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10 # move us over
                        
                    
                    # for the amount of lives we dont have draw black circles
                    for i in range(3 - horse.lives_remaining):
                        pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                    
                    # if we arent on the field then bring us back yo
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            # draw hopeless            
            file_path = os.path.join("images", hopeless_endeavor.image_url)
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (hopeless_endeavor.width, hopeless_endeavor.height))
            screen.blit(scaled_image, (hopeless_endeavor.location_x, hopeless_endeavor.location_y))
            
            # draw his knife
            knife_file_path = os.path.join("images", "knife.png")
            knife_image = pygame.image.load(knife_file_path)
            scaled_knife_image = pygame.transform.scale(knife_image, (30, 30))
            screen.blit(scaled_knife_image, (hopeless_endeavor.location_x + 20, hopeless_endeavor.location_y + 10))
            
            # draw the wall
            pygame.draw.rect(screen, (0, 0, 0), map.this_is_a_wall)
            
            this_is_a_wall = pygame.Rect(map.this_is_a_wall[0],map.this_is_a_wall[1],map.this_is_a_wall[2],map.this_is_a_wall[3])
            
            # logically figure out whether to rotate the text
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
            
            # draw the starting rect and its border
            start_rect_value = pygame.Rect(start_rect["rect"][0], start_rect["rect"][1], start_rect["rect"][2], start_rect["rect"][3])
            pygame.draw.rect(screen, (220, 0, 0), (start_rect["rect"][0]-10, start_rect["rect"][1]-10, start_rect["rect"][2]+20, start_rect["rect"][3]+20))
            pygame.draw.rect(screen, (255, 10, 10), start_rect_value)
            
            # draw the text on the border
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
            # this will increment the frame counter
            frames_since_game_start += 1
            
            # this will get the amount of alive horses
            alive_horses = 0
            for horse in horse_objects:
                if horse.width != 0:
                    alive_horses+=1
            
            # if only one horse is alive this will trigger stress mode (field is red now)
            if alive_horses == 1 and counter_2 == 0:
                if counter_3 < 1:
                    # slow everyone down for the slo mo shot
                    for horse in horse_objects:
                        horse.speed /= 4
                        horse.fit_movement_vectors()
                    hopeless_endeavor.speed /= 4
                    hopeless_endeavor.fit_movement_vectors()
                
                counter_3 += 1  # so the above conditional only occurs once
                if counter_3 == 72:
                    # speed everyone back up to normal
                    for horse in horse_objects:
                        horse.speed *= 4
                        horse.fit_movement_vectors()
                    hopeless_endeavor.speed *= 4
                    hopeless_endeavor.fit_movement_vectors()
                    
                    # change colors to red
                    map.background_color = (80, 00, 00)
                    map.field_color = (30, 0, 0)
                    
                    # to terminate this loop
                    counter_2 += 1
                    counter_3 += 1

            # if a frame minute has passed (the modulo function returns the remainder when the dividend is divided by the divisor)
            # so every 3660 frames this will occur
            if frames_since_game_start % 3660 == 0:
                # double hopeless' speed
                hopeless_endeavor.speed *= 2
                hopeless_endeavor.fit_movement_vectors()
            
            # set max fps
            clock = pygame.time.Clock()
            clock.tick(fps)
            screen.fill(map.background_color) 
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                  
            # draw hitboxes  
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, map.field_color, (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            for hitbox in map.circle_hitboxes:
                pygame.draw.rect(screen, map.field_color, hitbox)
              
            # draw special_rects  
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

            # draw carrot
            file_path = os.path.join("images", "carrot.png")
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (20, 20))
            screen.blit(scaled_image, (map.goal_x, map.goal_y)) 
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    # draw horses
                    file_path = os.path.join("images", horse.image_url)
                    image = pygame.image.load(file_path)
                    scaled_image = pygame.transform.scale(image, (horse.width, horse.height))
                    screen.blit(scaled_image, (horse.location_x, horse.location_y)) 
                    
                    # draw the hearts
                    heart_x = horse.location_x
                    heart_y = horse.location_y
                    
                    for i in range(int(horse.lives_remaining)):
                        pygame.draw.circle(screen, (255, 0, 0), (heart_x, heart_y), 5)
                        heart_x += 10
                    
                    if horse.width != 0:
                        for i in range(3 - horse.lives_remaining):
                            pygame.draw.circle(screen, (0, 0, 0), (heart_x, heart_y), 5)
                            heart_x += 10
                    
                    # bring horse back to the field
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse = map.get_single_start_pos(horse)
            
            # draw hopeless endeavor
            file_path = os.path.join("images", hopeless_endeavor.image_url)
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (hopeless_endeavor.width, hopeless_endeavor.height))
            
            # tints hopeless' sprite red
            tinted_image = scaled_image.copy()
            tint_color = (160, 12, 20)
            tinted_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
            
            # if its been more than a frame minute, then use red hopeless
            if frames_since_game_start < 3600:
                used_image = scaled_image
            else:
                used_image = tinted_image
            
            screen.blit(used_image, (hopeless_endeavor.location_x, hopeless_endeavor.location_y))
            
            # draw hopeless' knife
            knife_file_path = os.path.join("images", "knife.png")
            knife_image = pygame.image.load(knife_file_path)
            scaled_knife_image = pygame.transform.scale(knife_image, (30, 30))
            screen.blit(scaled_knife_image, (hopeless_endeavor.location_x + 20, hopeless_endeavor.location_y + 10))
            
            # if hopeless is not on screen then bring him back
            if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(hopeless_endeavor.location_x, 
                                    hopeless_endeavor.location_y, hopeless_endeavor.width, hopeless_endeavor.height)):
                
                hopeless_endeavor.location_x, hopeless_endeavor.location_y = 40, 40
            
            # move hopeless and fix his vectors
            hopeless_endeavor.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields, True)
            hopeless_endeavor.fix_vector_pair("horizontal", hopeless_endeavor.vector_left["vector_measurement"], hopeless_endeavor.vector_right["vector_measurement"])
            hopeless_endeavor.fix_vector_pair("vertical", hopeless_endeavor.vector_up["vector_measurement"], hopeless_endeavor.vector_down["vector_measurement"])         
            
            # test if there are enough alive horses
            alive_horses = 0
            for horse in horse_objects:
                if horse.width != 0:
                    alive_horses += 1
            
            # if there arent then hopeless wins
            if alive_horses == 0:
                game_done = True
                winning_horse = hopeless_endeavor
            
            # if the game is done
            if game_done == True:
                if counter_1 == 0: 
                    # slow everyone down for slow mo
                    for horse in horse_objects:
                        horse.speed /= 1000
                        horse.fit_movement_vectors()
                    hopeless_endeavor.speed /= 1000
                    hopeless_endeavor.fit_movement_vectors()
                counter_1 += 1 # this will ensure the slow down only occurs once
                
                # for two frame seconds
                if counter_1 <= 48:
                    for horse in horse_objects:
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
                
                # after two frame seconds then draw the winning horse
                if counter_1 > 48:
                    win_file_path = os.path.join("images", winning_horse.win_image_url)
                    win_image = pygame.image.load(win_file_path)
                    win_scaled_image = pygame.transform.scale(win_image, (1470, 820))
                    screen.blit(win_scaled_image, (0, 0))
            
            
            if game_done == False:
                for horse in horse_objects:
                    if isinstance(horse, Horse): # move the horses and fix the vectors
                        horse.horse_move(field_hitboxes, horse_objects, map, knife, map.circle_fields)
                        horse.fix_vector_pair("horizontal", horse.vector_left["vector_measurement"], horse.vector_right["vector_measurement"])
                        horse.fix_vector_pair("vertical", horse.vector_up["vector_measurement"], horse.vector_down["vector_measurement"])         
                        
                        # if a horse touches the goal then that horse wins and the game is done
                        if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(goal):
                            game_done = True
                            
                            # move the horse closer to the goal
                            if horse.vector_up["vector_measurement"] != 0: 
                                horse.location_y -= 10
                            if horse.vector_down["vector_measurement"] != 0: 
                                horse.location_y += 10    
                            if horse.vector_right["vector_measurement"] != 0: 
                                horse.location_x += 10 
                            if horse.vector_left["vector_measurement"] != 0: 
                                horse.location_x -= 10     
                            winning_horse = horse
                        
                        horse.frames_since_last_stab += 0.5 # i want to half speed the timer but im too lazy to fix this function
                        # if a horse is recently stabbed 
                        if horse.frames_since_last_stab < 25:
                            # use a red version of their win image and flash it on screen
                            hit_file_path = os.path.join("images", horse.win_image_url)
                            hit_image = pygame.image.load(hit_file_path)
                            hit_image.set_alpha(255*((24-horse.frames_since_last_stab)/24))
                            hit_scaled_image = pygame.transform.scale(hit_image, (1470, 820))
                            tint_hit_image = hit_scaled_image.copy()
                            tint_color = (120, 10, 15)
                            tint_hit_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
                            screen.blit(tint_hit_image, (0, 0))
                        
                        # a horse's speed is divided by 4 when stabbed so after a frame second then it will go back to normal
                        if horse.frames_since_last_stab == 24:
                            horse.speed *= 4
                            horse.fit_movement_vectors()
                        
                        
            
            pygame.display.update()