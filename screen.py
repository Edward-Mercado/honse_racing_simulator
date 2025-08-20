import pygame, json
from horse_logic import Horse
from collision_logic import handle_horse_collision, handle_wall_collision, get_opposite_direction, get_horse_start_pos

pygame.init()

screen = pygame.display.set_mode((1470, 820))
pygame.display.set_caption('Python Honse Racing Simulator')
running = True


john_horse = Horse("John Horse", 6, 30, 30, 40, 40, "john_horse.png")

class Screen:
    def game(participating_horses, map):
        running = True
        field_hitboxes = []
        horse_objects = [john_horse]
        
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
            screen.fill((30, 45, 70)) 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            
            for map_rect in map:
                if map_rect['type'] == "background_rect":
                    pygame.draw.rect(screen, (40, 80, 130), map_rect['rect_value'])     
                
            for horse in horse_objects:
                if isinstance(horse, Horse):
                    pygame.draw.rect(screen, (255, 255, 255), (horse.location_x, horse.location_y, horse.width, horse.height))      
            
            pygame.display.update()
            
Screen.game([], [])