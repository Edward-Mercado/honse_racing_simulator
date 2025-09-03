import pygame, json, os
from the_game import play_the_game

pygame.init()
pygame.mixer.set_num_channels(32)

screen = pygame.display.set_mode((1470, 820))

pygame.display.set_caption('Python Honse Racing Simulator')

starting_animation_going = True
starting_animation_going_number = 0

running = False
frames_since_animation_start = 0
start_button = pygame.Rect(485, -200, 500, 200)
title_text_coordinates = [-1000, 200]
creator_text_coordinates = [2000, 470]

with open("horses.json", "r") as file:
    horse_dictionaries = json.load(file)
    
horse_sprites = []
x_coordinate = -1500
for horse in horse_dictionaries:
    if horse["name"] != "Missing No.":
        horse_sprites.append([horse["image_url"], [x_coordinate, 50]])
        x_coordinate += 80

def get_speed(frames_since_animation_start):
    return 10*frames_since_animation_start

def play_menu_screen():
    running_play_menu = True
    frames_since_animation_start = 0
    
    with open("map_menu_displays.json", "r") as file:
        map_menu_displays = json.load(file)
        
    
    selected_map = None
    random_on = True
    participating_horses = []
    max_fps = 60
    frames_since_last_key_press = 0
    
    while running_play_menu:
        clock = pygame.time.Clock()
        clock.tick(max_fps)
        
        frames_since_last_key_press += 1
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        screen.fill((200, 230, 255))
        
        title_font = pygame.font.SysFont(None, 100, bold=True)
        title_text = title_font.render("MAP SELECTION", True, (20, 30, 45))
        title_surface = title_text.get_rect(center=(720, 100))
        screen.blit(title_text, title_surface)
        
        for map_menu_display in map_menu_displays:
            map_rect = pygame.Rect(map_menu_display["x"], map_menu_display["y"], 200, 100)
            color = (130, 170, 200)
            font_color = (255, 255, 255)
            if map_rect.collidepoint(pygame.mouse.get_pos()):
                color = (160, 200, 230)
                if pygame.mouse.get_pressed()[0] == 1 and frames_since_last_key_press > 5:
                    frames_since_last_key_press = 0
                    selected_map = map_menu_display["map_name"]
                    

            if map_menu_display["map_name"] == selected_map:
                color = (200, 230, 255)   
                font_color = (0, 0, 0)
                pygame.draw.rect(screen, (10, 10, 35), (map_rect[0]-10, map_rect[1]-10, map_rect[2]+20, map_rect[3]+20), border_radius=20)
            
            pygame.draw.rect(screen, color, map_rect, border_radius=20)
            
            map_name = map_menu_display["map_name"]
            map_name = map_name.split(" ")
            
            map_font = pygame.font.SysFont(None, 40, bold=True, italic=True)
            map_text = map_font.render(map_name[0], True, font_color)
            map_surface = map_text.get_rect(centerx=map_rect.centerx, centery=map_rect.centery-20)
            screen.blit(map_text, map_surface)
            
            if len(map_name) == 2:
                map_text_2 = map_font.render(map_name[1], True, font_color)
                map_surface_2 = map_text_2.get_rect(centerx=map_rect.centerx, centery=map_rect.centery+20)
                screen.blit(map_text_2, map_surface_2)
            elif len(map_name) > 2:
                rest_of_map_name = ""
                for word in map_name[1:]:
                    rest_of_map_name += (word)
                    rest_of_map_name += " "
                
                map_text_2 = map_font.render(rest_of_map_name, True, font_color)
                map_surface_2 = map_text_2.get_rect(centerx=map_rect.centerx, centery=map_rect.centery+20)
                screen.blit(map_text_2, map_surface_2)
                
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
            
        title_text_2 = title_font.render("HONSE SELECTION", True, (20, 30, 45))
        title_surface_2 = title_text_2.get_rect(center=(720, 500))
        screen.blit(title_text_2, title_surface_2)
        
        with open("horse_menu_displays.json", "r") as file:
            horse_menu_displays = json.load(file)
        
        for horse in horse_menu_displays:
            horse_rect = pygame.Rect(horse["x"]+100, horse["y"]-30, horse["width"], horse["height"])
            
            horse_image_url = os.path.join("images", horse["image_url"])
            horse_image = pygame.image.load(horse_image_url)
            horse_image = pygame.transform.scale(horse_image, (horse["width"], horse["height"]))
            
            if horse["name"] not in participating_horses:
                tint_color = (0, 0, 0)
                tinted_horse_image = horse_image.copy()
                tinted_horse_image.fill(tint_color, None, pygame.BLEND_RGBA_MULT)
                horse_image = tinted_horse_image
            
            screen.blit(horse_image, (horse["x"]+100, horse["y"]-30))         
            
            if horse_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] == 1 and frames_since_last_key_press > 5:
                    frames_since_last_key_press = 0
                    if horse["name"] in participating_horses:
                        participating_horses.remove(horse["name"])
                    else:
                        participating_horses.append(horse["name"])   
        
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        
        random_horses_button = pygame.Rect(1310, 520, 130, 180)
        color = (130, 170, 200)
        font_color = (255, 255, 255)
        if random_horses_button.collidepoint(pygame.mouse.get_pos()):
            color = (160, 200, 230)
            if pygame.mouse.get_pressed()[0] == 1 and frames_since_last_key_press > 5:
                frames_since_last_key_press = 0
                random_on = (True if random_on==False else False)
                
        if random_on == False:
            pygame.draw.rect(screen, (20, 30, 45), (random_horses_button[0]-10, random_horses_button[1]-10, random_horses_button[2]+20, random_horses_button[3]+20), border_radius=20)
            color = (200, 230, 255)
            font_color = (0, 0, 0)
            
        pygame.draw.rect(screen, color, random_horses_button, border_radius=20)
        
        text_font = pygame.font.SysFont(None, 30, bold=True, italic=True)
        
        selection_text_1 = text_font.render("JUST", True, font_color)
        selection_text_2 = text_font.render("THESE", True, font_color)
        selection_text_3 = text_font.render("HONSES", True, font_color)
        
        selection_surface_1 = selection_text_1.get_rect(centerx=random_horses_button.centerx-20, centery=random_horses_button.centery-40)
        selection_surface_2 = selection_text_1.get_rect(centerx=random_horses_button.centerx-20, centery=random_horses_button.centery)
        selection_surface_3 = selection_text_1.get_rect(centerx=random_horses_button.centerx-20, centery=random_horses_button.centery+40)
        
        screen.blit(selection_text_1, selection_surface_1)
        screen.blit(selection_text_2, selection_surface_2)
        screen.blit(selection_text_3, selection_surface_3)
        
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        
        start_button = pygame.Rect(135, 720, 1200, 70)
        color = (130, 170, 200)
        
        if start_button.collidepoint(pygame.mouse.get_pos()):
            color = (160, 200, 230)
            if pygame.mouse.get_pressed()[0] == 1 and frames_since_last_key_press > 5:
                chosen_horses = []
                for horse in participating_horses:
                    chosen_horses.append(horse)
                frames_since_last_key_press = 0
                if selected_map != None:
                    play_the_game(random_on, True, participating_horses, False, 60, selected_map)
                    participating_horses = chosen_horses
                else:
                    play_the_game(random_on, False, participating_horses, False, 60, selected_map)
                    participating_horses = chosen_horses
                       
        pygame.draw.rect(screen, color, start_button, border_radius=35)
        start_text = title_font.render("START GAME", True, (255, 255, 255))
        start_surface = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_surface)
        
        pygame.display.update()
    # play_the_game(random_on, map_chosen, participating_horses, gambling, max_fps, selected_map)

