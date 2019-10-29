import piece
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Quebra Doce - Match Three Game')
pygame.mouse.set_visible(1)

x = piece.Simple(1,1,6)

print(x.sprites)