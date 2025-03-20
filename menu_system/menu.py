import pygame

class Menu():
    def __init__(self, game): # chamamos a classe do game.py
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20) # o cursor que vamos usar pra navegar no menu
        self.offset = -100 # ir a esquerda do texto, vai ser mais simples colocando em ação

    def draw_cursor(self): # cursor
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y )

    def blit_screen(self): # atualiza a tela
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game) # significa: um argumento que envia as variaveis da classe game, em __init__
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30 # olha que coisa linda, criou as posições de cada opção do menu
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) # alinha

    def display_menu(self):
        self.run_display = True
        while self.run_display: # mostrar o menu
            self.game.check_events()
            self.check_input() # checaimput
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Guerreiro de Poá', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Em busca do diploma perdido', 15, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 5)
            self.game.draw_text('Começar', 20, self.startx, self.starty) # adicionamos os textos, que coisa linda
            self.game.draw_text('Opções', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Créditos', 20, self.creditsx, self.creditsy)
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
                pass

            elif self.state == 'Credits':
                pass

            self.run_display = False # para o menu sumir