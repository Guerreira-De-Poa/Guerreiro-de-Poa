import pygame
import sys

class Som:
    def __init__(self):
        # Inicialização do pygame e tela
        pygame.init()
        self.TELA = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Controle de Som")
        
        # Definindo cores como atributos da instância
        self.COR_TEXTO = (255, 255, 255)
        self.COR_SLIDER_BG = (50, 50, 50)
        self.COR_SLIDER_FILL_BORDA = (200, 200, 200)
        self.COR_SLIDER_FILL = (0, 255, 0)
        self.COR_CIRCULO = (255, 0, 0)
        self.COR_SOMBRA = (0, 0, 0, 128)
        self.COR_MENU = (60, 60, 60)
        self.COR_BORDA_MENU = (255, 255, 255)

        # Inicialização da fonte
        self.fonte = pygame.font.SysFont(None, 36)

        # Variáveis de controle de som
        self.volume_musica = 1
        self.volume_efeitos = 1
        self.menu_ativo = False
        self.arrastando_musica = False
        self.arrastando_efeito = False

        # Inicialização do mixer de som
        pygame.mixer.init()
        self.efeito_musica = pygame.mixer.music.load('musicas/fundo.mp3')  # Substitua pelo seu arquivo de efeito sonoro
        self.efeito_som.set_volume(self.volume_efeitos)  # Define o volume inicial do efeito sonoro
        pygame.mixer.music.set_volume(self.volume_musica)  # Configura volume inicial para música

        # Variáveis para controle do jogo
        self.jogo_iniciado = False

    def desenhar_slider(self, x, y, valor, texto):
        largura_slider = 300
        altura_slider = 12
        pos = int(x + largura_slider * valor)

        # Texto
        label = self.fonte.render(f"{texto}", True, self.COR_TEXTO)
        self.TELA.blit(label, (x, y - 40))

        # Fundo do slider
        pygame.draw.rect(self.TELA, self.COR_SLIDER_BG, (x, y, largura_slider, altura_slider), border_radius=10)

        # Volume
        pygame.draw.rect(self.TELA, self.COR_SLIDER_FILL_BORDA, (x, y, largura_slider * valor, altura_slider), border_radius=10)
        pygame.draw.rect(self.TELA, self.COR_SLIDER_FILL, (x + 2, y + 2, largura_slider * valor - 4, altura_slider - 4), border_radius=10)

        # Círculo
        pygame.draw.circle(self.TELA, self.COR_CIRCULO, (pos, y + altura_slider // 2), 10)

        return pygame.Rect(x, y, largura_slider, altura_slider), pygame.Rect(pos - 10, y - 5, 20, 20)

    def desenhar_tela_inicial(self):
        # Exibe uma tela inicial com um texto e opção de pressionar Enter
        self.TELA.fill((0, 0, 0))  # Preenche a tela com cor preta
        titulo = self.fonte.render("Pressione ENTER para começar", True, self.COR_TEXTO)
        self.TELA.blit(titulo, (250, 250))

    def update(self):
        if self.menu_ativo:
            menu_x, menu_y, menu_l, menu_a = 200, 150, 400, 300

            # Sombra
            sombra = pygame.Surface((menu_l, menu_a), pygame.SRCALPHA)
            pygame.draw.rect(sombra, self.COR_SOMBRA, (5, 5, menu_l, menu_a), border_radius=20)
            self.TELA.blit(sombra, (menu_x - 5, menu_y - 5))

            # Menu
            pygame.draw.rect(self.TELA, self.COR_MENU, (menu_x, menu_y, menu_l, menu_a), border_radius=20)
            pygame.draw.rect(self.TELA, self.COR_BORDA_MENU, (menu_x, menu_y, menu_l, menu_a), 2, border_radius=20)

            # Sliders
            self.slider_bg_musica, self.slider_musica = self.desenhar_slider(menu_x + 50, menu_y + 110, self.volume_musica, "Música")
            self.slider_bg_efeito, self.slider_efeito = self.desenhar_slider(menu_x + 50, menu_y + 210, self.volume_efeitos, "Efeitos")

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.menu_ativo = not self.menu_ativo
                if evento.key == pygame.K_SPACE and self.efeito_som:
                    self.efeito_som.play()

                if evento.key == pygame.K_RETURN and not self.jogo_iniciado:
                    self.jogo_iniciado = True  # Marca que o jogo foi iniciado

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_ativo:
                    if self.slider_musica.collidepoint(evento.pos):
                        self.arrastando_musica = True
                    if self.slider_efeito.collidepoint(evento.pos):
                        self.arrastando_efeito = True

            if evento.type == pygame.MOUSEBUTTONUP:
                self.arrastando_musica = False
                self.arrastando_efeito = False

            if evento.type == pygame.MOUSEMOTION:
                if self.arrastando_musica:
                    rel_x = evento.pos[0] - self.slider_bg_musica.x
                    self.volume_musica = max(0, min(1, rel_x / self.slider_bg_musica.width))
                    pygame.mixer.music.set_volume(self.volume_musica)
                    print(self.volume_musica)


                if self.arrastando_efeito and self.efeito_som:
                    rel_x = evento.pos[0] - self.slider_bg_efeito.x
                    self.volume_efeitos = max(0, min(1, rel_x / self.slider_bg_efeito.width))
                    self.efeito_som.set_volume(self.volume_efeitos)  # Ajusta o volume do efeito sonoro
                    print(self.volume_efeitos, self.efeito_som)

    def run(self):
        while True:
            if not self.jogo_iniciado:
                self.desenhar_tela_inicial()  # Desenha a tela inicial enquanto o jogo não foi iniciado
            else:
                self.update()  # Se o jogo foi iniciado, faz o update do jogo

            pygame.display.update()  # Atualiza a tela

            self.processar_eventos()  # Processa os eventos (como pressionar teclas)
            
            pygame.time.Clock().tick(60)  # Controla o FPS para não rodar o loop muito rápido


# Cria a instância do jogo e inicia
jogo = Som()
jogo.run()
