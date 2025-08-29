import pygame, json, os, time, math, random
from pygame import mixer

pygame.init()
mixer.init()

screen = pygame.display.set_mode((1470, 820))

pygame.display.set_caption('Python Honse Racing Simulator')
running = True
frames_since_game_begin = 0

smart_race = os.path.join("music", "smart_race.mp3")
critical_health_music = os.path.join("music", "critical_health.mp3")
mixer.music.load(smart_race)
mixer.music.play(-1)
frames_since_game_begin = 0
while running:
    frames_since_game_begin += 1
    clock = pygame.time.Clock()
    clock.tick(50)

    screen.fill((0, 0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
    
    if frames_since_game_begin == 200:
        mixer.music.fadeout(2000)
        mixer.music.unload()
        mixer.music.stop()
    elif frames_since_game_begin == 250:
        mixer.music.load(critical_health_music)
        mixer.music.play(-1)
    
    pygame.display.update()