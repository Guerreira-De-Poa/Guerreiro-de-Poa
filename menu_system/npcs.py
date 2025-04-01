import pygame
from dialogo import Dialogo

class NPC(pygame.sprite.Sprite):
    def __init__(self,image,screen,pos_x,pos_y):
        super().__init__()  # Chama o inicializador da classe pai
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x,pos_y)
        self.dialogo_rect = pygame.Rect(self.rect.left-32, self.rect.top-32, self.rect.width+64, self.rect.height+64)
        self.texto = {
            'personagem_1':'Omori',
            'texto_1':['Bem vindo ao Espaço em branco', 'Meu nome é Omori'],
            'personagem_2': "Guerreiro de Poá",
            'texto_2':['Que viagem é essa?']
            }
        self.dialogo = Dialogo(self.texto,screen)