import sys, pygame, time, random
import numpy as np
from pygame.locals import *

# Arquivos próprios
import piece
import board
import game_utils

size = width, height = 800, 600

'''
Conjunto de Cores
'''
BLACK  = (  0,   0,   0)
WHITE  = (245, 245, 245)
GREY   = (180, 180, 180)
RED    = (250,  24,  22)
ORANGE = (250, 162,   8)
YELLOW = (244, 235,   5)
GREEN  = (  4, 206,   6)
BLUE   = (  5,  60, 242)
PURPLE = (176,   4, 214)

'''
Cores das peças
'''
PIECE_COLORS = [
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    PURPLE
]

'''
Cores dos modos
'''
MODE_COLORS = {}
MODE_COLORS['POINTS'] = ORANGE
MODE_COLORS['BLOCKS'] = BLUE
MODE_COLORS['OBJECTIVE'] = GREEN
MODE_COLORS['MIX'] = PURPLE

class Game(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.status = 'start' # estado inicial do jogo
        self.frame = 0 # frames do jogo
        self.color = random.choice(PIECE_COLORS) # cor da tela
        self.board = None # Campo do jogo
        self.pick = None # Peça escolhida
        self.objective_image = None # Imagem do objeto

    def _pygame_init(self):
        # Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Quebra Doce - Match Three Game')
        pygame.mouse.set_visible(1)

    def play(self):
        
        # Inicializa o pygame e a interface
        self._pygame_init()

        # Prepare Game Objects
        clock = pygame.time.Clock()
    
        # Main Loop
        going = True
        while going:

            # Garante os 60 frames do jogo
            clock.tick(60)
            
            # Informação do frame atual
            self.frame += 1
            if self.frame > 60:
                self.color = random.choice(PIECE_COLORS)
                self.frame = 0

            # Captura eventos
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT: 
                    going = False

            if self.status == 'start':
                background = self._start_screen()
            elif self.status == 'game':
                background = self._game_screen()

            # Draw Everything
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

        pygame.quit()

        # Game Over
    
    # Adiciona um texto com a fonte de NES na tela
    def _add_nes_text(self, string, text_size=60, reverse=False, 
            centerx=size[0]/2, centery=size[1]/2, left=None, 
            right=None, top=None, bottom=None):
        
        # Ordem das cores
        colors = [WHITE, BLACK]
        if reverse:
            colors = list(reversed(colors))

        # Espaço de sombra
        plus = 2

        # Inicializa a lista
        texts, pos = [], []
        
        # Inicializa a fonte da frente
        font_path = 'assets/fonts/pixel_nes.otf'
        font = pygame.font.Font(font_path, text_size)

        # Cria o texto Inicial
        front = font.render(string, 1, colors[0])
        frontpos = front.get_rect(centerx=centerx, centery=centery)

        # Se tiver posição esquerda, atualiza
        if left is not None:
            frontpos.left = left
        
        # Se tiver posição direita, atualiza
        if right is not None:
            frontpos.right = right
        
        # Se tiver posição do topo, atualiza
        if top is not None:
            frontpos.top = top
        
        # Se tiver posição de baixo, atualiza
        if bottom is not None:
            frontpos.bottom = bottom

        # Cria a sombra
        back = font.render(string, 1, colors[1])
        backpos = back.get_rect()
        backpos.right = frontpos.right + plus
        backpos.bottom = frontpos.bottom + plus

        return [back,front], [backpos, frontpos]

    # Inicializa a imagem do icone
    def _get_objective_image(self):
        
        if self.objective_image is None:
            self.objective_image = game_utils.load_image(
                "assets/sprite/pieces/objective/0.png",
                size=(35,35)
            )

    # Inicializa as informações necessárias pro Game_Screen
    def _set_game_screen(self):
        self.status = 'game'
        #self.board = board.Board("levels/example.csv")
        self.board = board.Board()
        self._get_objective_image()
        self.blocks = self.board.blocks
        self.objectives = self.board.canes

    # Trabalha todas as operações da tela inicial
    def _start_screen(self):
        
        # Captura de eventos da tela inicial
        for event in self.events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self._set_game_screen()

        # Cria o plano de fundo
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.color)

        # Coloca as letras na tela com sombreamento
        if pygame.font:
            
            # QUEBRA DOCE
            texts, textpos = self._add_nes_text("QUEBRA DOCE")
            background.blit(texts[0], textpos[0])
            background.blit(texts[1], textpos[1])

            # - A SIMPLE MATCH THREE GAME -
            texts, textpos = self._add_nes_text(
                "- A SIMPLE MATCH THREE GAME -",
                centery=size[1]/2 + 40,
                text_size=15)
            background.blit(texts[0], textpos[0])
            background.blit(texts[1], textpos[1])

            # CLICK WITH THE MOUSE!
            if self.frame % 60 <= 30:
                texts, textpos = self._add_nes_text(
                    "CLICK WITH THE MOUSE!",
                    centery= size[1] - 30,
                    text_size=20)
                background.blit(texts[0], textpos[0])
                background.blit(texts[1], textpos[1])

        return background

    # Desenha um quadrado em volta da posição da peça
    def _draw_square(self, background, piece, color=BLACK, width=3):

        # Pega o tamanho do quadrado
        l = piece.rect.left -width
        t = piece.rect.top -width
        w = piece.rect.width +width
        h = piece.rect.height +width

        # Desenha o quadrado
        pygame.draw.rect(
            background,
            color,
            (l, t, w, h),
            width)
        
        return background

    # Checa se a peça selecionada é válida
    def _check_picked_piece(self, p):

        # Se clicou em um bloco, retorna nada
        if type(p) is piece.Block or type(p) is piece.Objective:
            return None

        # Se não tiver nenhuma escolhida,
        # retorna a tocada
        if self.pick is None:
                return p
        
        # Pega a posição das duas peças
        x = abs(self.pick.x - p.x)
        y = abs(self.pick.y - p.y)

        # Se a distância das duas for maior,
        # posição invalida
        if x > 1 or y > 1:
            return None
        
        # Pega a possibilidade de clicar na mesma ou
        # clicar na diagonal
        if x == y:
            return None
        
        # Testa o movimento
        self.board.test_move(p, self.pick)

        # Retorna nenhuma peça seleciona
        return None

    # Retorna a quantidade de pontos do jogo
    def _get_points(self):

        value = str(self.board.points)
        value = ''.join(reversed(value))

        size = len(value)
        for i in range(size, 9):
            value += '0'

        number = ''
        for i, c in enumerate(value):
            number += c
            if i % 3 == 2:
                number += '.'

        if number[-1] == '.':
            number = number[:-1]

        number = ''.join(reversed(number))
        return number

    # Imprime o modo de jogo na tela
    def _print_game_mode(self, background):
        
        # Caixa onde fica o modo de jogo
        pygame.draw.rect(
            background,
            WHITE,
            (15, 25, 190, 90),
        )
        
        # Caixa onde fica o modo de jogo
        pygame.draw.rect(
            background,
            BLACK,
            (15, 25, 190, 90),
            10
        )

        # Imprime a String: "GAME MODE"
        texts, pos = self._add_nes_text(
            "GAME MODE",
            text_size=25,
            reverse=True,
            left=25,
            top=30,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        # Desenha uma linha que separa as strings
        pygame.draw.line(
            background, 
            BLACK, 
            (30, 60), 
            (190, 60), 
            2
        )
        
        # Imprime o modo do jogo
        texts, pos = self._add_nes_text(
            self.board.mode,
            text_size=25,
            reverse=True,
            centerx=pos[1].centerx,
            top=pos[1].bottom + 10,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)
        
        # Desenha um quadrado em volta do modo do jogo
        pygame.draw.rect(
            background,
            MODE_COLORS[self.board.mode],
            (pos[1].left - 3,
            pos[1].top + 5, 
            pos[1].width + 5, 
            pos[1].height - 7),
            3
        )

    # Imprime a quantidade de pontos na tela
    def _print_game_points(self, background):

        # Pinta o fundo da caixa
        rect = pygame.draw.rect(
            background,
            WHITE,
            (10, 130, 200, 90),
        )

        # Caixa onde fica a pontuação
        rect = pygame.draw.rect(
            background,
            BLACK,
            (10, 130, 200, 90),
            10
        )

        # Imprime a String: "SCORE"
        texts, pos = self._add_nes_text(
            "SCORE",
            text_size=40,
            reverse=True,
            # left=25,
            centerx = rect.centerx,
            top=130,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        # Desenha uma linha que separa as strings
        pygame.draw.line(
            background, 
            BLACK, 
            (30, 175), 
            (190, 175), 
            2
        )

        # Imprime a quantidade de pontos
        texts, pos = self._add_nes_text(
            self._get_points(),
            text_size=24,
            reverse=True,
            right=pos[1].right + 15,
            top=pos[1].bottom,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

    # Imprime a quantidade de movimentos restantes no jogo
    def _print_game_moves(self, background):
        
        # Pinta o fundo do campo
        rect = pygame.draw.rect(
            background,
            WHITE,
            (15, 235, 190, 105),
        )

        # Faz o campo de movimentos
        rect = pygame.draw.rect(
            background,
            BLACK,
            (15, 235, 190, 105),
            10
        )

        # Imprime a String: "MOVES"
        texts, pos = self._add_nes_text(
            "MOVES",
            text_size=40,
            reverse=True,
            centerx=rect.centerx+2,
            top=rect.top,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        # Desenha uma linha para separar as strings
        pygame.draw.line(
            background, 
            BLACK, 
            (pos[1].left - 2, pos[1].bottom), 
            (pos[1].right - 5, pos[1].bottom), 
            2
        )

        # Imprime a quantidade de movimentos
        texts, pos = self._add_nes_text(
            str(self.board.moves),
            text_size=50,
            reverse=True,
            centerx=pos[1].centerx,
            centery=pos[1].centery + 47,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        pass
    
    # Retorna a quantidade dos objetivos especificos
    def _get_objectives_string(self, a, b):
        string = ""

        string += str(a - b)
        string += "/"
        string += str(a)

        return string

    # Retorna a quantidade pontos necessários para ganhar
    def _get_points_string(self):

        points = self.board.w_points
        m = int(points/1000000)
        
        if m > 0:
            return ("%dM" % m)
        
        k = int(points/1000)
        if k > 0:
            return ("%dK" % k)
        
        return str(points)

    # Imprime os objetivos da partida
    def _print_game_objectives(self, background):

        # Pinta o fundo do campo de objetivos
        pygame.draw.rect(
            background,
            WHITE,
            (15, 355, 190, 225),
        )

        # Faz o campo de objetivos
        rect = pygame.draw.rect(
            background,
            BLACK,
            (15, 355, 190, 225),
            10
        )

        # Imprime a String: "OBJECTIVES"
        texts, pos = self._add_nes_text(
            "GOALS",
            text_size=40,
            reverse=True,
            centerx=rect.centerx+2,
            top=rect.top,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        # Desenha uma linha para separar as strings
        pygame.draw.line(
            background, 
            BLACK, 
            (pos[1].left - 2, pos[1].bottom), 
            (pos[1].right - 5, pos[1].bottom), 
            2
        )

        ''' Quantidade de Pontos Necessários. '''

        # Fundo do campo onde fica os pontos
        pygame.draw.rect(
            background,
            GREY,
            (pos[1].left-5, pos[1].bottom +10,
            155, 40),
        )

        # Contorno do campo onde fica os pontos
        rect_b = pygame.draw.rect(
            background,
            BLACK,
            (pos[1].left-5, pos[1].bottom +10,
            155, 40),
            3
        )

        # quantidade de pontos necessário
        texts, pos = self._add_nes_text(
            "PTS",
            text_size=30,
            reverse=True,
            left=pos[1].left,
            top=pos[1].bottom +10,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)
        
        # quantidade de pontos necessário
        texts_aux, pos_aux = self._add_nes_text(
            self._get_points_string(),
            text_size=22,
            reverse=True,
            centery=pos[1].centery,
            centerx=pos[1].right + 40,
        )
        for t, p in zip(texts_aux, pos_aux):
            background.blit(t,p)
        
        if self.board.points >= self.board.w_points:
            self._draw_complete(background, rect_b)
        
        ''' Quantidade de Objetivos Necessário. '''

        # Fundo do campo onde fica os pontos
        pygame.draw.rect(
            background,
            GREY,
            (pos[1].left-5, pos[1].bottom +10,
            155, 50),
        )

        # Contorno do campo onde fica os pontos
        rect_b = pygame.draw.rect(
            background,
            BLACK,
            (pos[1].left-5, pos[1].bottom +10,
            155, 50),
            3
        )

        # Quantidade de objetivos necessário
        image = self.objective_image[0]
        rect = self.objective_image[1]
        rect.left = pos[1].left +10
        rect.top = pos[1].bottom +18
        background.blit(image, rect)

        # quantidade de objetivos necessário
        texts_aux, pos_aux = self._add_nes_text(
            self._get_objectives_string(self.objectives, self.board.canes),
            text_size=22,
            reverse=True,
            centery=rect.centery,
            centerx=rect.right + 55,
        )
        for t, p in zip(texts_aux, pos_aux):
            background.blit(t,p)

        if self.board.canes == 0:
            self._draw_complete(background, rect_b)

        ''' Quantidade de Bloqueios Necessário '''

        # Fundo do campo onde fica os bloqueios
        pygame.draw.rect(
            background,
            GREY,
            (pos[1].left-5, rect.bottom +15,
            155, 50),
        )

        # Contorno do campo onde fica os bloqueios
        rect_b = pygame.draw.rect(
            background,
            BLACK,
            (pos[1].left-5, rect.bottom +15,
            155, 50),
            3
        )

        # Desenha a borda do bloqueio
        rect = pygame.draw.rect(
            background,
            BLUE,
            (rect.left, rect.bottom +23,
            rect.width, rect.height),
            5
        )

        # Desenha o quadrado transparente
        s = pygame.Surface(rect.size)
        s.set_alpha(128)
        s.fill(BLUE)
        background.blit(s, (rect.left, rect.top))

        # quantidade de bloqueios necessário
        texts, pos = self._add_nes_text(
            self._get_objectives_string(self.blocks, self.board.blocks),
            text_size=22,
            reverse=True,
            centery=rect.centery,
            centerx=rect.right + 55,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)

        if self.board.blocks == 0:
            self._draw_complete(background, rect_b)

    # Se já tiver completo os objetivos, pinta
    def _draw_complete(self, background, rect_b):

            pygame.draw.line(
                background, 
                RED, 
                rect_b.topright, 
                rect_b.bottomleft, 
                5
            )

            pygame.draw.line(
                background, 
                RED, 
                rect_b.topleft, 
                rect_b.bottomright, 
                5
            )

    # Imprime toda a informação do jogo na tela
    def _print_game_info(self, background):

        self._print_game_mode(background)
        self._print_game_points(background)
        self._print_game_moves(background)
        self._print_game_objectives(background)

    # Trabalha todas as operação da tela do jogo    
    def _game_screen(self):

        # Eventos possiveis da tela do jogo
        for event in self.events:
            
            # Apertou com o mouse (botão esquerdo)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                
                # Posição do mouse
                pos = pygame.mouse.get_pos()

                # Percorre por todas as peças no campo
                find = False
                for pieces in self.board.level:
                    for p in pieces:
                        
                        # Verifica se houve colisão
                        if p.rect.collidepoint(pos):
                            self.pick = self._check_picked_piece(p) 
                            find = True
                            break
                    
                    # Se encontrou, sai do loop
                    if find:
                        break
                
                # Se não encontrou, tira a peça
                if not find:
                    self.pick = None

        # Cria o background da fase
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(MODE_COLORS[self.board.mode])

        # Imprime as informações do jogo
        self._print_game_info(background)
        
        # Adiciona a cor branca ao fundo
        # Imprime o contorno
        pygame.draw.rect(
            background,
            WHITE,
            (self.board.level[0][0].rect.left -5,
            self.board.level[0][0].rect.top -5,
            self.board.level[8][8].rect.right -215,
            self.board.level[8][8].rect.bottom -15),
        )

        # Imprime as peças na tela
        for pieces in self.board.level:
            for p in pieces:
                background.blit(p.image, p.rect)
                background = self._draw_square(background, p)
        
        # Imprime o contorno
        pygame.draw.rect(
            background,
            BLACK,
            (self.board.level[0][0].rect.left -5,
            self.board.level[0][0].rect.top -5,
            self.board.level[8][8].rect.right -215,
            self.board.level[8][8].rect.bottom -15),
            10
        )
        
        # Imprime a peça escolhida
        if self.pick is not None:
            self._draw_square(
                background,
                self.pick,
                color=RED,
                width=5)

        # Retorna a tela a ser imprimida
        return background