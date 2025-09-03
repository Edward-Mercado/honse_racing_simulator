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

while starting_animation_going:
    frames_since_animation_start += 1
    clock = pygame.time.Clock()
    clock.tick(60)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
    
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
                play_the_game(random_on, map_chosen, participating_horses, gambling, max_fps, map_choice)
    
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

