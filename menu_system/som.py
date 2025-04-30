import pygame
import sys

class Som:
    def __init__(self):
        # Agora recebemos a tela como parâmetro
        
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

        # Variáveis para controle do jogo
        self.jogo_iniciado = False

    def desenhar_slider(self, x, y, valor, texto, tela):
        largura_slider = 400  # Aumentei a largura para se ajustar melhor à nova resolução
        altura_slider = 15  # Levemente aumentado para maior visibilidade
        pos = int(x + largura_slider * valor)

        # Texto
        label = self.fonte.render(f"{texto}", True, self.COR_TEXTO)
        tela.blit(label, (x, y - 50))  # Ajustei a posição vertical para se alinhar melhor

        # Fundo do slider
        pygame.draw.rect(tela, self.COR_SLIDER_BG, (x, y, largura_slider, altura_slider), border_radius=10)

        # Volume
        pygame.draw.rect(tela, self.COR_SLIDER_FILL_BORDA, (x, y, largura_slider * valor, altura_slider), border_radius=10)
        pygame.draw.rect(tela, self.COR_SLIDER_FILL, (x + 2, y + 2, largura_slider * valor - 4, altura_slider - 4), border_radius=10)

        # Círculo
        pygame.draw.circle(tela, self.COR_CIRCULO, (pos, y + altura_slider // 2), 12)  # Círculo um pouco maior

        return pygame.Rect(x, y, largura_slider, altura_slider), pygame.Rect(pos - 12, y - 6, 24, 24)  # Ajuste nas dimensões do círculo

    def update(self, tela):
        if self.menu_ativo:
            menu_x, menu_y, menu_l, menu_a = 350, 200, 500, 400  # Ajustei a posição e o tamanho do menu

            # Sombra
            sombra = pygame.Surface((menu_l, menu_a), pygame.SRCALPHA)
            pygame.draw.rect(sombra, self.COR_SOMBRA, (5, 5, menu_l, menu_a), border_radius=20)
            tela.blit(sombra, (menu_x - 5, menu_y - 5))

            # Menu
            pygame.draw.rect(tela, self.COR_MENU, (menu_x, menu_y, menu_l, menu_a), border_radius=20)
            pygame.draw.rect(tela, self.COR_BORDA_MENU, (menu_x, menu_y, menu_l, menu_a), 2, border_radius=20)

            # Sliders
            self.slider_bg_musica, self.slider_musica = self.desenhar_slider(menu_x + 50, menu_y + 110, self.volume_musica, "Música", tela)
            self.slider_bg_efeito, self.slider_efeito = self.desenhar_slider(menu_x + 50, menu_y + 210, self.volume_efeitos, "Efeitos", tela)

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.menu_ativo = not self.menu_ativo
                print("a")
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
                # print(self.volume_musica)

            if self.arrastando_efeito:
                rel_x = evento.pos[0] - self.slider_bg_efeito.x
                self.volume_efeitos = max(0, min(1, rel_x / self.slider_bg_efeito.width))