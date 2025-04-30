import pygame
from inventario1 import Inventario
import os
import sys

pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'assets'))
sys.path.append(pasta_pai)

class Bau(pygame.sprite.Sprite):
    def __init__(self,screen,pos_x,pos_y,loot=[]):
        super().__init__()  # Chama o inicializador da classe pai
        self.bau_fechado = pygame.image.load(os.path.join(pasta_pai, 'chest_closed.png'))
        self.bau_aberto = pygame.image.load(os.path.join(pasta_pai, 'chest_opened.png'))

        self.image = self.bau_fechado
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.interagir_rect = pygame.Rect(self.rect.left-32, self.rect.top-32, self.rect.width+64, self.rect.height+64)

        self.loot = loot

        self.inventario = Inventario((125,125,0),600,self.loot)
    
    def abrir_bau(self):
        self.image = self.bau_aberto