import pygame

class Bau(pygame.sprite.Sprite):
    def __init__(self,screen,pos_x,pos_y):
        super().__init__()  # Chama o inicializador da classe pai
        self.bau_fechado = pygame.image.load("chest_closed.png")
        self.bau_aberto = pygame.image.load("chest_opened.png")

        self.image = self.bau_fechado
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.interagir_rect = pygame.Rect(self.rect.left-32, self.rect.top-32, self.rect.width+64, self.rect.height+64)
    
    def abrir_bau(self):
        self.image = self.bau_aberto