fps = 60
while starting_animation_going:
    frames_since_animation_start += 1
    clock = pygame.time.Clock()
    clock.tick(fps)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            fps = 1000
    
    screen.fill((200, 230, 255))
    
    start_button_color = (130, 170, 200)
    
    pygame.draw.rect(screen, start_button_color, start_button, border_radius=100)
    start_button_font = pygame.font.SysFont(None, 160, bold=True, italic=True)
    start_button_text = start_button_font.render("RACE!", True, (255, 255, 255))
    start_button_rect = start_button_text.get_rect(centerx=start_button.centerx, centery=start_button.centery+5)
    screen.blit(start_button_text, start_button_rect)
    
    pygame.draw.rect(screen, (40, 50, 100), (title_text_coordinates[0]-600, title_text_coordinates[1]-75, 1200, 300), border_radius=20)
    
    title_font = pygame.font.SysFont(None, 200, bold=True)
    title_text = title_font.render("HONSE RACING", True, (255, 255, 255))
    title_surface = title_text.get_rect(center=(title_text_coordinates[0], title_text_coordinates[1]))
    screen.blit(title_text, title_surface)
    
    title_text_2 = title_font.render("SIMULATOR", True, (255, 255, 255))
    title_surface_2 = title_text_2.get_rect(center=(title_text_coordinates[0], title_text_coordinates[1] + 150))
    screen.blit(title_text_2, title_surface_2)
    
    creator_font = pygame.font.SysFont(None, 50, italic=True)
    creator_text = creator_font.render("by Edward Mercado", True, (0, 0, 20))
    creator_surface = creator_text.get_rect(center=(creator_text_coordinates[0], creator_text_coordinates[1]))
    screen.blit(creator_text, creator_surface)
    
    for horse in horse_sprites:
        horse_file_path = os.path.join("images", horse[0])
        horse_image = pygame.image.load(horse_file_path)
        horse_image = pygame.transform.scale(horse_image, (70, 70))
        horse_image_rect = horse_image.get_rect(center=(horse[1][0], horse[1][1]))
        screen.blit(horse_image, horse_image_rect)
    
    if starting_animation_going_number == 0:
        start_button[1] += get_speed(frames_since_animation_start)
        if start_button[1] >= 500:
            starting_animation_going_number += 1
        
    if starting_animation_going_number == 1:
        start_button[1] -= 40
        if start_button[1] <= 450:
            starting_animation_going_number += 1
    
    if starting_animation_going_number == 2:
        start_button[1] += 20
        if start_button[1] >= 550:
            starting_animation_going_number += 1
            
    if starting_animation_going_number == 3:
        title_text_coordinates[0] += 60
        creator_text_coordinates[0] -= 45
        
        if title_text_coordinates[0] >= 735:
            title_text_coordinates[0] = 735
            
        if creator_text_coordinates[0] <= 735:
            creator_text_coordinates[0] = 735
            
        if title_text_coordinates[0] == 735 and creator_text_coordinates[0] == 735:
            starting_animation_going_number += 1
    
    if starting_animation_going_number == 4:
        for horse in horse_sprites:
            horse[1][0] += 40
            if horse[1][0] >= 1400:
                for horse in horse_sprites:
                    horse[1][0] -= 10
                starting_animation_going_number += 1
                
    if starting_animation_going_number == 5:
        starting_animation_going = False
        
    pygame.display.update()
    
