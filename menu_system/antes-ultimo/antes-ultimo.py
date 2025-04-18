import pygame
import sys
import json
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem
from npcs import * 
from dialogo import *
from inimigo_teste import *
from inventario1 import Inventario
from boss import Boss1
from bau import Bau
from XP import XP
from menu_status import Menu

pause = False

def inicio():
    boss_parado = False
    global pause
    
    # Inicialização do Pygame
    pygame.init()

    # Configurações da tela
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo com Mapa e Colisões")

    # Obter caminhos dos arquivos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, 'map.json')
    spritesheet_path = os.path.join(current_dir, 'spritesheet.png')

    # Carregar o arquivo JSON do mapa
    try:
        with open(map_path, 'r') as f:
            map_data = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar mapa: {e}")
        pygame.quit()
        sys.exit()

    # Configurações do mapa (tamanho final desejado)
    TILE_SIZE = 64  # Tamanho final dos tiles na tela
    ORIGINAL_TILE_SIZE = 16  # Tamanho original na spritesheet
    SCALE_FACTOR = TILE_SIZE // ORIGINAL_TILE_SIZE
    
    MAP_WIDTH = map_data['mapWidth']
    MAP_HEIGHT = map_data['mapHeight']

    # Classe para carregar a spritesheet do mapa (corrigida)
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
                # Pegar o tile no tamanho original (16x16)
                sprite = pygame.Surface((ORIGINAL_TILE_SIZE, ORIGINAL_TILE_SIZE), pygame.SRCALPHA)
                sprite.blit(self.sheet, (0, 0), (x, y, ORIGINAL_TILE_SIZE, ORIGINAL_TILE_SIZE))
                # Escalar para o tamanho desejado (64x64)
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            return None

    # Carregar a spritesheet do mapa
    map_spritesheet = MapSpriteSheet(spritesheet_path)
    if map_spritesheet.sheet is None:
        pygame.quit()
        sys.exit()

    xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    menu = Menu(5, 5, 5, 5, 5, 6.25, 0.0, 10, 6.25, 5.0)

    # Dicionário de mapeamento de tiles (coordenadas originais 16x16)
    TILE_MAPPING = {
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
        '39': (112, 64), '40': (0, 80), '41': (16, 80),
        '42': (32, 80), '43': (48, 80), '44': (64, 80),
        '45': (80, 80), '46': (96, 80), '47': (112, 80),
        '48': (0, 96), '49': (16, 96), '50': (32, 96),
        '51': (48, 96), '52': (64, 96), '53': (80, 96),
        '54': (96, 96), '55': (112, 96), '56': (0, 112),
        '57': (16, 112), '58': (32, 112), '59': (48, 112),
        '60': (64, 112),
    }

    def process_map_for_collision(map_data):
        walls = []
        for layer in map_data['layers']:
            if layer['collider']:
                for tile in layer['tiles']:
                    # Usar TILE_SIZE (64) para colisões
                    x = int(tile['x']) * TILE_SIZE
                    y = int(tile['y']) * TILE_SIZE
                    walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        return walls

    def process_map_for_rendering(map_data):
        tiles = []
        layer_order = ['Floor', 'Walls', 'Walls sides', 'Miscs', 'Doors', 'colunas']
        
        layer_dict = {layer_name: [] for layer_name in layer_order}
        
        for layer in map_data['layers']:
            layer_name = layer['name']
            if layer_name not in layer_dict:
                layer_dict[layer_name] = []
            
            for tile in layer['tiles']:
                tile_id = str(tile['id'])
                # Usar coordenadas originais (16) para posicionamento
                x = int(tile['x']) * ORIGINAL_TILE_SIZE
                y = int(tile['y']) * ORIGINAL_TILE_SIZE
                
                if tile_id in TILE_MAPPING and map_spritesheet.sheet:
                    sprite_x, sprite_y = TILE_MAPPING[tile_id]
                    image = map_spritesheet.get_sprite(sprite_x, sprite_y, ORIGINAL_TILE_SIZE, ORIGINAL_TILE_SIZE)
                    if image:
                        # Multiplicar por SCALE_FACTOR para posicionar corretamente
                        layer_dict[layer_name].append((x * SCALE_FACTOR, y * SCALE_FACTOR, image))
        
        for layer_name in layer_order:
            if layer_name in layer_dict:
                tiles.extend(layer_dict[layer_name])
        
        return tiles

    # Processar o mapa
    walls = process_map_for_collision(map_data)
    map_tiles = process_map_for_rendering(map_data)
    
    lista_1 = [7 for i in range(4)]
    lista_2 = [4 for i in range(4)]
    lista_3 = [6 for i in range(8)]
    lista_4 = [13 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    # Criar o jogador
    try:
        player_sprite_path = os.path.join(current_dir, '..', '..', 'personagem_carcoflecha(2).png')
        player_sprite_path2 = os.path.join(current_dir, '..', '..', 'sprites_ataque_espada.png')
        
        player_sprite = SpriteSheet(player_sprite_path, 0, 514, 64, 64, 4, lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
        player_sprite_ataques = SpriteSheet(player_sprite_path2, 8, 38, 128, 128, 12, [6,6,6,6], (255,255,255))
        
        player = Personagem(player_sprite, menu.atributos["ataque"], menu.atributos["defesa"], menu.atributos["vida"], 
                           menu.atributos["stamina"], menu.atributos["velocidade"], player_sprite_ataques)
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    player.rect.x, player.rect.y = 1056, 800

    # Configuração da câmera
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    spritesheet_inimigo_arco2 = SpriteSheet('boss_agua.png', 0, 522, 64, 64, 4, lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    boss = Boss1(player.rect, player, 1220, 1000, True, spritesheet_inimigo_arco2, 30, 300, 200)

    inimigos = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_group.add(player)
    all_sprites.add(boss)
    inimigos.add(boss)

    contador = 0
    click_hold = 0
    interagir_bg = pygame.image.load("caixa_dialogo_pequena.jpg")
    npcs = pygame.sprite.Group()
    baus = pygame.sprite.Group()
    dialogo_group = []

    # Configurações de inventário
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 140, 60)
    dragging_item = None
    dragging_from = None

    inventario1 = Inventario((50, 50, 50), 50, ["Espada", "Poção", "Escudo"])
    inventario2 = Inventario((0, 100, 0), 400)

    contador_ataque_melee = 0
    dash = 0
    cooldown_dash = 0
    velocidade_anterior = 0
    contador_melee = 0

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        player.atualizar_stamina()
        bau_perto = False

        for bau in baus:
            if bau.interagir_rect.colliderect(player.rect):
                bau_perto = bau

        clock.tick(60)
        botao_ativo = False
        dialogo_a_abrir = False

        screen.fill((100, 100, 100))

        dialogo_hitbox = False
        for npc in npcs:
            if npc.dialogo_rect.colliderect(player.rect):
                dialogo_hitbox = npc

        if dialogo_hitbox:
            dialogo_a_abrir = dialogo_hitbox.dialogo

        for bau in baus:
            if bau_perto == bau:
                if bau.interagir_rect.colliderect(player.rect):
                    botao_ativo = True
                if bau.rect.colliderect(player.rect):
                    player.rect.x, player.rect.y = old_x, old_y
                elif not bau.interagir_rect.colliderect(player.rect):
                    botao_ativo = False
                    if bau_perto:
                        bau_perto.inventario.inventory_open = False

        keys = pygame.key.get_pressed()
        player.direction = None
        player.nova_direcao = False

        if keys[pygame.K_w]:
            player.direction = 'UP'
        elif keys[pygame.K_s]:
            player.direction = 'DOWN'
        elif keys[pygame.K_a]:
            player.direction = 'LEFT'
        elif keys[pygame.K_d]:
            player.direction = 'RIGHT'
        else:
            player.direction = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.nova_direcao = True
                elif event.key == pygame.K_s:
                    player.nova_direcao = True
                elif event.key == pygame.K_a:
                    player.nova_direcao = True
                elif event.key == pygame.K_d:
                    player.nova_direcao = True
                elif event.key == pygame.K_r:
                    if cooldown_dash == 0:
                        velocidade_anterior = player.speed
                        player.dash = True
                        cooldown_dash = 1
                elif event.key == pygame.K_LSHIFT:
                    player.correr()
                elif event.key == pygame.K_SPACE:
                    if dialogo_a_abrir:
                        dialogo_a_abrir.trocar_texto()
                    elif botao_ativo:
                        if bau_perto:
                            bau_perto.inventario.inventory_open = not bau_perto.inventario.inventory_open
                elif event.key == pygame.K_z:
                    DEBUG_MODE = not DEBUG_MODE
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key in (pygame.K_LALT, pygame.K_RALT):
                    inventario1.inventory_open = not inventario1.inventory_open
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and botao_ativo == True:
                    if bau_perto:
                        bau_perto.inventario.inventory_open = not bau_perto.inventario.inventory_open

                if inventario1.inventory_open:
                    item = inventario1.get_item_at(event.pos)
                    if item:
                        dragging_item = item
                        dragging_from = "inventory1"

                if bau_perto:
                    if bau_perto.inventario.inventory_open:
                        item = bau_perto.inventario.get_item_at(event.pos)
                        if item:
                            dragging_item = item
                            dragging_from = "inventory2"

            if event.type == pygame.MOUSEBUTTONUP:
                if bau_perto:
                    if dragging_item:
                        if bau_perto.inventario.inventory_open and bau_perto.inventario.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory1":
                            inventario1.items.remove(dragging_item)
                            bau_perto.inventario.items.append(dragging_item)
                        elif inventario1.inventory_open and inventario1.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory2":
                            bau_perto.inventario.items.remove(dragging_item)
                            inventario1.items.append(dragging_item)
                        dragging_item = None
                        dragging_from = None

        contador += 1

        if cooldown_dash > 0:
            cooldown_dash += 1
            if cooldown_dash == 90:
                cooldown_dash = 0

        if player.dash:
            player.speed = 15
            dash += 1
            if dash == 10:
                player.dash = False
                player.speed = velocidade_anterior
                dash = 0

        player_hits = pygame.sprite.groupcollide(player.balas, inimigos, False, False)
        
        for inimigo in inimigos:
            enemy_hits = pygame.sprite.groupcollide(inimigo.balas, player_group, False, False)

            if len(enemy_hits) > 0:
                a = (enemy_hits.keys())
                inimigo.balas.remove(a)
                player.get_hit(2.5)

        if len(player_hits) > 0:
            a = (player_hits.keys())
            b = (player_hits.values())

            player.balas.remove(a)
            for value in b:
                for item in inimigos:
                    if value[0] == item:
                        item.get_hit(1)

        for inimigo in inimigos:
            xp.atualizar_xp(inimigo, 300)
            if inimigo.HP <= 0:
                inimigo.image = pygame.Surface((32, 32), pygame.SRCALPHA)
                inimigo.remover_todas_balas()
                inimigos.remove(inimigo)
                all_sprites.remove(inimigo)
            if inimigo.rect.colliderect(player.range_melee) and player.atacando_melee:
                if player.sheet_sec.tile_rect in [player.sheet_sec.cells[player.sheet_sec.action][-3], 
                                                player.sheet_sec.cells[player.sheet_sec.action][-2], 
                                                player.sheet_sec.cells[player.sheet_sec.action][-1]]:
                    inimigo.get_hit(1)
                    inimigo.rect.x, inimigo.rect.y = inimigo.old_pos_x, inimigo.old_pos_y

        old_x, old_y = player.rect.x, player.rect.y

        if dialogo_a_abrir:
            all_sprites.update(dialogo_a_abrir.texto_open)
        else:
            all_sprites.update(False)
        
        for wall in walls:
            if player.collision_rect.colliderect(wall):
                player.rect.x, player.rect.y = old_x, old_y
                break

        for npc in npcs:
            if player.collision_rect.colliderect(npc):
                player.rect.x, player.rect.y = old_x, old_y
                break
                
        camera.center = player.rect.center
        camera.left = max(0, camera.left)
        camera.top = max(0, camera.top)
        camera.right = min(MAP_WIDTH * TILE_SIZE, camera.right)
        camera.bottom = min(MAP_HEIGHT * TILE_SIZE, camera.bottom)

        click = pygame.mouse.get_pressed()[0]
        click_mouse_2 = pygame.mouse.get_pressed()[2]
        mouse_errado = pygame.mouse.get_pos()

        mouse_pos = [0, 0]
        if camera.left > 0:
            mouse_pos[0] = mouse_errado[0] + camera.left
        else:
            mouse_pos[0] = mouse_errado[0] - camera.left

        mouse_pos[1] = mouse_errado[1] + camera.top
    
        if not player.atacando_melee:
            if click:
                click_hold += 1
                player.atacando = True
                player.hold_arrow(mouse_pos, camera)
                player.atacando_melee = False
            elif click_mouse_2:
                player.atacando_melee = True
                player.hold_arrow(mouse_pos, camera)
            elif click_hold > 30:
                player.shoot(mouse_pos)
                click_hold = 0
                player.atacando = False
                player.atacando_melee = False
        else:
            contador_melee += 1
            if contador_melee != 7*7:
                player.atacando_melee = True
            else:
                contador_melee = 0
                player.sheet_sec.index = 0
                if not click_mouse_2:
                    player.atacando_melee = False
                else:
                    player.atacando_melee = True
                    player.hold_arrow(mouse_pos, camera)

        # Renderização
        screen.fill((0, 0, 0))
        
        # Desenhar tiles do mapa com offset da câmera
        for x, y, image in map_tiles:
            screen.blit(image, (x - camera.left, y - camera.top))

        for inimigo in inimigos:
            if inimigo.rect.colliderect(player.rect):
                player.get_hit(30)
                inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y
                player.rect.topleft = (old_x, old_y)
                inimigo.atacando_melee = True
                inimigo.frame_change = 4
            else:
                inimigo.atacando_melee = False
                inimigo.frame_change = 8

        player.draw(screen, camera)

        for inimigo in inimigos:
            inimigo.draw_balas(screen, camera)
        player.draw_balas(screen, camera)

        for inimigo in inimigos:
            inimigo.sheet.draw(screen, inimigo.rect.x - camera.left, inimigo.rect.y - camera.top)

        for bau in baus:
            screen.blit(bau.image, (bau.rect.x - camera.left, bau.rect.y - camera.top))

        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf', 48)
            render = font.render("Interagir", True, (0, 0, 0))
            screen.blit(interagir_bg, (300, 450))
            screen.blit(render, (325, 457))

        if boss.HP > 0:
            pygame.draw.rect(screen, (0, 0, 0), (200, 45, 400, 25))
            pygame.draw.rect(screen, (255, 0, 0), (200, 45, 80 * boss.HP, 25))
            fonte = pygame.font.Font('8-BIT WONDER.TTF', 30)
            text_surface = fonte.render("O Ligeiro", True, (255, 255, 255))
            screen.blit(text_surface, (288, 68, 400, 100))

            fonte2 = pygame.font.Font('8-BIT WONDER.TTF', 30)
            text_surface = fonte2.render("O Ligeiro", True, (0, 0, 0))
            screen.blit(text_surface, (290, 70, 400, 100))

        if inventario1.inventory_open:
            inventario1.draw_inventory(screen)
        if bau_perto:
            if bau_perto.inventario.inventory_open:
                bau_perto.image = bau_perto.bau_aberto
                bau_perto.inventario.draw_inventory(screen)
            else:
                bau_perto.image = bau_perto.bau_fechado

        if botao_ativo:
            inventario1.draw_button(screen)

        if dragging_item:
            inventario1.draw_dragging_item(screen, dragging_item)

        player.draw_health(screen)
        player.draw_stamina(screen)
        xp.render()

        for npc in npcs:
            npc.dialogo.coisa()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    inicio()