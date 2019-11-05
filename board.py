import pygame
import numpy as np
from pygame.locals import *

import piece
import game_utils

class Board(pygame.sprite.Sprite):

    def __init__(self, file=None):
        pygame.sprite.Sprite.__init__(self)
        
        if file is not None:
            info, level = game_utils.load_level(file)
            self._get_info(info=info)
            self._create_level(level=level)
        else:
            self._create_level()
            self._get_info()


    def _set_mode(self):
        modes = 0

        # Se tiver objetivo de pontos, atualiza
        if self.w_points > 0:
            self.mode = 'POINTS'
            modes += 1

        # Se tiver objetivos de bloqueios, atualiza
        if self.blocks > 0:
            self.mode = 'BLOCKS'
            modes += 1

        # Se tiver objetivos de itens, atualiza
        if self.canes > 0:
            self.mode = 'OBJECTIVE'
            modes += 1

        # Se tiver mais de um modo, atualiza pra MIX
        if modes > 1:
            self.mode = 'MIX'

    def _get_info(self, info=None):
        self.points = 0

        if info is not None:
            self.moves = info[0]
            self.w_points = info[1]
            self.canes = info[2]
            self.blocks = info[3]
            self._set_mode()
        else:
            self.mode = 'POINTS'
            self.w_points = 500000
            self.blocks = 0
            self.canes = 0
            self.moves = 30

    def _create_level(self, level=None):

        self.level = np.zeros((9, 9), dtype=object)

        if level is not None:
            for i, row in enumerate(level):
                for j, p in enumerate(row):
                    if p == 0:
                        self.level[j][i] = piece.Block(j,i)
                    elif p == 1:
                        self.level[j][i] = piece.Simple(j,i,6)
                    elif p == 2:
                        self.level[j][i] = piece.Protection(j,i,6)
                    elif p == 3:
                        self.level[j][i] = piece.Objective(j,i)
                    pass
        else:
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