running = True
start_button_hovering = False

random_on, map_chosen, gambling = True, True, False
participating_horses = []
max_fps = 60
map_choice = "Blank Field"

while running:
    frames_since_animation_start += 1
    clock = pygame.time.Clock()
    clock.tick(60)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_hovering == True:
                play_menu_screen()
    
    screen.fill((200, 230, 255))
    
    start_button_color = (130, 170, 200)
    if start_button.collidepoint(pygame.mouse.get_pos()):
        start_button_color = (160, 200, 230)
        start_button_hovering = True
    else:
        start_button_hovering = False
        
    pygame.draw.rect(screen, start_button_color, start_button, border_radius=100)
    start_button_font = pygame.font.SysFont(None, 160, bold=True, italic=True)
    start_button_text = start_button_font.render("RACE!", True, (255, 255, 255))
    start_button_rect = start_button_text.get_rect(centerx=start_button.centerx, centery=start_button.centery+5)
    screen.blit(start_button_text, start_button_rect)
    
    pygame.draw.rect(screen, (40, 50, 100), (title_text_coordinates[0]-600, title_text_coordinates[1]-75, 1200, 300), border_radius=20)
    
    title_font = pygame.font.SysFont(None, 200, bold=True)
    title_text = title_font.render("HONSE RACING", True, (255, 255, 255))
    title_surface = title_text.get_rect(center=(title_text_coordinates[0], title_text_coordinates[1]))
    screen.blit(title_text, title_surface)
    
    title_text_2 = title_font.render("SIMULATOR", True, (255, 255, 255))
    title_surface_2 = title_text_2.get_rect(center=(title_text_coordinates[0], title_text_coordinates[1] + 150))
    screen.blit(title_text_2, title_surface_2)
    
    creator_font = pygame.font.SysFont(None, 50, italic=True)
    creator_text = creator_font.render("by Edward Mercado", True, (0, 0, 20))
    creator_surface = creator_text.get_rect(center=(creator_text_coordinates[0], creator_text_coordinates[1]))
    screen.blit(creator_text, creator_surface)
    
    for horse in horse_sprites:
        horse_file_path = os.path.join("images", horse[0])
        horse_image = pygame.image.load(horse_file_path)
        horse_image = pygame.transform.scale(horse_image, (70, 70))
        horse_image_rect = horse_image.get_rect(center=(horse[1][0], horse[1][1]))
        screen.blit(horse_image, horse_image_rect)
        
    pygame.display.update()