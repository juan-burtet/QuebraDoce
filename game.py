import sys, pygame
import numpy as np
from pygame.locals import *

import piece
import board

size = width, height = 800, 600

'''
COLORS
'''
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

class Game(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.status = 'start'

    def _pygame_init(self):
        # Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Quebra Doce - Match Three Game')
        pygame.mouse.set_visible(1)

    def play(self):
        
        # Inicializa o pygame
        self._pygame_init()

        # Create The Backgound
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(BLACK)

        # Put Text On The Background, Centered
        if pygame.font:
            font = pygame.font.Font('assets/fonts/pixel_nes.otf', 50)
            text = font.render("Quebra Doce", 1, WHITE)
            textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/2)
            background.blit(text, textpos)

        # Display The Background
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        # Prepare Game Objects
        clock = pygame.time.Clock()

        # Main Loop
        going = True
        while going:
            clock.tick(60)

            # Captura eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


            # Está no Estado de Inicio
            if self.status == 'start':
                self._start_screen()



            # Draw Everything
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

        pygame.quit()

        # Game Over
    
    def _start_screen(self):
        
        # Eventos na tela inicial
        for event in pygame.event.get():
            if event.type == MOUSEBUTTOMDOWN:
                self.status == 'game'
        
        pass




        