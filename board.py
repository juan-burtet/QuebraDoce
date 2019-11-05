import pygame
import numpy as np
from pygame.locals import *
import copy

import piece
import game_utils

class Board(pygame.sprite.Sprite):

    def __init__(self, file=None):
        pygame.sprite.Sprite.__init__(self)
        
        if file is not None:
            info, level = game_utils.load_level(file)
            self._set_info(info=info)
            self._create_level(level=level)
        else:
            self._create_level()
            self._get_info()

    # Adiciona o modo de jogo
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

    # Adiciona as informações do mapa
    def _set_info(self, info=None):
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

    # Checa se o mapa não possui sequencias de 3 ou mais
    def _check_board(self, level):

        # Percorre todo o campo
        for i in range(9):
            for j in range(9):
                
                # Pega a peça e seu tipo
                p = level[i][j]
                t = None
                try:
                    t = p.type
                except:
                    continue

                # Se for maior, não precisa verificar
                if i + 2 < 9:

                    # Se encontrou uma sequência de mesmo tipo, 
                    # retorna True
                    for index in range(1,3):
                        p_aux = level[i+index][j]
                        t_aux = None
                        try:
                            t_aux = p_aux.type
                        except:
                            break

                        if t != t_aux:
                            break

                        if index == 2:
                            return True 

                # Se for maior, não precisa verificar
                if j + 2 < 9:

                    # Se encontrou uma sequência de mesmo tipo, 
                    # retorna True
                    for index in range(1,3):
                        p_aux = level[i][j+index]
                        t_aux = None
                        try:
                            t_aux = p_aux.type
                        except:
                            break

                        if t != t_aux:
                            break

                        if index == 2:
                            return True
        
        return False

    # Gera o mapa do jogo
    def _create_level(self, level=None):

        self.level = np.zeros((9, 9), dtype=object)

        # Se o nivel foi passado, inicializa
        if level is not None:
            for i, row in enumerate(level):
                for j, p in enumerate(row):
                    check = True

                    while(check):
                        if p == 0:
                            self.level[j][i] = piece.Block(j,i)
                        elif p == 1:
                            self.level[j][i] = piece.Simple(j,i,6)
                        elif p == 2:
                            self.level[j][i] = piece.Protection(j,i,6)
                        elif p == 3:
                            self.level[j][i] = piece.Objective(j,i)
                        
                        check = self._check_board(self.level)

        # Se não foi, cria um padrão
        else:
            for x in range(9):
                for y in range(9):
                    check = True
                    while(check):
                        self.level[x][y] = piece.Simple(x,y,6)
                        check = self._check_board(self.level)
    
    # Retorna uma lista com todas as peças
    def get_board(self):

        list_pieces = []
        for i in range(9):
            for j in range(9):
                list_pieces.append(
                    self.level[i][j].get_piece()
                )
        
        return list_pieces

    # Move as duas peças de lugar
    def _move_pieces(self, p1, p2):
        # Verifica as novas posições
        pos1 = (p1.x, p1.y)
        pos2 = (p2.x, p2.y)
        p1.x = pos2[0]
        p1.y = pos2[1]
        p2.x = pos1[0]
        p2.y = pos1[1]

        # Faz uma copia do nivel e troca as posições
        self.level[p1.x][p1.y] = p1
        self.level[p2.x][p2.y] = p2

    def _check_line(self, p):
        

    def _check_column(self, p):
        pass

    # Destroi todas as sequências de peças
    def _destroy_pieces(self):
        
        # Enquanto tiver possibilidades, destruir!
        while self._check_board(self.level):
            p = None
            for i in range(9):
                for j in range(9):
                    p = self.level[i][j]

                    # Se passou do limite, não precisa conferir
                    if i + 2 < 9:
                        line = self.check_line(p)
                    
                    # Se passou do limite, não precisa conferir
                    if j + 2 < 9:
                        column = self.check_column(p)
        pass

    # Testa se o movimento é possivel
    def test_move(self, p1, p2):

        self._move_pieces(p1,p2)

        if self._check_board(self.level):
            self._destroy_pieces()
        else:
            self._move_pieces(p1,p2)
            p1.update_rect()
            p2.update_rect()
