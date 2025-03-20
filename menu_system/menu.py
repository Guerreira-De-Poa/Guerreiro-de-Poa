import pygame
fundo_menu = pygame.image.load('fundo_menu.png')
fundo_creditos = pygame.image.load('fundo_creditos.png')
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


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game) # significa: um argumento que envia as variaveis da classe game, em __init__
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30 # olha que coisa linda, criou as posições de cada opção do menu
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 90
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) # alinha

    def display_menu(self):
        self.run_display = True
        while self.run_display: # mostrar o menu
            self.game.check_events()
            self.check_input() # checaimput
            self.game.display.blit(fundo_menu, (0,0)) # fundo
            self.game.draw_text('START', 35, self.startx, self.starty) # adicionamos os textos, que coisa linda
            self.game.draw_text('OPTIONS', 35, self.optionsx, self.optionsy)
            self.game.draw_text('CREDITS', 35, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen() # mostra na tela

    def move_cursor(self):
        if self.game.DOWN_KEY: # VAI ALTERANDO A POSIÇÃO
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start' 

        if self.game.UP_KEY: # VAI ALTERANDO A POSIÇÃO
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
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

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(fundo_creditos, (0,0))
            # self.game.draw_text('OPTIONS', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('VOLUME', 35, self.volx, self.voly)
            self.game.draw_text('CONTROLS', 35, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass # daqui cria o menu de volume e controles
            # if self.state == 'Volume':
            #     pass
            # elif self.state == 'Controls':
            #     pass
            
class CreditsMenu(Menu):
    def __init__(self, game): # pelo que eu entendi, essa "função dunder, com dois '_'" é pra chamar funções, variaveis, que estão em outras artes, como a de créditos não tem muita coisa, só precisamos dela!
        Menu.__init__(self, game)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY or self.game.START_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(fundo_creditos, (0,0))
            # self.game.draw_text('CREDITS', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Game design - ', 35, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2)
            self.game.draw_text('Programming -  ', 35, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('Art - ', 35, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 + 100)
            self.game.draw_text('Music - ', 35, self.game.
            DISPLAY_W / 3, self.game.DISPLAY_H / 2 + 150)
            self.blit_screen()
    