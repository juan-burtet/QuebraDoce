import pygame
from pygame.locals import *
from game_utils import *

import random

path_image = "assets/sprite/"
BLUE   = (146, 179, 255)

'''
Representa uma simples Peça no Tabuleiro,
serve como uma classe abstrata
'''
class Piece(pygame.sprite.Sprite):

    topleft = (225, 25)
    space = 2

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def get_pos(self):
        return (self.x, self.y)
    
    def get_piece(self):
        return (self.image, self.rect)
    
    def update_rect(self):
        # Atualiza a posição da peça
        self.rect.topleft = self.topleft
        self.rect.left += self.x * (self.space + self.rect.width)
        self.rect.top  += self.y * (self.space + self.rect.height)

'''
Representa uma área onde não pode possuir peças
'''
class Block(Piece):
    
    sprite = path_image + \
        "pieces/block/0.png"

    def __init__(self, x,y):
        Piece.__init__(self, x,y)

        self.image, self.rect = load_image(
            self.sprite, -1)
        
        self.update_rect()

'''
Representa uma peça de Objetivo que precisa ser
retirada do campo
'''
class Objective(Piece):

    # Sprite da imagem
    sprite = path_image + \
        "pieces/objective/0.png"

    def __init__(self, x,y):
        Piece.__init__(self, x, y)
        
        # Imagem e o rect da sprite
        self.image, self.rect = load_image(
            self.sprite, -1)
        
        self.update_rect()


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

        self.update_rect()

class Protection(Simple):

    def __init__(self, x, y, n):

        Simple.__init__(self, x, y, n)
        
        # Imagem e o rect da sprite
        self.image, self.rect = load_image(
            self.sprites[self.type], -1)
        
        # Desenha o quadrado transparente
        s = pygame.Surface(self.rect.size)
        s.fill(BLUE)
        s.blit(self.image, (self.rect.left, self.rect.top))
        self.image = s

        self.update_rect()


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

