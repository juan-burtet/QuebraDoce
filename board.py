import pygame
import numpy as np
from pygame.locals import *
import copy
import random

import piece
import game_utils


# Tipos especiais
special = (
    piece.Stripped,
    piece.Wrapped,
    piece.Bomb
)

# Tipos que não quebram
extra = (
    piece.Objective,
    piece.Block
)

'''
Concentra o campo do jogo e trabalha com 
toda a movimentação e objetivos.
'''
class Board(pygame.sprite.Sprite):

    # Inicializador
    def __init__(self, file=None, string=None):
        pygame.sprite.Sprite.__init__(self)
        
        # Estado do Random
        self.state = None

        # Iniciaca as informações com o arquivo
        if file is not None:
            self.info, self.map = game_utils.load_level(file)
        elif string is not None:
            self.info, self.map = game_utils.load_level_string(string)
        else:
            self.info, self.map = None, None

        # Quantidade de Peças Destruidas
        self.piece_destroyed = 0

        # Quantidade de pontos desde a ultima rodada
        self.last_round_points = 0

        # Inicializa os mapas
        self._create_labels()
        self._set_info()
        self._create_level()

    def copy_level(self, level):
        for x in range(9):
            for y in range(9):
                self.level[x][y] = copy.deepcopy(level[x][y])
        pass

    def _print_board(self):
        for i in range(9):
            for j in range(9):
                p = self.level[i][j]
                string = ''
                if p is None:
                    string += '_'
                elif type(p) is piece.Block:
                    string += 'X'
                elif type(p) is piece.Objective:
                    string += "O"
                elif type(p) is piece.Simple:
                    string += "s"
                elif type(p) is piece.Protection:
                    string += "p"
                elif type(p) is piece.Stripped:
                    string += "S"
                elif type(p) is piece.Wrapped:
                    string += "W"
                elif type(p) is piece.Bomb:
                    string += "B"
                else:
                    string += "_"
                print("%s " % string, end="")
            print("")
        print("")

    # Retorna o quanto cada cane está pra ser completo
    def get_canes_reward(self):
        canes = []

        level = self.map
        for i, row in enumerate(level):
            for j, p in enumerate(row):
                if self.labels[j][i] == 3:
                    x = i/8
                    canes.append(x)
        
        return canes

    # Retorna o estado do random
    def get_random_state(self):
        if self.state is None:
            self.state = random.getstate()
        return self.state
    
    # Seta o estado do random
    def set_random_state(self, state):
        self.state = state

    # Atualiza o estado do random
    def update_random_state(self):
        if state is not None:
            random.setstate(self.state)

    # Verifica se o jogo foi finalizado
    def is_finished(self):

        # Verifica se a pontuação feita é maior que a necessária
        if self.w_points > self.points:
            return False
        
        # Verifica se os ingredientes já estão fora do mapa
        if self.canes > 0:
            return False
        
        # Verifica se todos os bloqueios foram destruidos
        if self.blocks > 0:
            return False
        
        # Acabou o jogo
        return True

    # Define os labels das posições de peças especiai
    def _create_labels(self, first=True):
        level = self.map

        # Inicializa os labels com 0
        self.labels = np.zeros((9,9), dtype=int)
        if first:
            if level is not None:
                for i, row in enumerate(level):
                    for j, p in enumerate(row):
                        
                        # Se tiver um objetivo ou proteção
                        if p == 2 or p == 3:
                            self.labels[j][i] = p
        else:
            for x in range(9):
                for y in range(9):
                    p = self.level[x][y]
                    if p is not None:
                        if type(p) is piece.Objective:
                            self.labels[x][y] = 3
                        elif type(p) is piece.Protection:
                            self.labels[x][y] = 2

    # Atualiza os objetivos
    def _update_objectives(self):

        self.canes, self.blocks = 0, 0
        for x in range(9):
            for y in range(9):
                if self.labels[x][y] == 2:
                    self.blocks += 1
                elif self.labels[x][y] == 3:
                    self.canes += 1

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
        if info is not None:
            self.moves = info[0]
            self.w_points = info[1]
            self.types = info[2]
        else:
            self.w_points = 9999999
            self.blocks = 0
            self.canes = 0
            self.moves = 75
            self.types = 6
        
        # Atualiza os objetivos
        self._update_objectives()

        # Atualiza o modo do jogo
        self._set_mode()

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

                    # Gera peças enquanto não for uma jogada válida
                    while(check):
                        
                        # Adiciona uma Proteção
                        if self.labels[j][i] == 2:
                            self.level[j][i] = piece.Protection(j,i,self.types)
                        
                        # Adiciona um Objetivo
                        elif self.labels[j][i] == 3:
                            self.level[j][i] = piece.Objective(j,i)

                        # Adiciona um bloqueio
                        elif p == 0:
                            self.level[j][i] = piece.Block(j,i)

                        # Adiciona uma peça simples
                        else:
                            self.level[j][i] = piece.Simple(j,i,self.types)
                        
                        # Verifica se tem jogadas possiveis
                        check = self._check_board(self.level)

        # Se não foi, cria um padrão
        else:
            for x in range(9):
                for y in range(9):
                    check = True
                    while(check):
                        self.level[x][y] = piece.Simple(x,y,self.types)
                        check = self._check_board(self.level)
        
        if not self._has_moves():
            return self._create_level(first=False)

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
    def _check_combinations(self, p, factor):

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
            # for i in range(p.x - left, p.x):
            #     self._destroy_single_piece(self.level[i][p.y])
            # for i in range(p.x +1, p.x + right + 1):
            #     self._destroy_single_piece(self.level[i][p.y])
            for i in range(p.x - left, p.x + right + 1):
                self._destroy_single_piece(self.level[i][p.y])
        
        # Verifica a Coluna
        if col >= 3:
            delete = True
            # for j in range(p.y - top, p.y):
            #     self._destroy_single_piece(self.level[p.x][j])
            # for j in range(p.y + 1, p.y + bottom + 1):
            #     self._destroy_single_piece(self.level[p.x][j])
            for j in range(p.y - top, p.y + bottom + 1):
                self._destroy_single_piece(self.level[p.x][j])
        
        # Se a peça foi deletada, exclui ela
        if delete:

            # Mas caso tenha uma nova peça gerada, coloca
            # ela nesta posição
            #self._destroy_single_piece(self.level[p.x][p.y])
            if new_piece is not None:
                self.level[p.x][p.y] = new_piece
            
            # Total de peças
            total = row + col - 1
            total -= 2
            self.points += (total * 60) * factor

    # Destroi as peças do campo
    def _destroy_pieces(self, pieces, factor=0):
        
        # Aumenta o fator pra aumentar nas cascatas
        factor += 1

        # Checa a combinação dessas duas peças
        for p in pieces:
            self._check_combinations(p, factor)

        # Verifica se um objetivo foi encontrado
        found_objective = False

        # Percorre todas as colunas
        for x in range(9):
            
            blocks = True

            # Vai da posição mais baixa até ao topo
            for y in reversed(range(9)):

                # Se encontrou o objetivo enquanto tem blocks em baixo, deleta!
                if type(self.level[x][y]) is piece.Objective and blocks:
                    found_objective = True
                    self._eliminate_piece(self.level[x][y])

                # Se não for block
                if type(self.level[x][y]) is not piece.Block:
                    blocks = False

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
                                return self._destroy_pieces([p], factor=factor)
                            
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
                                    return self._destroy_pieces([self.level[x][i]], factor=factor)
                        
                        # Já adicionou peças o suficiente,
                        # pode pular pra próxima posição
                        break
        
        # Encontrou objetivo, destroi novamente
        if found_objective:
            return self._destroy_pieces([])

        # Verifica as peças na ultima posição
        destroy = False
        for x in range(9):
            if type(self.level[x][8]) is piece.Objective:
                self._eliminate_piece(self.level[x][8])
                destroy = True
        
        # Se destruiu, refazer novamente
        if destroy:
            return self._destroy_pieces([])


        # Atualiza os labels dos objetivos
        self._create_labels(first=False)
        
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

    # Informações retornadas
    def _finish_move(self):

        # Calcula a quantidade de pontos feitos
        points = self.points - self.last_round_points
        self.last_round_points = self.points

        # Atualiza os objetivos
        self._update_objectives()

        return (
            points, # Pontos Feito nesta rodada,
            self.piece_destroyed, # Peças Eliminadas nesta rodada,
            self.is_finished() or (self.moves == 0), # Indica se a partida terminou 
            self.is_finished() # Indica se a partida foi ganha
        )  

    # Testa se o movimento é possivel
    def test_move(self, p1, p2, mcts=False):

        # Se o MCTS for verdadeiro, inicializa o state do random
        if mcts:
            self.update_random_state()

        # Se o jogo terminou, não pode jogar!
        if self.is_finished():
            return None

        self.piece_destroyed = 0

        # Se não tiver combinações especiais
        if not self._special_comb(p1, p2):

            # Troca as peças de posição
            self._move_pieces(p1,p2)

            # Se surgiu movimentos válidos,
            # destroi as peças em sequência
            if self._check_board(self.level):

                # print("Jogada sem combinações Especiais!\n")
                self._destroy_pieces([p1,p2])
                self.moves -= 1
                #self._print_possible_moves(self.possible_moves())
                return self._finish_move()
            
            # Não surgiu movimentos válidos, retorna as
            # peças ao local correto
            else:
                self._move_pieces(p1,p2)
        
        # Teve combinações especiais!
        else:
            # print("Jogada teve combinações Especiais!\n")
            self._destroy_pieces([])
            self.moves -= 1
            #self._print_possible_moves(self.possible_moves())
            return self._finish_move()

        # Retorna Nada
        return None

    # Usado para eliminar esta peça do campo
    def _eliminate_piece(self, p):
        if p is not None:
            self.piece_destroyed += 1
            self.points += p.points
            self.level[p.x][p.y] = None

    # Elimina a linha e a coluna ao mesmo tempo [FEITO]
    def _special_double_stripped(self, p):
        # print("Especial: Listrada dupla!")

        if p is None:
            return

        x = p.x
        for y in range(9):
            aux_p = self.level[x][y]
            self._destroy_single_piece(aux_p)
        
        y = p.y
        for x in range(9):
            aux_p = self.level[x][y]
            self._destroy_single_piece(aux_p)

    # Elimina as 24 peças em volta [FEITO]
    def _special_double_wrapped(self, p):
        # print("Especial: Goma Dupla!")

        if p is None:
            return

        # Faz igual a normal, mas com um tamanho maior
        self._special_wrapped(p, size=2)

    # Destroi todas as peças do campo [FEITO]
    def _special_double_bomb(self):
        # print("Especial: Bomba Dupla!")

        # Destroi todas as peças do campo
        for x in range(9):
            for y in range(9):
                p = self.level[x][y]
                self._destroy_single_piece(p)

    # Elimina 3 linhas e 3 colunas [FEITO]
    def _special_stripped_wrapped(self, p, size=2):
        # print("Especial: Listrada + Goma")
        
        if p is None:
            return

        # Retorna os intervalos
        x, y, end_x, end_y = self._get_wrapped_size(p, size)

        # Percorre a diagonal, deletando linha e coluna
        i = 0
        while i < 3:
            if end_x <= 8 and end_y <= 8:
                aux_p = self.level[x+i][y+i]
                self._special_double_stripped(aux_p)
            else:
                break
            i += 1

    # Transforma todas as peças do mesmo tipo em listradas e ativa elas [FEITO]
    def _special_stripped_bomb(self, p):
        # print("Especial: Listrada + Bomba")

        if p is None:
            return

        # Percorre todas as peças
        for x in range(9):
            for y in range(9):
                aux_p = self.level[x][y]

                # Se for do mesmo tipo, ativa elas como listradas
                if self._can_destroy(aux_p) and aux_p.type == p.type:
                    self._special_stripped(aux_p)

    # Transforma todas as peças do mesmo tipo em gomas, e ativa elas [FEITO]
    def _special_wrapped_bomb(self, p):
        # print("Especial: Goma + Bomba")

        if p is None:
            return

        # Percorre todas as peças
        for x in range(9):
            for y in range(9):
                aux_p = self.level[x][y]

                # Se for do mesmo tipo, ativa elas como listradas
                if self._can_destroy(aux_p) and aux_p.type == p.type:
                    self._special_wrapped(aux_p)

    # elimina uma linha ou uma coluna inteira, aleatoriamente [FEITO]
    def _special_stripped(self, p):
        # print("Especial: Listrada!")

        if p is None:
            return

        # Decide a opção do movimento
        option = random.choice([True, False])

        # Se for True, é Linha
        if option:
            y = p.y

            # Percorre toda a linha
            for x in range(9):
                aux_p = self.level[x][y]
                # if self._can_destroy(aux_p):
                #     self._eliminate_piece(aux_p)
                self._destroy_single_piece(aux_p)

        # Se for False, é Coluna
        else:
            x = p.x

            # Percorre toda a coluna
            for y in range(9):
                aux_p = self.level[x][y]
                if self._can_destroy(aux_p):
                    self._eliminate_piece(aux_p)
                #self._destroy_single_piece(aux_p)

    # elimina as 8 peças a volta dela [FEITO]
    def _special_wrapped(self, p, size=1):
        # print("Especial: Goma!")

        if p is None:
            return

        #self._eliminate_piece(p)
        x, y, end_x, end_y = self._get_wrapped_size(p, size)
        
        # Percorre toda a área
        for i in range(x, end_x):
            for j in range(y, end_y):
                aux_p = self.level[i][j]
                # if self._can_destroy(aux_p):
                #     self._eliminate_piece(aux_p)
                self._destroy_single_piece(aux_p)

    # Retorna os intervalos do tipo goma [FEITO]
    def _get_wrapped_size(self, p, size):
        # Pega as posições anteriores 
        x = p.x - size
        y = p.y - size

        # Se passou das margens
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        # Pega as posições finais
        end_x = p.x + size + 1
        end_y = p.y + size + 1

        # Se passou das margens
        if end_x > 8:
            end_x = 8
        if end_y > 8:
            end_y = 8
        
        return x, y, end_x, end_y

    # elimina todas as peças de mesma cor do campo. [FEITO]
    def _special_bomb(self, p):

        t = None
        # Se a peça for None, decide um tipo aleatório
        if p is None:
            t = random.randint(0,self.types -1)
        else:
            t = p.type

        # print("Especial: Bomba com o tipo", t)

        # Percorre todas as posições
        for x in range(9):
            for y in range(9):
                aux_p = self.level[x][y]
                
                # Se a peça pode ser destruida
                if self._can_destroy(aux_p) and aux_p.type == t:
                    self._destroy_single_piece(aux_p)

    # Destroi uma unica peça, referente ao seu tipo [FEITO]
    def _destroy_single_piece(self, p):

        # Se não tiver peça, pula pra próxima
        if p is None:
            return 

        # Se for peça especial, ativa ela
        if self._is_special(p):
            return self._special_type(p)
        
        # Se não for Bloqueio ou objetivo, exclui
        elif self._can_destroy(p):
            # Destroi a peça para não ter efeito duplo
            return self._eliminate_piece(p)

    # Decide qual o tipo da peça e ativa seu poder [FEITO]
    def _special_type(self, p):
        
        # Elimina a peça
        self._eliminate_piece(p)

        if type(p) is None:
            return
        elif type(p) is piece.Stripped:
            return self._special_stripped(p)
        elif type(p) is piece.Wrapped:
            return self._special_wrapped(p)
        elif type(p) is piece.Bomb:
            return self._special_bomb(None)

    # Verifica se é uma peça especial
    def _is_special(self, p):

        # Se for None, não é especial
        if p is None:
            return False
        
        # Se for Listrada, é especial
        elif type(p) is piece.Stripped:
            return True
        
        # Se for Goma, é especial
        elif type(p) is piece.Wrapped:
            return True

        # Se for Bomba, é especial
        elif type(p) is piece.Bomb:
            return True
        
        # Qualquer caso diferente é falso
        return False

    # Usado para conferir se uma peça pode ser destruida
    def _can_destroy(self, p):

        # É None, não é uma peça
        if p is None:
            return False
        # Se for uma simples peça, não pode
        elif type(p) is piece.Piece:
            return False
        # Um bloqueio não pode ser destruido
        elif type(p) is piece.Block:
            return False
        elif type(p) is piece.Objective:
            return False
        
        # O resto pode ser destruido
        return True

    # Método para todas as combinações especiais [FEITO]
    def _special_comb(self, p1, p2):
        
        # Caso um dos dois seja None
        if p1 is None or p2 is None:
            return False

        # Elimina as peças do campo pra não ter efeito duplo
        if self._is_special(p1) and self._is_special(p2):
            self._eliminate_piece(p1)
            self._eliminate_piece(p2)
        elif type(p1) is piece.Bomb:
            self._eliminate_piece(p1)
        elif type(p2) is piece.Bomb:
            self._eliminate_piece(p2)

        # Caso os 2 tipos sejam iguais
        if type(p1) is type(p2):

            # Se for tipo Listrado:
            if type(p1) is piece.Stripped:

                # Elimina a linha e a coluna ao mesmo tempo
                self._special_double_stripped(p1)
                return True
            
            # Se for tipo Goma
            elif type(p1) is piece.Wrapped:

                # Elimina as 24 peças em volta
                self._special_double_wrapped(p1)
                return True
            
            # Se for tipo Bomba
            elif type(p1) is piece.Bomb:

                # Destroi todas as peças do campo
                self._special_double_bomb()
                return True
        
        # Os dois tipos são diferentes
        else:

            # Se a primeira peça for Listrada
            if type(p1) is piece.Stripped:
                
                # Se a segunda peça for Goma
                if type(p2) is piece.Wrapped:

                    # Elimina 3 linhas e 3 colunas
                    self._special_stripped_wrapped(p1)
                    return True

                # Se a segunda peça for Bomba
                elif type(p2) is piece.Bomb:

                    # Transforma todas as peças do mesmo tipo
                    # em listradas e ativa elas
                    self._special_stripped_bomb(p1)
                    return True
            
            # Se a primeira peça for Goma
            elif type(p1) is piece.Wrapped:
                
                # Se a segunda peça for Listrada
                if type(p2) is piece.Stripped:

                    # Elimina 3 linhas e 3 colunas
                    self._special_stripped_wrapped(p1)
                    return True
                
                # Se a segunda peça for Bomba
                elif type(p2) is piece.Bomb:

                    # Transforma todas as peças do mesmo tipo
                    # em gomas, e ativa elas
                    self._special_wrapped_bomb(p1)
                    return True
            
            # Se a primeira peça for Bomba
            elif type(p1) is piece.Bomb:
                
                # Se a segunda peça for Listrada
                if type(p2) is piece.Stripped:

                    # Transforma todas as peças do mesmo tipo
                    # em listradas e ativa elas
                    self._special_stripped_bomb(p2)
                    return True
                
                # Se a segunda peça for Goma
                elif type(p2) is piece.Wrapped:

                    # Transforma todas as peças do mesmo tipo
                    # em gomas, e ativa elas
                    self._special_wrapped_bomb(p2)
                    return True
        
        # Se alguma das peças for Bomba neste momento, a outra é 
        # uma peça simples
        if (type(p1) is piece.Bomb) or (type(p2) is piece.Bomb):

            # Ativa o poder da Peça BOMBA na peça Simples
            if p1.type != -1:
                self._special_bomb(p1)
            else:
                self._special_bomb(p2)
            
            return True

        # Não tem combinações de peças especiais
        return False
    
    # Método para todas as combinações 
    def _check_move(self, p1, p2, moves):
        
        # Se algum dos dois for none
        if p1 is None or p2 is None:
            return

        # Se as duas peças forem especiais, a jogada é válida
        if self._is_special(p1) and self._is_special(p2):
            moves.append((p1,p2))
            return
        
        # Se uma das peças for bomba, a jogada é válida
        if type(p1) is piece.Bomb or type(p2) is piece.Bomb:
            moves.append((p1,p2))
            return
        
        # Troca as peças de posição
        self._move_pieces(p1, p2)
        
        # Se gerou movimentos, a jogada é válida
        if self._check_board(self.level):
            moves.append((p1,p2))
        
        # Retorna as peças pra posição originais
        self._move_pieces(p1, p2)

    # Imprime os movimentos possiveis
    def _print_possible_moves(self, moves):
        print("[")
        for move in moves:
            print("(%d,%d) -> " % (move[0].x, move[0].y), end="")
            print("(%d,%d)" % (move[1].x, move[1].y))
        print("]")

    # Retorna uma lista de tuplas com todos os movimentos possiveis
    def possible_moves(self):

        # Se o jogo já está em estado terminal, retorna None
        if self.is_finished():
            return None

        moves = []
        # Percorre todas as possibilidades
        for x in range(9):
            for y in range(9):
                p1 = self.level[x][y]

                # Se essa peça não pode ser destruida, pula pra próxima
                if not self._can_destroy(p1):
                    continue
                
                # Combinação Horizontal
                if x + 1 < 9:
                    p2 = self.level[x+1][y]
                    if self._can_destroy(p2):
                        self._check_move(p1, p2, moves)

                # Combinação Vertical
                if y + 1 < 9:
                    p2 = self.level[x][y+1]
                    if self._can_destroy(p2):
                        self._check_move(p1, p2, moves)

        return moves
