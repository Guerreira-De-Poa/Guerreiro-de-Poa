import pygame
from game import *
import os
import sys
import cv2
import numpy as np

pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'assets'))
sys.path.append(pasta_pai)

fundo_menu = pygame.image.load(os.path.join(pasta_pai, 'fundo_menu.png'))
fundo_creditos = pygame.image.load(os.path.join(pasta_pai, 'fundo_creditos.png'))
fundo_historia = pygame.image.load(os.path.join(pasta_pai, 'fundo_historia.png'))

class VideoBackground:
    def __init__(self, video_path, size):
        self.cap = cv2.VideoCapture(video_path)
        self.size = size  # (width, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            # Reinicia o vídeo ao chegar no final        
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        # Converte de BGR para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Redimensiona para o tamanho da tela
        frame = cv2.resize(frame, self.size)
        # Opcional: ajuste de rotação se necessário (alguns vídeos podem precisar)
        # frame = np.rot90(frame)
        # Cria uma surface do Pygame a partir do frame
        surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        return surface
    
class Menu():
    def __init__(self, game): # chamamos a classe do game.py
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/3.8, self.game.DISPLAY_H/1.7
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20) # o cursor que vamos usar pra navegar no menu
        self.offset = -150 # ir a esquerda do texto, vai ser mais simples colocando em ação

    def draw_cursor(self): # cursor
        self.game.draw_text('*', 25, self.cursor_rect.x, self.cursor_rect.y )

    def blit_screen(self): # atualiza a tela
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

    

def tocar_musica(): # função pra tocar a música
        
        som = pygame.mixer.Sound("musicas/altera-opcao.mp3") # ABAIXO SÃO OS 3 PARANAUE PARA COMEÇAR A MUSICA
        pygame.mixer.stop() # para o som anterior
        som.set_volume(1)
        som.play(1, 10000, 1000)  
         # 50% do volume máximo

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 90
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        # Cria o background de vídeo com o tamanho da tela
        self.video_bg = VideoBackground(os.path.join(pasta_pai, 'fundo_menu_animado.mp4'), (self.game.DISPLAY_W, self.game.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # Pega o frame atual do vídeo e desenha como fundo
            frame_surface = self.video_bg.get_frame()
            self.game.display.blit(frame_surface, (0, 0))
            # Desenha os textos do menu
            self.game.draw_text('START', 35, self.startx, self.starty)
            self.game.draw_text('OPTIONS', 35, self.optionsx, self.optionsy)
            self.game.draw_text('CREDITS', 35, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
    def move_cursor(self):
        if self.game.DOWN_KEY: # VAI ALTERANDO A POSIÇÃO
            if self.state == 'Start':
                tocar_musica()
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                tocar_musica()
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                tocar_musica()
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start' 

        if self.game.UP_KEY: # VAI ALTERANDO A POSIÇÃO
            if self.state == 'Start':
                tocar_musica()
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                tocar_musica()
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                tocar_musica()
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start' 

    def check_input(self): # CHECANDO QUANDO CLICA EM UMA OPÇÃO
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True

            elif self.state == 'Options':
                self.game.curr_menu = self.game.options

            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits

            self.run_display = False # para o menu sumir

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 30
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.video_bg = VideoBackground(os.path.join(pasta_pai, "fundo_menu_animado.mp4"), (self.game.DISPLAY_W, self.game.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            frame_surface = self.video_bg.get_frame()
            self.game.display.blit(frame_surface, (0, 0))
            # self.game.draw_text('OPTIONS', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('VOLUME', 35, self.volx, self.voly)
            # self.game.draw_text('CONTROLS', 35, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        # elif self.game.UP_KEY or self.game.DOWN_KEY:
        #     if self.state == 'Volume':
        #         self.state = 'Controls'
        #         self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                
        #     elif self.state == 'Controls':
        #         self.state = 'Volume'
        #         self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass # daqui cria o menu de volume e controles
            # if self.state == 'Volume':
            #     pass
            # elif self.state == 'Controls':
            #     pass
            
class CreditsMenu(Menu):
    def __init__(self, game): # pelo que eu entendi, essa "função dunder, com dois '_'" é pra chamar funções, variaveis, que estão em outras artes, como a de créditos não tem muita coisa, só precisamos dela!
        Menu.__init__(self, game)
        self.video_bg = VideoBackground(os.path.join(pasta_pai, 'fundo_creditos.mp4'), (self.game.DISPLAY_W, self.game.DISPLAY_H))
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY or self.game.START_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            frame_surface = self.video_bg.get_frame()
            self.game.display.blit(frame_surface, (0, 0))
            self.blit_screen()
    
