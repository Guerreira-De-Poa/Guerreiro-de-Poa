import pygame
from menu import *
import os
import sys

pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'assets'))
sys.path.append(pasta_pai)
from mapa_main.main_mapa import inicio as inicio_real
fundo_historia = pygame.image.load(os.path.join(pasta_pai, 'fundo_historia (1).png'))
    
class Game():
    def __init__(self):
        pygame.init() # acessar as "ferramentas" pyggame
        self.running, self.playing = True, False # running -> jogo roda, uma verdade, mesmo que voce não faça nada '-' | playing -> ação do player!
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False # controles pro menu, pra organizar as açoes
        self.DISPLAY_W, self.DISPLAY_H = 1200, 800 # Largura e altura da tela uai
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H)) # A TELA EM SI, só não conhecia este surface ->
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H)) # a janela...
        self.font_file = os.path.join(pasta_pai, '8-BIT WONDER.TTF') # caso instalarmos, usa o nome do arquivo, tipo 'fonte.tif'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255) # cores uai (r,g,b)
        self.main_menu = MainMenu(self) # menu principal
        self.options = OptionsMenu(self) # menu de opções
        self.credits = CreditsMenu(self) # menu de créditos
        self.curr_menu = self.main_menu 



    def game_loop(self): # loop do jogo em si
        while self.playing: # quando estiver jogando
            self.check_events() # analisa o seventos
            if self.BACK_KEY:
                self.playing = False
                break
                
            if self.START_KEY: # quando clicamos em começar
                self.playing = False # quebramos o loop, não o jogo em si, tipo, ainda roda, mas o loop do menu nãop

                ###
                # PARAR A MUSICA
                ###
                pygame.mixer.music.stop()
                print("NSDNADKSLANDLKSAJDKLSAJDLK")
                inicio_real()
                

            self.display.blit(fundo_historia, (0,0)) # ATUALIZAMOS A TELA, pra que não fica tudo junto na mesma tela
            self.window.blit(self.display, (0,0)) # manda o display, MANDA PRA WINDOW (0,0) É PRA ALINHA DISPLAY COM WINDOW
            pygame.display.update() # atrualiza a window (enxergamos)
            self.reset_keys()

    def check_events(self): # checar eventos
        for event in pygame.event.get(): # analisamos o que o user faz
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False # desligamos tudo
                self.curr_menu.run_display = False # DESLIGA O MENU
            if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada # gpt fez desta maneira, funcionou melhor
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True


            # RELEMBRANDO QUE ESTAS SÃO AS TECLAS LA DE CIMA

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False # pra deixar tudo falso quando o jogador parar de segurar a tecla

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_file,size) #V FONTE
        text_surface = font.render(text, True, self.WHITE) # TEXTO EM SI
        text_rect = text_surface.get_rect() 
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
