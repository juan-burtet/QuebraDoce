import pygame
from pygame.locals import *
from game_utils import *

import random

path_image = "assets/sprite/"

'''
Representa uma simples Peça no Tabuleiro,
serve como uma classe abstrata
'''
class Piece(pygame.sprite.Sprite):

    topleft = (20,20)
    space = 5

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def get_piece(self):
        return (self.image, self.rect)

'''
Representa uma área onde não pode possuir peças
'''
class Block(Piece):
    
    def __init__(self, x,y):
        Piece.__init__(self, x,y)

'''
Representa uma peça de Objetivo que precisa ser
retirada do campo
'''
class Objective(Piece):

    # Sprite da imagem
    sprite = path_image + \
        "pieces/objective/cane.png"

    def __init__(self, x,y):
        Piece.__init__(self, x, y)
        
        # Imagem e o rect da sprite
        self.image, self.rect = load_image(
            self.sprite, -1)


'''
Representa a peça mais simples do campo, antes de 
ter qualquer upgrade
'''
class Simple(Objective):

    # Conjunto de imagens 
    # aux = path_image + "pieces/simple/"
    sprites = [
        "%s%d.png" % (path_image + "pieces/simple/", i) \
            for i in range(6)
    ]

    def __init__(self, x, y, n):

        # Inicializa a peça
        Objective.__init__(self, x, y)
        self.type = random.randint(0,n-1)

        # Imagem e o rect da sprite
        self.image, self.rect = load_image(
            self.sprites[self.type], -1)
        
        # Atualiza a posição da peça
        self.rect.topleft = self.topleft
        self.rect.left += self.space + self.x * self.rect.width
        self.rect.top  += self.space + self.y * self.rect.height

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

