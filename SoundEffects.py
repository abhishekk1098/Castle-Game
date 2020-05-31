import pygame
from pygame.locals import *

# Initialize Mixer ------->
pygame.mixer.init()
# ------------------------>

# Load Sounds ------------>
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/elevator.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
# ------------------------>
