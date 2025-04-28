import pygame
import sys

pygame.init()
pygame.mixer.init()

# Tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu de Volume Estilizado")

pygame.mixer.music.load("musicas/The Four Seasons, Winter - Vivaldi.mp3")
pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop
pygame.mixer.music.set_volume(0.05)  # 50% do volume máximo

# Efeitos Sonoros
som_andar = pygame.mixer.Sound("musicas/Efeitos sonoros/Passos.mp3")
canal_andar = pygame.mixer.Channel(0)
teclas_movimento = {pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d}
teclas_pressionadas = set()

som_balançar_espada = pygame.mixer.Sound("musicas/Efeitos sonoros/Balançar espada.mp3")
canal_balançar_espada = pygame.mixer.Channel(1)
cooldown_som_balançar_espada = 0
delay_som_balançar_espada = 400
primeiro_ataque_espada = 0

som_carregar_arco = pygame.mixer.Sound("musicas/Efeitos sonoros/carregando_arco_flecha.mp3")
canal_carregar_arco = pygame.mixer.Channel(2)

som_atirar_flecha = pygame.mixer.Sound("musicas/Efeitos sonoros/Arco e flecha.mp3")
canal_atirar_flecha = pygame.mixer.Channel(3)

# Fonte
fonte = pygame.font.SysFont("arial", 24, bold=True)

# Cores
COR_BG = (20, 20, 30)
COR_MENU = (30, 30, 45)
COR_SOMBRA = (0, 0, 0, 80)
COR_SLIDER_BG = (60, 60, 80)
COR_SLIDER_FILL = (0, 200, 255)
COR_SLIDER_FILL_BORDA = (0, 150, 200)
COR_CIRCULO = (0, 255, 180)
COR_TEXTO = (255, 255, 255)
COR_BORDA_MENU = (70, 130, 180)

# Volumes
volume_musica = 0.5
volume_efeitos = 0.5
menu_ativo = False

class Som():
    def __init__(self):

        self.som_andar = pygame.mixer.Sound("musicas/Efeitos sonoros/Passos.mp3")
        self.canal_andar = pygame.mixer.Channel(0)
        self.teclas_movimento = {pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d}
        self.teclas_pressionadas = set()

        self.som_balançar_espada = pygame.mixer.Sound("musicas/Efeitos sonoros/Balançar espada.mp3")
        self.canal_balançar_espada = pygame.mixer.Channel(1)
        self.cooldown_som_balançar_espada = 0
        self.delay_som_balançar_espada = 400
        self.primeiro_ataque_espada = 0

        self.som_carregar_arco = pygame.mixer.Sound("musicas/Efeitos sonoros/carregando_arco_flecha.mp3")
        self.canal_carregar_arco = pygame.mixer.Channel(2)

        self.som_atirar_flecha = pygame.mixer.Sound("musicas/Efeitos sonoros/Arco e flecha.mp3")
        self.canal_atirar_flecha = pygame.mixer.Channel(3)

    def musica(self):
        pygame.mixer.music.load("musicas/The Four Seasons, Winter - Vivaldi.mp3")
        pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop
        pygame.mixer.music.set_volume(0.05)  # 50% do volume máximo

    def som_arco(self):
        self.som_carregar_arco.set_volume(1)
        self.canal_carregar_arco.play(som_carregar_arco, loops=0)

    def atirar(self):
        self.som_atirar_flecha.set_volume(0.05)
        self.canal_atirar_flecha.play(som_atirar_flecha, loops=0)

def desenhar_slider(x, y, valor, texto):
    largura_slider = 300
    altura_slider = 12
    pos = int(x + largura_slider * valor)

    # Texto
    label = fonte.render(f"{texto}", True, COR_TEXTO)
    TELA.blit(label, (x, y - 40))

    # Fundo do slider
    pygame.draw.rect(TELA, COR_SLIDER_BG, (x, y, largura_slider, altura_slider), border_radius=10)

    # Volume
    pygame.draw.rect(TELA, COR_SLIDER_FILL_BORDA, (x, y, largura_slider * valor, altura_slider), border_radius=10)
    pygame.draw.rect(TELA, COR_SLIDER_FILL, (x + 2, y + 2, largura_slider * valor - 4, altura_slider - 4), border_radius=10)

    # Círculo
    pygame.draw.circle(TELA, COR_CIRCULO, (pos, y + altura_slider // 2), 10)

    return pygame.Rect(x, y, largura_slider, altura_slider), pygame.Rect(pos - 10, y - 5, 20, 20)

clock = pygame.time.Clock()
arrastando_musica = False
arrastando_efeito = False