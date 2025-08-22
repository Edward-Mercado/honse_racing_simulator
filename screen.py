import pygame, json, time
from horse_logic import Horse
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction, get_horse_start_pos

pygame.init()

screen = pygame.display.set_mode((1470, 820))
pygame.display.set_caption('Python Honse Racing Simulator')
running = True


john_horse = Horse("John Horse", 1, 30, 30, 300, 300, (100, 80, 20))
aquamarine_gambit = Horse("Aquamarine Gambit", 1, 30, 30, 130, 130, (30, 200, 240))
jovial_merryment = Horse("Jovial Merryment", 1, 30, 30, 230, 230, (230, 120, 20))
cherry_jubilee = Horse("Cherry Jubilee", 1, 30, 30, 330, 330, (245, 10, 10))
the_sweetest_treat = Horse("The Sweetest Treat", 1, 30, 30, 400, 400, (245, 200, 210))
slow_n_steady = Horse("Slow 'N' Steady", 0.5, 30, 30, 400, 200, (20, 20, 60))
foggy_afterevening = Horse("Foggy Afterevening", 0.33, 30, 30, 200, 400, (240, 241, 242))

class Screen:
    def game(participating_horses, map):
        running = True
        field_hitboxes = [pygame.Rect(50, 50, 670, 320), pygame.Rect(720, 300, 300, 200)]
        horse_objects = [john_horse, aquamarine_gambit, jovial_merryment, cherry_jubilee, the_sweetest_treat, slow_n_steady, foggy_afterevening]
        goal = pygame.Rect(1520, 350, 10, 10)
        
        for map_rect in map:
            if map_rect['type'] == "background_rect":
                field_hitboxes.append(map_rect['rect_value'])
                
            if map_rect['type'] == "goal":
                goal_sprite_path = map_rect["image_url"]
                goal = map_rect['rect_value']
            
        for participating_horse in participating_horses:
            with open("horses.json", "r") as f:
                horses_json = json.load(f)
                
            for horse in horses_json:
                if horse['name'] == participating_horse:
                    horse_dict = horse
                    break
                
            location_x, location_y = get_horse_start_pos(horse_objects, map)
            horse_objects.append(Horse(horse_dict['name'], horse_dict['speed'], 30, 30, location_x, location_y, horse_dict['image_url']))
            
        while running:
            clock = pygame.time.Clock()
            clock.tick(24)
            screen.fill((30, 45, 70)) 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                    
            for hitbox in field_hitboxes:
                pygame.draw.rect(screen, (100, 150, 200), (hitbox[0] - 20, hitbox[1] - 20, hitbox[2] + 40, hitbox[3] + 40))
            
            for map_rect in map:
                if map_rect['type'] == "background_rect":
                    pygame.draw.rect(screen, (40, 80, 130), map_rect['rect_value'])     
                
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    pygame.draw.rect(screen, horse.image_url, (horse.location_x, horse.location_y, horse.width, horse.height))      
                    if pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height).colliderect(goal):
                        print(f"WINNER! {horse.name}")
                        quit()
            pygame.draw.rect(screen, (255, 255, 255), goal)
            
            
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    horse.horse_move(field_hitboxes, horse_objects, goal)
                    horse.fix_vector_pair("horizontal", horse.vector_left["vector_measurement"], horse.vector_right["vector_measurement"])
                    horse.fix_vector_pair("vertical", horse.vector_up["vector_measurement"], horse.vector_down["vector_measurement"])
                    if not pygame.Rect(0, 0, 1470, 820).colliderect(pygame.Rect(horse.location_x, horse.location_y, horse.width, horse.height)):
                        horse.location_x, horse.location_y = get_horse_start_pos(horse, map)
            
            pygame.display.update()
            
Screen.game([], [])