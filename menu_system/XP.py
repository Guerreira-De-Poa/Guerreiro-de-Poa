import pygame
from inimigo_teste import Inimigo

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema de Combate Simples")

class XP():
    def __init__(self, screen, screen_width, screen_height, nivel=1,pontos_disponiveis=0):

        self.screen = screen
        self.screen_width, self.screen_height = screen_width, screen_height

        # Cores
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_PURPLE = (87, 23, 215)

        # Sistema de xp
        self.xp = 0
        self.xp_limitador = 0
        self.xp_max = 100
        self.nivel = nivel
        self.nivel_anterior = self.nivel
        self.nivel_max = 100
        self.tamanho_nivel = 40
        self.dano = 15
        self.multiplicador_xp = 500
        self.temporizador_mensagem = None 

        # Variáveis xp
        self.xp_width = 200
        self.xp_height = 10
        self.xp_ratio = 0
        self.temporizador_xp = None
        self.ganhando_xp = False

        # Posição desenho do nivel
        self.pos_xp_x = (self.screen_width // 2) - (self.xp_width // 2)
        self.pos_xp_y = self.screen_height - (self.xp_height * 2)
        self.pos_nivel_x = (self.screen_width // 2) - 3
        self.pos_nivel_y = self.pos_xp_y - (self.tamanho_nivel - 10)

        # Distribuição de pontos
        self.pontos_disponiveis = pontos_disponiveis
        self.pontos_disponiveis_copy = 0

        # Inicializa o Pygame Clock
        self.clock = pygame.time.Clock()

        self.show_menu = False

    # Função para desenhar a barra de vida
    # def draw_health_bar(self, x, y, health, max_health):
    #     health_width = 200
    #     health_height = 20
    #     health_ratio = health / max_health
    #     pygame.draw.rect(screen, self.RED, (x, y, health_width, health_height))
    #     pygame.draw.rect(screen, self.GREEN, (x, y, health_width * health_ratio, health_height))

    # Atualiza a barra de XP
    def atualizar_xp(self, inimigo, xp_inimigo):
        if inimigo.HP <= 0 and not self.ganhando_xp:
            self.temporizador_xp = pygame.time.get_ticks()
            self.ganhando_xp = True
            self.xp_limitador += xp_inimigo

        if self.ganhando_xp:
            if self.xp <= self.xp_limitador and pygame.time.get_ticks() - self.temporizador_xp > 30:
                self.xp += (0.02 * self.xp_max)
                self.xp_ratio = (self.xp / self.xp_max) * 200
                self.temporizador_xp = pygame.time.get_ticks()
            elif self.xp > self.xp_limitador - (0.02 * self.xp_max):
                self.ganhando_xp = False 

        if self.nivel < self.nivel_max:
            if self.xp >= self.xp_max and self.temporizador_mensagem is None:
                self.temporizador_mensagem = pygame.time.get_ticks()

                self.nivel += 1
                self.pontos_disponiveis += 5
                # print(self.pontos_disponiveis)
                self.pontos_disponiveis_copy = self.pontos_disponiveis
                # print(self.pontos_disponiveis_copy)
                self.xp_excedente = self.xp_limitador - self.xp_max
                self.xp_max *= self.multiplicador_xp
                self.xp = 0
                self.xp_limitador = self.xp_excedente
                self.xp_ratio = (self.xp / self.xp_max) * 200

            if self.nivel_anterior < self.nivel:
                self.nivel_anterior = self.nivel

            if self.temporizador_mensagem is not None:
                font = pygame.font.SysFont(None, 55)
                text = font.render("Você upou de nível", True, self.GREEN)
                self.screen.blit(text, (self.screen_width // 2 - 120, self.screen_height // 2 - 50))
                if pygame.time.get_ticks() - self.temporizador_mensagem > 1500:
                    self.temporizador_mensagem = None
        
        else:
            self.xp_limitador = self.xp_max

    # def nivel_limitador(self):
    #     if self.nivel > 10:
    #         self.xp

    # Exibe a tela com os componentes
    def render(self):
        if self.xp_ratio is None:
            self.xp_ratio = 0  # Garantir que não seja None

        # Desenha a barra de XP
        pygame.draw.rect(self.screen, self.WHITE, (self.pos_xp_x, self.pos_xp_y, self.xp_width, self.xp_height), 0, 10)
        pygame.draw.rect(self.screen, self.DARK_PURPLE, (self.pos_xp_x, self.pos_xp_y, self.xp_ratio, self.xp_height), 0, 10)

        # Ajustar a posição do nível para não ficar desalinhado
        self.font_nivel = pygame.font.SysFont(None, self.tamanho_nivel)
        if self.nivel < self.nivel_max:
            self.text_nivel = self.font_nivel.render(f"{self.nivel}", True, self.DARK_PURPLE)
            self.screen.blit(self.text_nivel, (self.pos_nivel_x, self.pos_nivel_y))
        elif self.nivel >= 10:
            self.text_nivel = self.font_nivel.render(f"{self.nivel}", True, self.DARK_PURPLE)
            self.screen.blit(self.text_nivel, (self.pos_nivel_x - 5, self.pos_nivel_y))
        else:
            self.text_nivel = self.font_nivel.render("MAX", True, self.DARK_PURPLE)
            self.screen.blit(self.text_nivel, (self.pos_nivel_x - 30, self.pos_nivel_y))




#     # Loop do jogo
#     def game_loop(self):
#         running = True
#         while running:
#             self.movimentacao()
#             self.atualizar_xp()
#             self.render()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         self.attack(self.dano)  # Ataca quando o espaço é pressionado

#             pygame.display.flip()
#             self.clock.tick(60)

#         pygame.quit()

# # Inicia o jogo
# if _name_ == "_main_":
#     combate = Combate()
#     combate.game_loop()