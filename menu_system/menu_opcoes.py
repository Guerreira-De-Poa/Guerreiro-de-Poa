import pygame
import sys

pygame.init()

width, height = 1200, 800
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pressione 0 para sair")
rodando = True

class MenuOpcoes:
    def __init__(self, width, height, tela, rodando):
        self.width, self.height = width, height
        self.tela = tela

        self.branco = (255, 255, 255)
        self.preto = (0, 0, 0)
        self.escurecedor = pygame.Surface((1200, 800), pygame.SRCALPHA)
        self.escurecedor.fill((0, 0, 0, 80))

        self.clock = pygame.time.Clock()
        self.rodando = rodando
        self.pausado = False
        self.som_ligado = True
        self.evento_ativado = False

        self.opcao_selecionada = 0
        self.pos_espadinha_x, self.pos_espadinha_y = 325, 303
        self.pos_espadinha_y_final = self.pos_espadinha_y
        self.mudar_opcao_baixo = False
        self.mudar_opcao_cima = False

        self.ativar_controles_img = False
        self.pos_menus = []

        self.retangulo_transparente = pygame.Rect(981, 127, 35, 42)

        # Imagens
        self.imgs = {
            "controles": pygame.transform.scale(
                pygame.image.load("menu_opcoes_imagens/Controles_guerreiro_poa.png"), (850, 567)
            ),
            "espadinha": pygame.image.load("menu_opcoes_imagens/espadinha_menu_opcoes.png"),
        }

    def desenhar_menu(self):
        fonte = pygame.font.Font(None, 60)
        texto_paused = fonte.render("Jogo Pausado", True, self.preto)
        self.tela.blit(texto_paused, (self.width // 2 - texto_paused.get_width() // 2, self.height // 2 - 200))

        nomes = ["Continuar", "Audio", "Controles", "Sair"]
        self.pos_menus = []

        for i, nome in enumerate(nomes):
            y = 288 + i * 80
            imagem = pygame.image.load(f"menu_opcoes_imagens/{nome}.png")
            self.tela.blit(imagem, (425, y))
            self.pos_menus.append(pygame.Rect(425, y, 350, 74))

    def processar_eventos(self, evento):
        # for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_0):
                self.rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and self.pausado and self.evento_ativado == False:
                    if self.opcao_selecionada == 0:
                        self.pausado = False
                    elif self.opcao_selecionada == 1:
                        self.som_ligado = not self.som_ligado
                    elif self.opcao_selecionada == 2:
                        self.ativar_controles_img = True
                        self.evento_ativado = True
                    elif self.opcao_selecionada == 3:
                        self.rodando = False
                    
                elif evento.key == pygame.K_SPACE and self.pausado and self.evento_ativado and self.ativar_controles_img == True:
                    self.ativar_controles_img = False
                    self.evento_ativado = False

                elif evento.key == pygame.K_ESCAPE:
                    if self.evento_ativado and self.ativar_controles_img:
                        self.ativar_controles_img = False
                        self.evento_ativado = False
                    else:
                        self.pausado = not self.pausado

                elif evento.key == pygame.K_DOWN and self.pausado:
                    print("A")
                    if self.opcao_selecionada < len(self.pos_menus) - 1:
                        self.opcao_selecionada += 1
                        self.pos_espadinha_y_final += 80
                        self.mudar_opcao_baixo = True
                elif evento.key == pygame.K_UP and self.pausado:
                    if self.opcao_selecionada > 0:
                        self.opcao_selecionada -= 1
                        self.pos_espadinha_y_final -= 80
                        self.mudar_opcao_cima = True

    def atualizar(self):
        if self.mudar_opcao_baixo:
            self.pos_espadinha_y += 8
            if self.pos_espadinha_y >= self.pos_espadinha_y_final:
                self.mudar_opcao_baixo = False

        if self.mudar_opcao_cima:
            self.pos_espadinha_y -= 8
            if self.pos_espadinha_y <= self.pos_espadinha_y_final:
                self.mudar_opcao_cima = False

    def desenhar(self):
        # self.tela.fill(self.branco)

        if self.pausado:
            self.tela.blit(self.escurecedor, (0, 0))
            self.desenhar_menu()

            self.tela.blit(self.imgs["espadinha"], (self.pos_espadinha_x, self.pos_espadinha_y))

            nomes = ["Continuar", "Audio", "Controles", "Sair"]
            if 0 <= self.opcao_selecionada < len(nomes):
                nome = nomes[self.opcao_selecionada]
                imagem = pygame.image.load(f"menu_opcoes_imagens/{nome}_selecionado.png")
                self.tela.blit(imagem, (425, 288 + self.opcao_selecionada * 80))

            if self.ativar_controles_img:
                self.tela.blit(self.imgs["controles"], (self.width // 2 - 425, self.height // 2 - 284))

        pygame.display.flip()

    def executar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# # Iniciar o menu
# menu = MenuOpcoes(width, height, tela, rodando)
# menu.executar()
