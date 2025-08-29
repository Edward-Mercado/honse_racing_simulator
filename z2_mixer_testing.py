import pygame, os, random
from pygame import mixer
pygame.init()
mixer.init()

def play_honse_sound():
    honse_sfx_path = os.path.join("sfx", "honse.wav")
    honse_sfx = pygame.mixer.Sound(honse_sfx_path)
        
    pygame.mixer.Sound.play(honse_sfx)
    
def decide_to_play_honse_sound():
    if random.randint(1, 50) == 50:
        play_honse_sound()