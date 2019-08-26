import pygame
import numpy as np
from pygame.locals import *

import piece
import board

size = width, height = 800, 600

class Game(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
    def play(self):
        pygame.init()



        