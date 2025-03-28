import pygame
from dialogo import Dialogo

class NPC(pygame.sprite.Sprite):
    def __init__(self,image,screen):
        super().__init__()  # Chama o inicializador da classe pai
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (300,800)
        self.texto = {
            'personagem_1':'Omori',
            'texto_1':['Bem vindo ao Espaço em branco', 'Meu nome é Omori'],
            'personagem_2': "Guerreiro de Poá",
            'texto_2':['Que viagem é essa?']
            }
        self.dialogo = Dialogo(self.texto,screen)