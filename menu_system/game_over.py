import pygame
import sys
import os

def Game_over(funcao):

    pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'assets'))
    sys.path.append(pasta_pai)

    imagem = pygame.image.load(os.path.join(pasta_pai, 'game_over.png'))
    pygame.init()

    # Configurações da tela
    # Configurações da tela
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo com Mapa e Colisões")

    running = True

    font = pygame.font.Font(os.path.join(pasta_pai,'8bitOperatorPlus8-Regular.ttf'),48)

    text = font.render('x', True,(255,255,255))

    escolha = True

    while running:
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
                        # print("RESTART")
                        running = False
                        funcao()
                    else:
                        # print("GAME OVER")
                        running = False

        screen.fill((50,20,50))

        screen.blit(imagem,(0,0))

        screen.blit(text,(130,text_pos))
        pygame.display.flip()

