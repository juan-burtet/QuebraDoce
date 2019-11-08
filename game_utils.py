import pygame
import numpy as np
from pygame.locals import *
import os, sys

fonts = {}
fonts['NES'] = 'assets/fonts/pixel_nes.otf'


""" Carrega a imagem, retornando a surface e rect """
def load_image(name, colorkey=None, size=(60,60)):

    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    image = image.convert_alpha()
    image = pygame.transform.scale(image, size)
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

""" Carrega uma fase de um arquivo csv. """
def load_level(file_csv):

    # Checa se o arquivo existe
    if os.path.exists(file_csv):
        file = open(file_csv, "r")
    else:
        print("File don't Exist!")
        exit()
    
    # Inicia a leitura de linhas
    line = file.readline()

    # Recebe a informação dos campos
    info = [int(x) for x in line.split(',')]

    level = []
    for i in range(9):
        line = file.readline()
        level.append([int(x) for x in line.split(',')])
    
    return info, level