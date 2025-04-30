import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
class Dialogo():
    def __init__(self,texto,screen,missao):
        self.font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf',27)
        self.font_secundaria = pygame.font.Font('8bitOperatorPlus8-Regular.ttf',30)
        #text = (font.render(texto.get('texto_1')[iter_texto], True, (100,100,100)))
        self.screen = screen

        self.text_bg = pygame.image.load("caixa_dialogo2.jpg")

        self.texto = texto

        self.iter_texto = 0
        self.texto_open = False
        self.texto_pos_x = 340
        self.frame_count = 0
        self.frase = ''
        self.letra_index = 0

        self.texto_index = 0
        self.todos_textos = []
        self.qtd_textos = 0
        self.personagem_falando = ''
        #########
        # Uma variavel para configurar o inicio da missão
        #########
        self.missao_ativada = missao  # <-- Adicionando a variável de missão ativada

        personagem = ''
        for item in self.texto.keys():
            if 'personagem' in item:
                personagem = self.texto.get(item)
            elif 'texto' in item:
                self.qtd_textos +=1
                self.todos_textos.append((personagem,item))
        
    def trocar_texto(self):
        if self.texto_open == False:
            self.texto_open = True
            return
        
        if self.texto.get(self.todos_textos[self.texto_index][1])[-1] == self.texto.get(self.todos_textos[self.texto_index][1])[self.iter_texto]:
            if self.texto_index != self.qtd_textos-1:
                self.texto_index+=1
                self.iter_texto = -1
            elif self.texto_index == self.qtd_textos-1:
                self.texto_open = False

                self.letra_index = 0
                self.frase = ''

                ##########
                # Dai caso a missão seja true, começa, essa parte funciona!
                ##########
                if self.missao_ativada !=0:
                    self.missao_ativada = True  # <-- Missão ativada aqui!
                    # print("Missão ativada!")  # Teste para ver se está funcionando
                return

        self.iter_texto +=1
        self.letra_index = 0
        self.frase = ''

    def coisa(self):
        self.frame_count +=1

        self.text = self.texto.get(self.todos_textos[self.texto_index][1])[self.iter_texto]
        self.personagem_falando = self.todos_textos[self.texto_index][0]

        if self.texto_open == True:
            self.screen.blit(self.text_bg, (300,500))

            if self.letra_index < len(self.text) and self.frame_count % 2 == 0:
                self.frase += self.text[self.letra_index]
                self.letra_index += 1

            personagem_render = self.font_secundaria.render(self.personagem_falando, True, (0,0,0))
            frase_render = self.font.render(self.frase, True, (100,100,100))

            self.screen.blit(frase_render, (self.texto_pos_x,580))
            self.screen.blit(personagem_render,(self.texto_pos_x,540))


