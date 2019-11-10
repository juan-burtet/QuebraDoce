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
class Piece():

    topleft = (225, 25)
    space = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 20

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    # Retorna a posição da peça
    def get_pos(self):
        return (self.x, self.y)
    
    def get_piece(self):

        # Pygame precisa estar inicializado
        if pygame.get_init():
            return (self.image, self.rect)
        else:
            return (None, None)
    
    # Atualiza o rect da peça
    def update_rect(self):

        # Pygamegame precisa estar inicializado
        if pygame.get_init():

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

        # Pygamegame precisa estar inicializado
        if pygame.get_init():
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
        
        # Pygamegame precisa estar inicializado
        if pygame.get_init():

            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprite, -1)
        
        self.update_rect()
        self.points = 10000

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

        # Pygamegame precisa estar inicializado
        if pygame.get_init():

            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprites[self.type], -1)

        self.points = 0
        self.update_rect()

'''
Representa a peça mais simples do campo com uma 
proteção azul que necessita ser quebrada
'''
class Protection(Simple):

    def __init__(self, x, y, n):

        Simple.__init__(self, x, y, n)

        # Pygamegame precisa estar inicializado
        if pygame.get_init():
        
            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprites[self.type], -1)
            
            # Desenha o quadrado transparente
            s = pygame.Surface(self.rect.size)
            s.fill(BLUE)
            s.blit(self.image, (self.rect.left, self.rect.top))
            self.image = s

        self.update_rect()
        self.points = 1000


    pass

'''
Representa uma peça listrada, que possui
a habilidade de eliminar uma linha ou uma coluna inteira,
dependendo do movimento da peça
'''
class Stripped(Simple):

    # Conjunto de imagens 
    # aux = path_image + "pieces/simple/"
    sprites = [
        "%s%d.png" % (path_image + "pieces/stripped/", i) \
            for i in range(6)
    ]

    def __init__(self, x, y, t):
        Simple.__init__(self, x, y, 1)
        self.type = t

        # Pygamegame precisa estar inicializado
        if pygame.get_init():

            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprites[self.type], -1)

        self.update_rect()
        self.points = 3000

'''
Representa uma peça goma, que possui 
a habilidade de eliminar as 8 peças a volta dela.
'''
class Wrapped(Simple):

    # Conjunto de imagens 
    # aux = path_image + "pieces/simple/"
    sprites = [
        "%s%d.png" % (path_image + "pieces/wrapped/", i) \
            for i in range(6)
    ]

    def __init__(self, x, y, t):
        Simple.__init__(self, x, y, 1)
        self.type = t

        # Pygamegame precisa estar inicializado
        if pygame.get_init():

            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprites[self.type], -1)

        self.update_rect()
        self.points = 6000
        pass

'''
Representa uma peça bomba, que possui
a habilidade de eliminar todas as peças de 
mesma cor do campo.
'''
class Bomb(Simple):

    sprite = path_image + 'pieces/bomb/0.png'

    def __init__(self, x, y):
        Simple.__init__(self, x, y, 1)

        # Pygamegame precisa estar inicializado
        if pygame.get_init():

            # Imagem e o rect da sprite
            self.image, self.rect = load_image(
                self.sprite, -1)

        
        self.type = -1
        self.update_rect()
        self.points = 10000
        pass

