import pygame  # Importa a biblioteca pygame

class NPC:
    """Classe que representa os personagens não jogáveis (NPCs)"""
    def __init__(self, x, y, name, dialogos, nivel_destino):
        """Inicializa o NPC com posição, nome, diálogos e missão associada"""
        # Retângulo principal do NPC (32x32 pixels)
        self.rect = pygame.Rect(x, y, 32, 32)
        
        # Área maior para detectar quando o jogador está perto o suficiente para interagir
        self.dialogo_rect = pygame.Rect(x - 50, y - 50, 132, 132)
        
        self.name = name  # Nome do NPC (para identificação)
        self.dialogos = dialogos  # Lista de falas do NPC
        self.dialogo_ativo = False  # Controla se o diálogo está sendo mostrado
        self.dialogo_index = 0  # Índice da fala atual
        self.dialogo_aguardando_confirmacao = False  # Esperando confirmação de missão
        self.nivel_destino = nivel_destino  # Qual nível esse NPC inicia
        self.missao_completa = False  # Se a missão foi completada
        self.color = (0, 255, 0) if not self.missao_completa else (100, 100, 100)  # Cor verde ou cinza
        self.font = pygame.font.SysFont(None, 36)  # Fonte para textos
    
    def pode_interagir(self, player_rect):
        """Verifica se o jogador está perto o suficiente para interagir"""
        # Retorna True se o jogador está na área de interação E o diálogo não está ativo
        return player_rect.colliderect(self.dialogo_rect) and not self.dialogo_ativo
    
    def interact(self):
        """Inicia ou avança o diálogo quando o jogador interage"""
        if not self.dialogo_ativo:  # Se o diálogo não estava ativo
            self.dialogo_ativo = True  # Ativa o diálogo
            self.dialogo_index = 0     # Começa na primeira fala
            
            # Se a missão já foi completada, muda os diálogos
            if self.missao_completa:
                self.dialogos = ["Obrigado! Missão já completada."]
        else:
            # Se não é a última fala, avança para a próxima
            if self.dialogo_index < len(self.dialogos) - 1:
                self.dialogo_index += 1
            # Se for a última fala e a missão não foi completada, pede confirmação
            elif not self.missao_completa:
                self.dialogo_aguardando_confirmacao = True
    
    def confirmar_missao(self):
        """Confirma a missão e retorna o nível de destino"""
        if self.dialogo_aguardando_confirmacao:  # Se estava esperando confirmação
            self.dialogo_ativo = False  # Fecha o diálogo
            self.dialogo_aguardando_confirmacao = False  # Para de esperar confirmação
            return self.nivel_destino  # Retorna qual nível deve ser carregado
        return None  # Retorna None se não havia confirmação pendente
    
    def desenhar_dialogo(self, surface):
        """Desenha a caixa de diálogo na tela"""
        # Desenha o fundo branco da caixa de diálogo
        pygame.draw.rect(surface, (255, 255, 255), (50, 400, 700, 150))
        # Desenha a borda preta
        pygame.draw.rect(surface, (0, 0, 0), (50, 400, 700, 150), 2)
        
        # Renderiza o texto da fala atual
        texto = self.font.render(self.dialogos[self.dialogo_index], True, (0, 0, 0))
        surface.blit(texto, (70, 450))  # Desenha o texto
        
        # Se estiver esperando confirmação, mostra instruções
        if self.dialogo_aguardando_confirmacao:
            confirmacao = self.font.render(
                "Enter para confirmar, ESC para recusar", True, (0, 0, 0))
            surface.blit(confirmacao, (70, 500))
    
    def desenhar_interacao(self, surface):
        """Desenha a mensagem 'Pressione ESPAÇO para interagir' acima do NPC"""
        if not self.dialogo_ativo:  # Só mostra se não estiver em diálogo
            texto = self.font.render("Interagir...", True, (255, 255, 255))
            
            # Cria um retângulo preto como fundo para o texto
            bg_rect = pygame.Rect(
                self.rect.centerx - 150,  # Centraliza horizontalmente
                self.rect.y - 40,         # Posiciona acima do NPC
                300, 30                   # Tamanho do fundo
            )
            
            # Desenha o fundo e a borda
            pygame.draw.rect(surface, (0, 0, 0), bg_rect)
            pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)
            
            # Desenha o texto sobre o fundo
            surface.blit(texto, (bg_rect.x + 10, bg_rect.y + 5))
    
    def draw(self, surface):
        """Desenha o NPC na tela"""
        pygame.draw.rect(surface, self.color, self.rect)  # Desenha o quadrado do NPC