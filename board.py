import pygame
import numpy as np
from pygame.locals import *
import copy

import piece
import game_utils

'''
Concentra o campo do jogo e trabalha com 
toda a movimentação e objetivos.
'''
class Board(pygame.sprite.Sprite):

    # Inicializador
    def __init__(self, file=None):
        pygame.sprite.Sprite.__init__(self)
        
        # Iniciaca as informações com o arquivo
        if file is not None:
            self.info, self.map = game_utils.load_level(file)
        else:
            self.info, self.map = None, None

        # Inicializa os mapas
        self._set_info()
        self._create_level()

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
    def _set_info(self):
        info = self.info
        self.points = 0

        self.types = 3
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
                    else:
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
                    else:
                        return True
        
        return False

    # Gera o mapa do jogo
    def _create_level(self, first=True):
        level = self.map
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
                            self.level[j][i] = piece.Simple(j,i,self.types)
                        elif p == 2:
                            if first:
                                self.level[j][i] = piece.Protection(j,i,self.types)
                            else:
                                self.level[j][i] = piece.Simple(j,i,self.types)
                        elif p == 3:
                            self.level[j][i] = piece.Objective(j,i)
                        
                        check = self._check_board(self.level)

        # Se não foi, cria um padrão
        else:
            for x in range(9):
                for y in range(9):
                    check = True
                    while(check):
                        self.level[x][y] = piece.Simple(x,y,self.types)
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
        p1.update_rect()
        p2.update_rect()

    # Checar todas as combinações com essa peça
    def _check_combinations(self, p):

        # Checa a sequencia a esquerda da peça
        x = p.x -1
        left = 0
        while x >= 0:
            
            # Verifica se é o mesmo tipo, caso ocorra algum
            # erro, é uma classe sem "tipo", então pula fora
            try:
                if self.level[x][p.y].type == p.type:
                    left += 1
                else:
                    break
            except:
                break
            
            x -= 1
        
        # Checa a sequencia a direita da peça
        x = p.x +1
        right = 0
        while x < 9:
            
            # Verifica se é o mesmo tipo, caso ocorra algum
            # erro, é uma classe sem "tipo", então pula fora
            try:
                if self.level[x][p.y].type == p.type:
                    right += 1
                else:
                    break
            except:
                break

            x += 1
        
        # Checa a sequência a cima da peça
        y = p.y -1
        top = 0
        while y >= 0:
            
            try:
                if self.level[p.x][y].type == p.type:
                    top += 1
                else:
                    break
            except:
                break
            
            y -= 1
        
        # Checa a sequência a baixo da peça
        y = p.y +1
        bottom = 0
        while y < 9:
            
            # Verifica se é o mesmo tipo, caso ocorra algum
            # erro, é uma classe sem "tipo", então pula fora
            try:
                if self.level[p.x][y].type == p.type:
                    bottom += 1
                else:
                    break
            except:
                break

            y += 1
        
        # Pega o tamanho das sequências
        row = left + right + 1 # linha
        col = top + bottom + 1 # coluna

        # Nova peça no local?
        new_piece = None
        if row >= 5 or col >= 5: # IGUAL A BOMBA!
            new_piece = piece.Bomb(p.x, p.y)
        elif row >= 3 and col >= 3: # IGUAL A WRAPPED
            new_piece = piece.Wrapped(p.x, p.y, p.type)
        elif row == 4 or col == 4: # IGUAL AO STRIPPED
            new_piece = piece.Stripped(p.x, p.y, p.type)

        # Indica se a peça foi deletada
        delete = False

        # Verifica a linha
        if row >= 3:
            delete = True
            for i in range(p.x - left, p.x):
                self.level[i][p.y] = None
            for i in range(p.x +1, p.x + right + 1):
                self.level[i][p.y] = None
        
        # Verifica a Coluna
        if col >= 3:
            delete = True
            for j in range(p.y - top, p.y):
                self.level[p.x][j] = None
            for j in range(p.y + 1, p.y + bottom + 1):
                self.level[p.x][j] = None
        
        # Se a peça foi deletada, exclui ela
        if delete:

            # Mas caso tenha uma nova peça gerada, coloca
            # ela nesta posição
            if new_piece is not None:
                self.level[p.x][p.y] = new_piece
            else:
                self.level[p.x][p.y] = None
        
        print(
            "Left: %d" % left,
            "Right: %d" % right,
            "Top: %d" % top,
            "Bottom: %d" % bottom
        )

    # Destroi as peças do campo
    def _destroy_pieces(self, pieces):
        
        # Checa a combinação dessas duas peças
        print("Começou a destruição")
        for p in pieces:
            print("(%d,%d)" % (p.x, p.y))
            self._check_combinations(p)
            print("")
        print("Acabou a destruição!")

        # Percorre todas as colunas
        for x in range(9):
            
            # Vai da posição mais baixa até ao topo
            for y in reversed(range(9)):

                # Se a posição for None, é necessário
                # buscar as posições     
                if self.level[x][y] is None:
                    find = False

                    # Percorre até encontrar uma peça diferente
                    # de None e diferente de Block
                    for i in reversed(range(y)):

                        p = self.level[x][i]
                        if (p is not None) and (type(p) is not piece.Block):
                            find = True
                            
                            # Atualiza com a posição nova
                            p.x = x
                            p.y = y
                            self.level[x][y] = p

                            # Retira a peça da posição antiga
                            self.level[x][i] = None

                            # Se tiver combinações, destroi na localização
                            # dessa peça
                            if self._check_board(self.level):
                                return self._destroy_pieces([p])
                            
                            # Atualiza a posição dela no campo
                            self.level[x][y].update_rect()

                            # Já adicionou peça, pode sair do laço!
                            break
                    
                    # Se não encontrou nenhuma peça,
                    # adiciona novas peças nas posições
                    if not find:
                        
                        # Começa da peça até o topo
                        for i in reversed(range(y+1)):
                            
                            # Se não for uma proteção, adiciona a peça nova!
                            if type(self.level[x][i]) is not piece.Block:

                                # Adiciona a nova peça
                                self.level[x][i] = piece.Simple(x,i,self.types)

                                # Se gerou uma nova possibilidade, destruir!
                                if self._check_board(self.level):
                                    return self._destroy_pieces(
                                        [self.level[x][i]])
                        
                        # Já adicionou peças o suficiente,
                        # pode pular pra próxima posição
                        break

        # O Tabuleiro está completo novamente, agora
        # se não tiver movimentos possiveis, gera novamente
        if not self._has_moves():
            self._create_level(first=False)
        
        # Atualiza as posições
        self._update_rects()

    # Atualiza os rects das peças
    def _update_rects(self):
        for x in range(9):
            for y in range(9):
                p = self.level[x][y]
                p.x = x
                p.y = y
                p.update_rect()
    
    # Usado para verificar se o tabuleiro possui movimentos possiveis
    def _has_moves(self):

        # Percorre todo o campo
        for y in range(9):
            for x in range(9):

                # Pega o tipo da peça
                p = self.level[x][y]
                try:
                    t = p.type
                except:
                    continue
                
                # Checa as sequências para verificar movimentos
                if x + 3 < 9:
                    
                    # Percorre as 3 peças seguintes e
                    # verifica se só existe um tipo diferente
                    count = 0
                    for index in range(1,4):
                        p_aux = self.level[x+index][y]
                        t_aux = None
                        try:
                            t_aux = p_aux.type
                        except:
                            break
                        
                        # Se os tipos forem diferentes, 
                        # soma 1
                        if t_aux != t:
                            count += 1
                        
                        # Se encontrou mais que 1, pula
                        if count > 1:
                            break
                    # Se passou por todo esse processo, tem movimentos
                    else:
                        return True
                
                # Checa as sequências para verificar movimentos
                if y + 3 < 9:

                    # Percorre as 3 peças seguintes e
                    # verifica se só existe um tipo diferente
                    count = 0
                    for index in range(1,4):
                        p_aux = self.level[x][y+index]
                        t_aux = None
                        try:
                            t_aux = p_aux.type
                        except:
                            break
                        
                        # Se os tipos forem diferentes, 
                        # soma 1
                        if t_aux != t:
                            count += 1
                        
                        # Se encontrou mais que 1, pula
                        if count > 1:
                            break
                    # Se passou por todo esse processo, tem movimentos
                    else:
                        return True
        
        # Não possui movimentos
        return False

    # Testa se o movimento é possivel
    def test_move(self, p1, p2):

        # Troca as peças de posição
        self._move_pieces(p1,p2)

        # Se surgiu movimentos válidos,
        # destroi as peças em sequência
        if self._check_board(self.level):
            self._destroy_pieces([p1,p2])
        
        # Não surgiu movimentos válidos, retorna as
        # peças ao local correto
        else:
            self._move_pieces(p1,p2)

    # Método para todas as combinações especiais
    def _special_comb(self, p1, p2):

        # Caso os 2 tipos sejam iguais
        if type(p1) is type(p2):

            # Se for tipo Listrado:
            if type(p1) is piece.Stripped:
                # Elimina a linha e a coluna ao mesmo tempo
                pass
            
            # Se for tipo Goma
            elif type(p1) is piece.Wrapped:
                # Elimina as 24 peças em volta
                pass
            
            # Se for tipo Bomba
            elif type(p1) is piece.Bomb:
                # Destroi todas as peças do campo
                pass
        
        # Os dois tipos são diferentes
        else:

            # Se a primeira peça for Listrada
            if type(p1) is piece.Stripped:
                
                # Se a segunda peça for Goma
                if type(p2) is piece.Wrapped:
                    # Elimina 3 linhas e 3 colunas
                    pass

                # Se a segunda peça for Bomba
                elif type(p2) is piece.Bomb:
                    # Transforma todas as peças do mesmo tipo
                    # em listradas e ativa elas
                    pass
            
            # Se a primeira peça for Goma
            elif type(p1) is piece.Wrapped:
                
                # Se a segunda peça for Listrada
                if type(p2) is piece.Stripped:
                    # Elimina 3 linhas e 3 colunas
                    pass
                
                # Se a segunda peça for Bomba
                elif type(p2) is piece.Bomb:
                    # Transforma todas as peças do mesmo tipo
                    # em gomas, e ativa elas
                    pass
            
            # Se a primeira peça for Bomba
            elif type(p1) is piece.Bomb:
                
                # Se a segunda peça for Listrada
                if type(p2) is piece.Stripped:
                    # Transforma todas as peças do mesmo tipo
                    # em listradas e ativa elas
                    pass
                
                # Se a segunda peça for Goma
                elif type(p2) is piece.Wrapped:
                    # Transforma todas as peças do mesmo tipo
                    # em gomas, e ativa elas
                    pass