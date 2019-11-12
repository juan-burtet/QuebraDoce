import sys, pygame
pygame.init()

# Inicialização
size = width, height = 800, 600
speed = [2, 2]
black = 0, 0, 0

# Tela
screen = pygame.display.set_mode(size)

# Inicialização da imagem da Bola
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

# Loop de Eventos
while 1:
    
    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Movimentação da bola
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    # Display da tela
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()