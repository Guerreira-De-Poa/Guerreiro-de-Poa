import pygame
import json
# import os

# Inicialização do Pygame
pygame.init()

# Carregar o arquivo JSON do mapa
with open('mapa-boss/map.json') as f:
    map_data = json.load(f)

# Configurações do jogo
TILE_SIZE = 16
MAP_WIDTH = map_data['mapWidth']
MAP_HEIGHT = map_data['mapHeight']
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)  # Para visualização de colisões

# Criar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo com Sistema de Colisões e Spritesheet")
clock = pygame.time.Clock()

# Classe para carregar a spritesheet
class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            print("Spritesheet carregada com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar spritesheet: {e}")
            self.sheet = None
    
    def get_sprite(self, x, y, width, height):
        if self.sheet:
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(self.sheet, (0, 0), (x, y, width, height))

            sprite = pygame.transform.scale(sprite, (64, 64))
            return sprite
        return None

# Carregar a spritesheet
spritesheet = SpriteSheet('mapa-boss/spritesheet.png')

# Dicionário de mapeamento de tiles (ajuste conforme sua spritesheet)
TILE_MAPPING = {
    # está tudo confuso, mas está certo
    # Background
    '0': (0, 0), '1': (16, 0), '2': (32, 0),
    '3': (48, 0), '4': (64, 0), '5': (80, 0),
    '6': (96, 0), '7': (112, 0), '8': (0, 16),
    '9': (16, 16), '10': (32, 16), '11': (48, 16),
    '12': (64, 16), '13': (80, 16), '14': (96, 16),
    '15': (112, 16), '16': (0, 32), '17': (16, 32),
    '18': (32, 32), '19': (48, 32), '20': (64, 32),
    '21': (80, 32), '22': (96, 32), '23': (112, 32),
    '24': (0, 48), '25': (16, 48), '26': (32, 48),
    '27': (48, 48), '28': (64, 48), '29': (80, 48),
    '30': (96, 48), '31': (112, 48), '32': (0, 64),
    '33': (16, 64), '34': (32, 64), '35': (48, 64),
    '36': (64, 64), '37': (80, 64), '38': (96, 64),
    '39': (112, 64), '40': (0, 80),

}

# Classe do jogador com colisões aprimoradas
class Player:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE - 4  # Ligeiramente menor que o tile para melhor colisão
        self.height = TILE_SIZE - 4
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Sprite do jogador
        if spritesheet.sheet:
            # Ajuste essas coordenadas para a posição do sprite do jogador na spritesheet
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(BLUE)
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(BLUE)
    
    def update(self, walls):
        keys = pygame.key.get_pressed()
        
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
        
        # Verificar colisões em X e Y separadamente
        if dx != 0:
            self.move_single_axis(dx, 0, walls)
        if dy != 0:
            self.move_single_axis(0, dy, walls)
    
    def move_single_axis(self, dx, dy, walls):
        self.rect.x += dx
        self.rect.y += dy
        
        for wall in walls:
            if self.rect.colliderect(wall['rect']):
                if dx > 0:  # Movendo para direita
                    self.rect.right = wall['rect'].left
                elif dx < 0:  # Movendo para esquerda
                    self.rect.left = wall['rect'].right
                elif dy > 0:  # Movendo para baixo
                    self.rect.bottom = wall['rect'].top
                elif dy < 0:  # Movendo para cima
                    self.rect.top = wall['rect'].bottom
        
        self.x = self.rect.x
        self.y = self.rect.y
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Processar o mapa para colisões
def process_map_for_collision(map_data):
    walls = []
    
    for layer in map_data['layers']:
        if layer['collider']:
            for tile in layer['tiles']:
                x = int(tile['x']) * 64
                y = int(tile['y']) * 64
                walls.append({
                    'rect': pygame.Rect(x, y, 64, 64),
                    'layer': layer['name']
                })
    
    return walls

# Processar o mapa para renderização com spritesheet (corrigido)
def process_map_for_rendering(map_data):
    tiles = []
    
    # Ordem de renderização das camadas (do fundo para a frente)
    layer_order = ['Floor', 'Walls', 'Walls sides', 'Miscs', 'Doors', 'decoracoes']
    
    # Criar um dicionário para agrupar tiles por camada
    layer_dict = {layer_name: [] for layer_name in layer_order}
    
    # Agrupar todos os tiles por camada
    for layer in map_data['layers']:
        layer_name = layer['name']
        if layer_name not in layer_dict:
            layer_dict[layer_name] = []
        
        for tile in layer['tiles']:
            tile_id = str(tile['id'])
            x = int(tile['x']) * 64
            y = int(tile['y']) * 64
            
            if tile_id in TILE_MAPPING and spritesheet.sheet:
                sprite_x, sprite_y = TILE_MAPPING[tile_id]
                image = spritesheet.get_sprite(sprite_x, sprite_y, TILE_SIZE, TILE_SIZE)
                color = None
            else:
                image = None
                color = {
                    'Buildings': (150, 150, 150),
                    'Rocks': (100, 100, 100),
                    'Cliff': (120, 80, 50),
                    'Sand': (210, 180, 140),
                    'Grass': (100, 180, 100),
                    'Background': (50, 50, 150),
                    'pedras_para_preencher': (200, 200, 200),
                    'escadas': (200, 0, 200),
                }.get(layer_name, (200, 200, 200))
            
            layer_dict[layer_name].append({
                'rect': pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                'image': image,
                'color': color,
                'layer': layer_name,
                'collider': layer['collider']
            })
    
    # Adicionar os tiles na ordem correta
    for layer_name in layer_order:
        if layer_name in layer_dict:
            tiles.extend(layer_dict[layer_name])
    
    return tiles

# Processar o mapa
walls = process_map_for_collision(map_data)
tiles = process_map_for_rendering(map_data)

# Criar o jogador
player = Player(50, 10)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    player.update(walls)
    
    # Renderização
    screen.fill(BLACK)
    
    # Desenhar tiles - agora com spritesheet e ordem correta
    for tile in tiles:
        if tile['image']:
            screen.blit(tile['image'], (tile['rect'].x, tile['rect'].y))
        else:
            pygame.draw.rect(screen, tile['color'], tile['rect'])
    
    # Desenhar paredes (debug) - opcional
    for wall in walls:
        pygame.draw.rect(screen, RED, wall['rect'], 1)
    
    player.draw(screen)
    
    # Debug info
    font = pygame.font.SysFont(None, 24)
    debug_info = [
        f"Posição: ({player.rect.x}, {player.rect.y})",
        f"Tiles renderizados: {len(tiles)}",
        f"Tiles colidíveis: {len(walls)}",
        "Setas/WASD: mover | ESC: sair"
    ]
    
    for i, text in enumerate(debug_info):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()