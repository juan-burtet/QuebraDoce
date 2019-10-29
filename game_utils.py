import pygame
import numpy as np
from pygame.locals import *
import os, sys

""" Carrega a imagem, retornando a surface e rect """
def load_image(name, colorkey=None):

    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    image = image.convert()
    image = pygame.transform.scale(image, (60,60))
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    
    return image, image.get_rect()

""" Carrega o som, retornando seu Sound Object """
def load_sound(name):

    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error as message:
        print('Cannot load sound:', wav)
        raise SystemExit(message)
    
    return sound