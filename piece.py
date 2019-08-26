import pygame
from pygame.locals import *

import random



class Piece(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image(None, -1)
        self.type = random.randint(0,6)
    
    def _update_sprite():


    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value