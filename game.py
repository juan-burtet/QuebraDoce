import sys, pygame, time, random
import numpy as np
from pygame.locals import *

# Arquivos próprios
import piece
import board

size = width, height = 800, 600

'''
Conjunto de Cores
'''
BLACK  = (  0,   0,   0)
WHITE  = (245, 245, 245)
GREY   = ( 80,  80,  80)
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


class Game(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.status = 'start' # estado inicial do jogo
        self.frame = 0 # frames do jogo
        self.color = random.choice(PIECE_COLORS) # cor da tela
        self.board = None # Campo do jogo
        self.pick = None # Peça escolhida

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
                    sys.exit()

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
    def _add_nes_text(
        self, 
        string, 
        text_size=60,
        reverse=False,
        centerx=size[0]/2, 
        centery=size[1]/2, 
        left=None,
        right=None,
        top=None,
        bottom=None):
        
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

        # Atualiza com as posições passadas
        if left:
            frontpos.left = left
        
        if right:
            frontpos.right = right
        
        if top:
            frontpos.top = top
        
        if bottom:
            frontpos.bottom = bottom

        # Cria a sombra
        back = font.render(string, 1, colors[1])
        backpos = back.get_rect()
        backpos.right = frontpos.right + plus
        backpos.bottom = frontpos.bottom + plus

        return [back,front], [backpos, frontpos]

    # Inicializa as informações necessárias pro Game_Screen
    def _set_game_screen(self):
        self.status = 'game'
        self.board = board.Board()

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
    def _draw_square(self, background, piece, color=GREY, width=3):

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
        
        # Retorna a peça valida
        return p

    # Imprime toda a informação do jogo na tela
    def _print_game_info(self, background):

        # Caixa onde fica o modo de jogo
        pygame.draw.rect(
            background,
            BLACK,
            (15, 25, 190, 185),
            10
        )

        # Imprime a String: "Modo de Jogo"
        texts, pos = self._add_nes_text(
            "GAME MODE",
            text_size=25,
            reverse=True,
            left=25,
            top=30,
        )
        for t, p in zip(texts,pos):
            background.blit(t,p)
        
        # Imprime o modo do jogo

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
        background.fill(WHITE)

        # Imprime as informações do jogo
        self._print_game_info(background)
        
        # Imprime as peças na tela
        for pieces in self.board.level:
            for p in pieces:
                background.blit(p.image, p.rect)
                background = self._draw_square(background, p)
        
        # Imprime a peça escolhida
        if self.pick is not None:
            self._draw_square(
                background,
                self.pick,
                color=RED,
                width=5)

        # Retorna a tela a ser imprimida
        return background