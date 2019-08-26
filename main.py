import pygame
import numpy as np
from pygame.locals import *
import board

fase = board.Board()
fase.set_values()
#fase.print_board()

game = Game()
game.play()

print("Game Closed!")