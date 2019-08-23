import pygame
from pygame.locals import *

class Piece(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image(None, -1)
    
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value