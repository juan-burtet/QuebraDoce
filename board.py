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
                self.level[x][y] = piece.Piece()
    
    def set_values(self):
        for i in range(9):
            for j in range(9):
                self.level[i][j].set_value(str(i) + str(j))
    
    def print_board(self):
        for i in range(9):
            print("|", end="")
            for j in range(9):
                print("", self.level[i][j].get_value(), end="")
            print(" |")