import pygame
from dialogo import Dialogo

class NPC(pygame.sprite.Sprite):
    def __init__(self,image,screen,pos_x,pos_y,texto):
        super().__init__()  # Chama o inicializador da classe pai
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.dialogo_rect = pygame.Rect(self.rect.left-32, self.rect.top-32, self.rect.width+64, self.rect.height+64)
        self.texto = texto
        self.dialogo = Dialogo(self.texto,screen)