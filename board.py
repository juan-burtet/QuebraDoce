import pygame
import numpy as np
from pygame.locals import *
import piece

class Board(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._create_level()

    def _create_level(self):
        self.level = np.zeros((9, 9), dtype=object)
        for x in range(9):
            for y in range(9):
                self.level[x][y] = piece.Simple(x,y,6)
    
    def get_board(self):

        list_pieces = []
        for i in range(9):
            for j in range(9):
                list_pieces.append(
                    self.level[i][j].get_piece()
                )
        
        return list_pieces

