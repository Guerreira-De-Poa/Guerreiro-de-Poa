import pygame
import sys
import json
import os
from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem

def inicio():
    # Inicialização do Pygame
    pygame.init()

    # Configurações da tela
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo com Mapa e Colisões")

    # Obter caminhos dos arquivos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, 'map.json')
    spritesheet_path = os.path.join(current_dir, 'spritesheet.png')  # Nome correto da sua spritesheet

    # Carregar o arquivo JSON do mapa
    try:
        with open(map_path, 'r') as f:
            map_data = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar mapa: {e}")
        pygame.quit()
        sys.exit()

    # Configurações do mapa
    TILE_SIZE = map_data['tileSize']
    MAP_WIDTH = map_data['mapWidth']
    MAP_HEIGHT = map_data['mapHeight']

    # Classe para carregar a spritesheet do mapa
    class MapSpriteSheet:
        def __init__(self, filename):
            try:
                self.sheet = pygame.image.load(filename).convert_alpha()
                print(f"Spritesheet {filename} carregada com sucesso!")
            except Exception as e:
                print(f"Erro ao carregar spritesheet: {e}")
                self.sheet = None
        
        def get_sprite(self, x, y, width, height):
            if self.sheet:
                sprite = pygame.Surface((width, height), pygame.SRCALPHA)
                sprite.blit(self.sheet, (0, 0), (x, y, width, height))
                return sprite
            return None

    # Carregar a spritesheet do mapa
    map_spritesheet = MapSpriteSheet(spritesheet_path)
    if map_spritesheet.sheet is None:
        pygame.quit()
        sys.exit()

    # Dicionário de mapeamento de tiles
    TILE_MAPPING = {
        '33': (64, 256),
        '0': (0, 0), '1': (64, 0), '2': (128, 0),
        '3': (192, 0), '4': (256, 0), '5': (320, 0),
        '6': (384, 0), '7': (448, 0), '8': (0, 64),
        '9': (64, 64), '10': (128, 64), '11': (192, 64),
        '12': (256, 64), '13': (320, 64), '14': (384, 64),
        '15': (448, 64), '16': (0, 128), '17': (64, 128),
        '18': (128, 128), '19': (192, 128), '20': (256, 128),
        '21': (320, 128), '22': (384, 128), '23': (448, 128),
        '24': (0, 192), '25': (64, 192), '26': (128, 192),
        '27': (192, 192), '28': (256, 192), '29': (320, 192),
        '30': (384, 192), '31': (448, 192), '32': (0, 256),
    }

    def process_map_for_collision(map_data):
        walls = []
        for layer in map_data['layers']:
            if layer['collider']:
                for tile in layer['tiles']:
                    x = int(tile['x']) * TILE_SIZE
                    y = int(tile['y']) * TILE_SIZE
                    walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        return walls

    def process_map_for_rendering(map_data):
        tiles = []
        layer_order = ['Background', 'Sand', 'pedras_para_preencher_vazio', 'Grass', 
                      'Rocks', 'Cliff', 'escadas']
        
        layer_dict = {layer_name: [] for layer_name in layer_order}
        
        for layer in map_data['layers']:
            layer_name = layer['name']
            if layer_name not in layer_dict:
                layer_dict[layer_name] = []
            
            for tile in layer['tiles']:
                tile_id = str(tile['id'])
                x = int(tile['x']) * TILE_SIZE
                y = int(tile['y']) * TILE_SIZE
                
                if tile_id in TILE_MAPPING and map_spritesheet.sheet:
                    sprite_x, sprite_y = TILE_MAPPING[tile_id]
                    image = map_spritesheet.get_sprite(sprite_x, sprite_y, TILE_SIZE, TILE_SIZE)
                    if image:
                        layer_dict[layer_name].append((x, y, image))
        
        for layer_name in layer_order:
            if layer_name in layer_dict:
                tiles.extend(layer_dict[layer_name])
        
        return tiles

    # Processar o mapa
    walls = process_map_for_collision(map_data)
    map_tiles = process_map_for_rendering(map_data)
    
    if not map_tiles:
        print("Erro: Nenhum tile foi carregado para renderização!")
        pygame.quit()
        sys.exit()

    # Criar o jogador
    try:
        player_sprite_path = os.path.join(current_dir, '../../personagem.png')
        player_sprite = SpriteSheet(player_sprite_path, 0, 512, 64, 64, 4, [7 for i in range(34)], (0, 0, 0))
        player = Personagem(player_sprite)
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    # Posicionar o jogador em uma posição válida no mapa
    player.rect.x = 5 * TILE_SIZE
    player.rect.y = 5 * TILE_SIZE

    # Configuração da câmera
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    ###########################################
    # PARTE DO FPS DO JOGO

    # ESTAVA DANDO PROBLEMA EM RELAÇÃO AOS FPS (CONFLITO COM O SPRITE_TESTE_V2.PY)
    # DEIXEI DE FORMA MAIS SIMPLIFICADO, MAS DAR UMA OLHADA FUTURAMENTE

    ###########################################
    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30) # Delta time em segundos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Tratar eventos de teclado para o jogador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player.correr()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Obter teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Resetar direção
        player.direction = None
        player.nova_direcao = False

                # Adicione no início do código, com outras configurações
        DEBUG_MODE = True  # Mude para False para desativar o deb
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.direction = 'UP'
            player.nova_direcao = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.direction = 'DOWN'
            player.nova_direcao = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction = 'LEFT'
            player.nova_direcao = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction = 'RIGHT'
            player.nova_direcao = True
        elif keys[pygame.K_z]:
            DEBUG_MODE = not DEBUG_MODE
        
        # Salvar a posição anterior para colisão
        old_x, old_y = player.rect.x, player.rect.y
        
        # Atualizar jogador
        player.update()
        
        # Verificar colisões
        player_rect = player.rect
        for wall in walls:
            if player_rect.colliderect(wall):
                # Colisão detectada, voltar para a posição anterior
                player.rect.x, player.rect.y = old_x, old_y
                break
        
        # Atualizar câmera
        camera.center = player.rect.center
        
        # Limitar câmera aos limites do mapa
        camera.left = max(0, camera.left)
        camera.top = max(0, camera.top)
        camera.right = min(MAP_WIDTH * TILE_SIZE, camera.right)
        camera.bottom = min(MAP_HEIGHT * TILE_SIZE, camera.bottom)
        
        # Renderização
        screen.fill((0, 0, 0))  # Fundo preto
        
        # Desenhar o mapa (apenas tiles visíveis)
        for x, y, image in map_tiles:
            # Verificar se o tile está dentro da visão da câmera
            if (camera.left - TILE_SIZE <= x < camera.right and 
                camera.top - TILE_SIZE <= y < camera.bottom):
                screen.blit(image, (x - camera.left, y - camera.top))



        # Dentro do game loop, na seção de renderização (após desenhar o jogador):
        if DEBUG_MODE:
            # 1. Desenhar colisores do mapa (vermelho)
            for wall in walls:
                if camera.colliderect(wall):
                    debug_wall_rect = pygame.Rect(
                        wall.x - camera.left,
                        wall.y - camera.top,
                        wall.width,
                        wall.height
                    )
                    pygame.draw.rect(screen, (255, 0, 0), debug_wall_rect, 1)
            
            # 2. Desenhar colisor do jogador (azul)
            debug_player_rect = pygame.Rect(
                player.rect.x - camera.left,
                player.rect.y - camera.top,
                player.rect.width,
                player.rect.height
            )
            pygame.draw.rect(screen, (0, 0, 255), debug_player_rect, 2)
            
            # 3. Mostrar informações de debug
            font = pygame.font.SysFont(None, 24)
            debug_info = [
                f"Posição: ({player.rect.x}, {player.rect.y})",
                f"Direção: {player.direction}",
                f"Velocidade: {player.speed}",
                f"Colisores: {len(walls)}",
                "Z: Debug ON/OFF"
            ]
            
            for i, text in enumerate(debug_info):
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (10, 10 + i * 25))

        # Desenhar o jogador
        player.sheet.draw(screen, player.rect.x - camera.left, player.rect.y - camera.top)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    inicio()