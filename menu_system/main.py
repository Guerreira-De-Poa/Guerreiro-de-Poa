# filepath: c:\Users\Matt-dev\Desktop\projeto-senai-pygame\Guerreiro-de-Poa\menu_system\main.py
import pygame
from game import Game

pygame.init()
pygame.mixer.init()  # Inicializa o mixer

g = Game()

# VAMOS ADICIONAR A MÚSICA DO MENU!
# ABAIXO SÃO OS 3 PARANAUE PARA COMEÇAR A MUSICA
pygame.mixer.music.load("musicas/O mio Babbino Caro.mp3")
pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop
pygame.mixer.music.set_volume(0.3)  # 50% do volume máximo

while g.running:
    
    g.curr_menu.display_menu()
    g.game_loop()