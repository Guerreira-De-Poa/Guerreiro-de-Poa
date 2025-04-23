import pygame
import sys
import os

def game_over():

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    imagem = pygame.image.load('game_over.png')
    pygame.init()

    # Configurações da tela
    # Configurações da tela
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo com Mapa e Colisões")

    running = True

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf',48)

    text = font.render('x', True,(255,255,255))

    escolha = True

    while True:
        if escolha == True:
            text_pos = 472
        elif escolha == False:
            text_pos = 534

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    escolha = not escolha
                elif event.key == pygame.K_UP:
                    escolha = not escolha
                elif event.key == pygame.K_RETURN:
                    if escolha == True:
                        print("RESTART")
                    else:
                        print("GAME OVER")

                

        screen.fill((50,20,50))

        screen.blit(imagem,(0,0))

        screen.blit(text,(130,text_pos))
        pygame.display.flip()

game_over()