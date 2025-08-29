import pygame, os, random
from pygame import mixer
pygame.init()
mixer.init()

def play_sound(file_name):
    sfx_path = os.path.join("sfx", file_name)
    sfx = pygame.mixer.Sound(sfx_path)
        
    pygame.mixer.Sound.play(sfx)
    
def play_music(file_name, loop):
    music_path = os.path.join("music", file_name)
    pygame.mixer.music.load(music_path)
    
    if loop == True:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()
        
def transition_music(next_music_file_name, loop, fade_ms):
    pygame.mixer.music.fadeout(fade_ms)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    
    pygame.mixer.music.load(next_music_file_name)
    if loop == True:
        pygame.mixer.music.play(-1, 0.0, fade_ms)
    else:
        pygame.mixer.music.play(1, 0.0, fade_ms)
        
def pause_music():
    pygame.mixer.music.pause()
    
def unpause_music():
    pygame.mixer.music.unpause()