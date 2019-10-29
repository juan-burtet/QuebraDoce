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
WHITE  = (255, 255, 255)
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
        self.status = 'start'
        self.frame = 0
        self.color = random.choice(PIECE_COLORS)
        self.board = None

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
            if self.frame >=60:
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
    def _add_nes_text(self, string, x=size[0]/2,
        y=size[1]/2, text_size=60):
        
        plus = 2

        # Inicializa a lista
        texts, pos = [], []
        
        # Inicializa a fonte da frente
        font = pygame.font.Font('assets/fonts/pixel_nes.otf', text_size)

        # Cria o texto Inicial
        front = font.render(string, 1, WHITE)
        frontpos = front.get_rect(centerx=x, centery=y)

        # Cria a sombra
        back = font.render(string, 1, BLACK)
        backpos = back.get_rect()
        backpos.right = frontpos.right + plus
        backpos.bottom = frontpos.bottom + plus

        return [back,front], [backpos, frontpos]

    # Inicializa as informações necessárias pro Game_Screen
    def _set_game_screen(self):
        self.status = 'game'
        self.board = board.Board()

    def _start_screen(self):
        
        # Captura de eventos da tela inicial
        for event in self.events:
            if event.type == MOUSEBUTTONDOWN:
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
                y=size[1]/2 + 40,
                text_size=15)
            background.blit(texts[0], textpos[0])
            background.blit(texts[1], textpos[1])

            # CLICK WITH THE MOUSE!
            if self.frame % 60 <= 30:
                texts, textpos = self._add_nes_text(
                    "CLICK WITH THE MOUSE!",
                    y= size[1] - 30,
                    text_size=20)
                background.blit(texts[0], textpos[0])
                background.blit(texts[1], textpos[1])

        return background
        

    def _game_screen(self):
        
        for event in self.events:
            if event.type == MOUSEBUTTONDOWN:
                self.status = 'start'


        # Create The Backgound
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(WHITE)

        pieces = self.board.get_board()

        for image, rect in pieces:
            background.blit(image, rect)

        return background



        