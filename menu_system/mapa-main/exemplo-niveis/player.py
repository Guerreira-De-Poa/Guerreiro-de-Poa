import pygame  # Importa a biblioteca pygame

class Player:
    """Classe que representa o jogador principal"""
    def __init__(self, x, y):
        """Inicializa o jogador na posição (x, y)"""
        # Cria um retângulo para representar o jogador (32x32 pixels)
        self.rect = pygame.Rect(x, y, 32, 32)
        
        # Cria um retângulo maior para detectar interações (132x132 pixels)
        self.interact_rect = pygame.Rect(x - 50, y - 50, 132, 132)
        
        self.speed = 5          # Velocidade de movimento
        self.color = (0, 0, 255)  # Cor azul para o jogador
        self.interaction_cooldown = 0  # Tempo de espera entre interações
    
    def update(self, keys):
        """Atualiza a posição do jogador baseado nas teclas pressionadas"""
        # Diminui o tempo de espera entre interações se necessário
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= 1
        
        # Calcula a direção do movimento baseado nas teclas
        dx, dy = 0, 0  # Inicializa as direções como zero
        
        # Tecla W (cima) diminui a coordenada Y
        if keys[pygame.K_w]: dy -= self.speed
        # Tecla S (baixo) aumenta a coordenada Y
        if keys[pygame.K_s]: dy += self.speed
        # Tecla A (esquerda) diminui a coordenada X
        if keys[pygame.K_a]: dx -= self.speed
        # Tecla D (direita) aumenta a coordenada X
        if keys[pygame.K_d]: dx += self.speed
        
        # Move o jogador
        self.rect.x += dx
        self.rect.y += dy
        
        # Atualiza a posição da área de interação para acompanhar o jogador
        self.interact_rect.center = self.rect.center
        
        # Limita o jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
    
    def draw(self, surface):
        """Desenha o jogador na tela"""
        pygame.draw.rect(surface, self.color, self.rect)  # Desenha o jogador
        
        # (Para debug) Desenha a área de interação em vermelho
        pygame.draw.rect(surface, (255, 0, 0), self.interact_rect, 1)