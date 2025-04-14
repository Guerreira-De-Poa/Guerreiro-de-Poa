import pygame

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class Inventario:
    def __init__(self, cor_fundo, pos_x, items=[]):
        pygame.init()

        self.Cor_fundo = cor_fundo
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 30)

        self.inventory_open = False
        self.inventory_rect = pygame.Rect(pos_x, 100, 300, 400)
        self.items = items

        self.visible_items = 5

        self.scroll_index = 0

        self.pressed_counter = 0

        self.item_index = 0

        self.imagem_espada = pygame.image.load('sword.png')
        self.imagem_armadura = pygame.image.load('icons8-peitoral-blindado-24(1).png')
        self.imagem_pocao = pygame.image.load('icons8-poção-24.png')

    def draw_inventory(self, screen):
        pygame.draw.rect(screen, self.Cor_fundo, self.inventory_rect, border_radius=15)

        #print(self.items)

        texto = self.font.render('Tipo      Nome         Atributo',True,self.WHITE)
        screen.blit(texto,(self.inventory_rect.left+10,self.inventory_rect.top))

        for i in range(self.visible_items):
            atributos_nome = 0
            atributos = 0

            if i >=len(self.items) or len(self.items) == 0:
                return
            
            if len(self.items) >4:
                for atributo_nome,atributo in self.items[self.scroll_index + i].atributos.items():
                    atributos = atributo
                    atributos_nome = atributo_nome[0:3].upper()
            elif len(self.items)>0:
                for atributo_nome,atributo in self.items[self.scroll_index + i].atributos.items():
                    atributos = atributo
                    atributos_nome = atributo_nome[0:3].upper()
                    
            if self.items[i+self.scroll_index] == self.items[self.item_index]:
                x,y = self.inventory_rect.left + 80, self.inventory_rect.top + 40 + i * 80
            else:
                x,y = self.inventory_rect.left + 70, self.inventory_rect.top + 40 + i * 80
            x_rect = self.inventory_rect.left + 80
            text = self
            if self.items[self.scroll_index + i].equipado:
                pygame.draw.rect(screen, (100,100,100), (x_rect-80,y-10,self.inventory_rect.width,40), border_radius=5)
                text = self.font.render(''+self.items[self.scroll_index + i].nome+ '      +'+ str(atributos)+ f'  {atributos_nome}', True, self.WHITE)
            else:
                text = self.font.render(self.items[self.scroll_index + i].nome+ '      +'+ str(atributos)+ f'  {atributos_nome}', True, self.WHITE)


            if self.items[self.scroll_index + i].tipo == 'consumivel':
                screen.blit(self.imagem_pocao, (x-60, y))
            elif self.items[self.scroll_index + i].tipo == 'arma':
                screen.blit(self.imagem_espada, (x-60, y))
            elif self.items[self.scroll_index + i].tipo == 'armadura':
                screen.blit(self.imagem_armadura, (x-60, y))

            screen.blit(text, (x, y))

        # for i, item in enumerate(self.items):
        #     x, y = self.inventory_rect.left + 40, self.inventory_rect.top + 40 + i * 80
        #     text = self.font.render(item, True, self.WHITE)
        #     screen.blit(text, (x, y))

    def get_item_at(self, pos):
        for i in range(self.visible_items):
            x,y = self.inventory_rect.left + 40, self.inventory_rect.top + 40 + i * 80
            if i >=len(self.items) or len(self.items) == 0:
                return
            if pygame.Rect(x, y, 300, 80).collidepoint(pos):
                return self.items[self.scroll_index + i]
        return None

    def draw_button(self, screen):
        button_rect = pygame.Rect(screen.get_width() - 150, screen.get_height() - 100, 140, 60)
        pygame.draw.rect(screen, (200, 0, 0), button_rect, border_radius=10)
        text = self.font.render("Abrir", True, self.WHITE)
        screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

    def draw_dragging_item(self, screen, dragging_item):
        text = self.font.render(dragging_item.nome, True, self.WHITE)
        screen.blit(text, pygame.mouse.get_pos())

    def remove(self,item):
        if len(self.items) == 0 or item not in self.items:
            return
        self.items.remove(item)
