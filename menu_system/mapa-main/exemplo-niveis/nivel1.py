import pygame  # Importa a biblioteca pygame
from player import Player  # Importa a classe Player do arquivo player.py

class Nivel1:
    """Classe que representa o primeiro nível do jogo"""
    def __init__(self):
        """Inicializa o nível 1"""
        # Configura a tela (mesmo tamanho do mapa principal)
        self.screen = pygame.display.set_mode((800, 600))
        
        # Cria um fundo azul claro para o nível
        self.background = pygame.Surface((800, 600))
        self.background.fill((173, 216, 230))  # Cor azul claro
        
        # Cria uma nova instância do jogador no centro
        self.player = Player(400, 300)
        
        self.font = pygame.font.SysFont(None, 48)  # Fonte para textos
        self.completed = False  # Controla se o nível foi completado
    
    def run(self):
        """Executa o loop principal do nível 1"""
        clock = pygame.time.Clock()  # Relógio para controlar FPS
        running = True  # Controla se o nível está rodando
        
        while running:  # Loop do nível
            for event in pygame.event.get():  # Pega todos os eventos
                if event.type == pygame.QUIT:  # Se clicar no X
                    pygame.quit()  # Fecha o pygame
                    return        # Sai do nível
                
                if event.type == pygame.KEYDOWN:  # Tecla pressionada
                    if event.key == pygame.K_p:  # Tecla P
                        self.completed = True  # Marca nível como completo
                        running = False       # Termina o loop
            
            # Atualiza o jogador com as teclas pressionadas
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Desenha tudo na tela
            self.screen.blit(self.background, (0, 0))  # Fundo
            self.player.draw(self.screen)               # Jogador
            
            # Desenha as instruções do nível
            texto = self.font.render("Missão 1 - Pressione P para completar", True, (0, 0, 0))
            self.screen.blit(texto, (150, 50))
            
            pygame.display.flip()  # Atualiza a tela
            clock.tick(60)        # Mantém 60 FPS