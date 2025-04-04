# Importa as bibliotecas necessárias
import pygame  # Biblioteca para criar jogos
import sys     # Biblioteca para interagir com o sistema
from player import Player  # Importa a classe Player do arquivo player.py
from npc import NPC       # Importa a classe NPC do arquivo npc.py
from nivel1 import Nivel1 # Importa a classe Nivel1 do arquivo nivel1.py
from nivel2 import Nivel2 # Importa a classe Nivel2 do arquivo nivel2.py

# Inicializa o pygame e configura a tela
pygame.init()  # Prepara o pygame para ser usado
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Tamanho da janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a janela
pygame.display.set_caption("Jogo de Missões")  # Título da janela

class MapaPrincipal:
    def __init__(self):
        """Inicializa o mapa principal do jogo"""
        # Cria um fundo cinza para o mapa
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((100, 100, 100))  # Cor cinza
        
        # Cria o jogador no centro da tela (veja player.py para detalhes da classe Player)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Cria dois NPCs no mapa (veja npc.py para detalhes da classe NPC)
        self.npcs = [
            NPC(300, 300, "npc1", ["Olá!", "Vamos para a Missão 1?"], 1),  # NPC 1
            NPC(500, 300, "npc2", ["E aí!", "Quer tentar a Missão 2?"], 2)  # NPC 2
        ]
        
        # Variável para controlar qual nível está ativo
        self.current_level = None

    def handle_events(self):
        """Lida com todos os eventos do jogo (teclado, mouse, etc)"""
        for event in pygame.event.get():  # Pega todos os eventos que aconteceram
            if event.type == pygame.QUIT:  # Se clicar no X da janela
                pygame.quit()  # Fecha o pygame
                sys.exit()     # Fecha o programa
            
            if event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_SPACE:  # Tecla ESPAÇO
                    for npc in self.npcs:  # Verifica cada NPC
                        # Se o jogador estiver perto o suficiente para interagir
                        if npc.rect.colliderect(self.player.interact_rect):
                            npc.interact()  # Inicia a interação (veja npc.py)
                
                if event.key == pygame.K_RETURN:  # Tecla ENTER
                    for npc in self.npcs:
                        # Se o NPC estiver esperando confirmação de missão
                        if npc.dialogo_aguardando_confirmacao:
                            # Confirma a missão e define o nível atual
                            self.current_level = npc.confirmar_missao()

    def update(self):
        """Atualiza a lógica do jogo a cada frame"""
        if not self.current_level:  # Se nenhum nível estiver ativo
            keys = pygame.key.get_pressed()  # Pega todas as teclas pressionadas
            self.player.update(keys)  # Atualiza o jogador (veja player.py)

    def draw(self):
        """Desenha tudo na tela"""
        # Desenha o fundo
        screen.blit(self.background, (0, 0))
        
        # Desenha cada NPC e verifica se pode mostrar a mensagem de interação
        for npc in self.npcs:
            npc.draw(screen)  # Desenha o NPC (veja npc.py)
            if npc.pode_interagir(self.player.rect):  # Se o jogador estiver perto
                npc.desenhar_interacao(screen)  # Mostra "Pressione ESPAÇO"
        
        # Desenha o jogador
        self.player.draw(screen)
        
        # Desenha os diálogos se estiverem ativos
        for npc in self.npcs:
            if npc.dialogo_ativo:
                npc.desenhar_dialogo(screen)

def main():
    """Função principal que roda o jogo"""
    clock = pygame.time.Clock()  # Cria um relógio para controlar o FPS
    mapa = MapaPrincipal()       # Cria o mapa principal
    nivel1 = Nivel1()            # Prepara o nível 1 (veja nivel1.py)
    nivel2 = Nivel2()            # Prepara o nível 2 (veja nivel2.py)

    while True:  # Loop principal do jogo
        mapa.handle_events()  # Processa eventos
        
        # Verifica se algum nível deve ser iniciado
        if mapa.current_level == 1:
            nivel1.run()  # Executa o nível 1
            mapa.current_level = None  # Volta para o mapa principal
        elif mapa.current_level == 2:
            nivel2.run()  # Executa o nível 2
            mapa.current_level = None  # Volta para o mapa principal
        else:
            mapa.update()  # Atualiza a lógica do mapa
            mapa.draw()   # Desenha o mapa
        
        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)         # Mantém 60 FPS

if __name__ == "__main__":
    main()  # Inicia o jogo quando o arquivo é executado