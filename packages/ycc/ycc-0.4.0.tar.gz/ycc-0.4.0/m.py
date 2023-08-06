import pygame_sdl2
pygame_sdl2.import_as_pygame()
import sys
import pygame
from pygame.locals import *

pygame.init()
#pygame.mixer.init()
pygame.display.set_mode([0,0])
pygame.display.set_caption('music', icontitle='pydroball.png')
d='/storage/emulated/0/1.mp3'
pygame.mixer.music.load(d)
pygame.mixer.music.play()
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()