import pygame
from pygame.locals import *

import random

'''
Representa uma simples Peça no Tabuleiro,
serve como uma classe abstrata
'''
class Piece(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
    def _update_sprite():
        pass

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

'''
Representa um bloqueio que precisa de n movimentos 
para ser eliminado
'''
class Block(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        pass

'''
Representa uma peça de Objetivo que precisa ser
retirada do campo
'''
class Objective(Piece):

    def __init__(self):
        Piece.__init__(self)
        pass 

'''
Representa a peça mais simples do campo, antes de 
ter qualquer upgrade
'''
class Simple(Objective):

    def __init__(self, n):
        Objective.__init__(self)
        #self.image, self.rect = load_image(None, -1)
        self.type = random.randint(0,n)
        pass

'''
Representa uma peça listrada, que possui
a habilidade ...
'''
class Stripped(Simple):

    def __init__(self):
        Simple.__init__(self)
        pass

'''
Representa uma peça goma, que possui 
a habilidade ...
'''
class Wrapped(Simple):

    def __init__(self):
        Simple.__init__(self)
        pass

'''
Representa uma peça bomba, que possui
a habilidade de eliminar todas as peças de 
mesma cor do campo
'''
class Bomb(Simple):

    def __init__(self):
        Simple.__init__(self)
        pass

