import pygame
import sys
import json
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem
from npcs import * 
from dialogo import *
from inimigo_teste import *
from inventario1 import Inventario
from boss import *
from bau import Bau
from XP import XP
from menu_status import Menu
from itens import Item
from game_over import Game_over
from menu_opcoes import MenuOpcoes

from cutscenes.tocar_cutscene import tocar_cutscene_cv2

from cutscenes.tocar_cutscene import tocar_cutscene_cv2

pause = False

def inicio():
    assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","assets"))

    # Adicionando o diretório pai ao sys.path
    sys.path.append(assets)

    som_andar = pygame.mixer.Sound("musicas/Efeitos sonoros/Passos.mp3")
    canal_andar = pygame.mixer.Channel(0)
    teclas_movimento = {pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d}
    teclas_pressionadas = set()
    
    som_balançar_espada = pygame.mixer.Sound("musicas/Efeitos sonoros/Balançar espada.mp3")
    canal_balançar_espada = pygame.mixer.Channel(1)
    cooldown_som_balançar_espada = 0
    delay_som_balançar_espada = 400
    primeiro_ataque_espada = 0

    som_carregar_arco = pygame.mixer.Sound("musicas/Efeitos sonoros/carregando_arco_flecha.mp3")
    canal_carregar_arco = pygame.mixer.Channel(2)

    som_atirar_flecha = pygame.mixer.Sound("musicas/Efeitos sonoros/Arco e flecha.mp3")
    canal_atirar_flecha = pygame.mixer.Channel(3)

    boss_parado = False
    global pause
    global cutscene_final_rodada
    cutscene_final_rodada = False
    
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
    TILE_SIZE = 48  # Tamanho final dos tiles na tela
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
        '60': (64, 112), '61': (80, 112), '62': (96, 112),
        '63': (112, 112), '64': (0, 128), '65': (16, 128),
        '66': (32, 128), '67': (48, 128), '68': (64, 128),
        '69': (80, 128), '70': (96, 128), '71': (112, 128),
        '72': (0, 144), '73': (16, 144), '74': (32, 144),
        '75': (48, 144), '76': (64, 144), '77': (80, 144),
        '78': (96, 144), '79': (112, 144), '80': (0, 160),
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
        layer_order = ['Floor', 'Walls', 'Walls sides', 'colunass','Miscs', 'colunas', 'Doors']
        
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
    
    atributos = {
            "ataque": 6.25,
            "defesa": 5.0,
            "vida_max": 20,
            "vida_atual": 10,
            "stamina": 6.25,
            "velocidade": 10
    }

    with open('save.json', 'r') as f:
        try:
            save_carregado = json.load(f)
            print(save_carregado)
        except:
            save_carregado = False
            print("ERRO AO CARREGAR SAVE")

    # Processar o mapa
    walls = process_map_for_collision(map_data)
    map_tiles = process_map_for_rendering(map_data)
    lista_1 = [9 for i in range(4)]
    lista_2 = [6 for i in range(8)]
    lista_3 = [6 for i in range(6)]
    lista_4 = [5 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    # Criar o jogador
    try:
        player_sprite_path = os.path.join(assets, 'personagem_carcoflecha(2).png')
        player_sprite_path2 = os.path.join(assets, 'sprites_ataque_espada.png')
        
        player_sprite = SpriteSheet(player_sprite_path, 0, 514, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
        player_sprite_ataques = SpriteSheet(player_sprite_path2, 18, 38, 128, 128, 12,[6,6,6,6], (255,255,255))
        #######
        # ACIMA ALTERA, MAIS OU MENOS, A POSIÇÃO DO SPRITE DO JOGADOR EM RELAÇÃO NA ONDE ELE ESTÁ
        if save_carregado:
            # print("SAVE CARREGADO")
            player = Personagem(player_sprite, save_carregado['atributos'][0], save_carregado['atributos'][1], save_carregado['atributos'][2], save_carregado['atributos'][3], save_carregado['atributos'][4],save_carregado['atributos'][5],player_sprite_ataques)

            itens_carregados = []
            for item in save_carregado['itens']:
                novo_item = Item(item[0],item[1],item[2],item[3],player)
                itens_carregados.append(novo_item)
            inventario1 = Inventario((50, 50, 50), 50, [itens_carregados[i] for i in range(len(itens_carregados))])
            
            xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT,save_carregado['nivel'],save_carregado['pontos_disponiveis'])
            menu = Menu(save_carregado['menu_valores']['ataque'],save_carregado['menu_valores']['defesa'],save_carregado['menu_valores']['vida'],save_carregado['menu_valores']['stamina'],save_carregado['menu_valores']['velocidade'],save_carregado['menu_atributos']['ataque'],save_carregado['menu_atributos']['defesa'],save_carregado['menu_atributos']['vida'],save_carregado['menu_atributos']['stamina'],save_carregado['menu_atributos']['velocidade'], player)
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    player.rect.x, player.rect.y = 1072, 1280

    # Configuração da câmera
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    spritesheet_gabriel = SpriteSheet('gabrielFase2.png', 0, 522, 64, 64, 4, lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    boss = Boss2(player.rect, player, 1200, 400, True, spritesheet_gabriel, 30, 300, 20)

    inimigos = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_group.add(player)
    all_sprites.add(boss)
    inimigos.add(boss)

    contador = 0
    click_hold = 0
    interagir_bg = pygame.image.load(os.path.join(assets, "caixa_dialogo_pequena2.png"))
    npcs = pygame.sprite.Group()
    baus = pygame.sprite.Group()
    dialogo_group = []

    # Configurações de inventário
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 140, 60)
    dragging_item = None
    dragging_from = None

    contador_ataque_melee = 0
    dash = 0
    cooldown_dash = 0
    velocidade_anterior = 0
    contador_melee = 0

    # Game loop
    clock = pygame.time.Clock()
    running = True
    menu_opcoes = MenuOpcoes(SCREEN_WIDTH, SCREEN_HEIGHT, screen, running)

    dash = 0
    cooldown_dash = 0
    velocidade_anterior = 0

    while menu_opcoes.rodando:
        if player.HP <= 0:
            running = False
            Game_over(inicio)
            menu_opcoes.rodando = False
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
                # ativar efeitos sonoros
                if event.key in teclas_movimento and not menu_opcoes.pausado:
                    teclas_pressionadas.add(event.key)
                    
                    if not canal_andar.get_busy():
                        som_andar.set_volume(menu_opcoes.volume_efeitos)
                        canal_andar.play(som_andar, loops=-1)
                if event.key == pygame.K_w:
                    player.nova_direcao = True
                elif event.key == pygame.K_s:
                    player.nova_direcao = True
                elif event.key == pygame.K_a:
                    player.nova_direcao = True
                elif event.key == pygame.K_d:
                    player.nova_direcao = True
                elif event.key == pygame.K_q:
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
                            if bau_perto.inventario.inventory_open == True:
                                if inventario1.inventory_open == False:
                                    pass
                                else:
                                    inventario1.inventory_open = not inventario1.inventory_open
                            else:
                                inventario1.inventory_open = True
                            bau_perto.inventario.inventory_open = not bau_perto.inventario.inventory_open
                elif event.key == pygame.K_z:
                    DEBUG_MODE = not DEBUG_MODE
                elif event.key == pygame.K_p:
                    pause = not pause

                if event.key == pygame.K_m:
                    xp.show_menu = not xp.show_menu
                    if xp.show_menu:
                        menu.valores_copy = menu.valores.copy()

                elif event.key in (pygame.K_LALT, pygame.K_RALT):
                    inventario1.inventory_open = not inventario1.inventory_open
                # elif event.key == pygame.K_ESCAPE:
                #     running = False

                elif event.key == pygame.K_DOWN and inventario1.item_index < len(inventario1.items)-1 and not menu_opcoes.pausado:
                    inventario1.item_index +=1
                elif event.key == pygame.K_UP and inventario1.item_index > 0:
                    inventario1.item_index -=1

                elif event.key == pygame.K_RETURN:
                    if inventario1.inventory_open:
                        if inventario1.items[inventario1.item_index].tipo != 'consumivel':
                            inventario1.items[inventario1.item_index].equipar()
                        else:
                            inventario1.items[inventario1.item_index].utilizar()
                            inventario1.remove(inventario1.items[inventario1.item_index])

            elif event.type == pygame.KEYUP and not event.type == pygame.KEYDOWN:
                if event.key in teclas_movimento:
                    teclas_pressionadas.discard(event.key)
                    if len(teclas_pressionadas) == 0:
                        canal_andar.stop()
            menu_opcoes.processar_eventos(event)

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
                # Handle mouse button release

                #print(inventario1.pressed_counter)
                
                if event.button == 1:
                    if bau_perto:
                        if dragging_item:
                            if bau_perto.inventario.inventory_open and bau_perto.inventario.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory1":
                                inventario1.remove(dragging_item)
                                bau_perto.inventario.items.append(dragging_item)
                            elif inventario1.inventory_open and inventario1.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory2":
                                bau_perto.inventario.remove(dragging_item)
                                inventario1.items.append(dragging_item)
                            # elif inventario1.inventory_open and inventario1.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory1":
                            #     inventario1.items.append(dragging_item)
                            dragging_item = None
                            dragging_from = None
                            if bau_perto.inventario.inventory_open and inventario1.pressed_counter <= 10:
                                if inventario1.get_item_at(event.pos) == None:
                                    pass
                                else:
                                    bau_perto.inventario.remove(inventario1.get_item_at(event.pos))

                    elif inventario1.inventory_open and inventario1.pressed_counter < 10:
                        if inventario1.get_item_at(event.pos) == None:
                            inventario1.inventory_open = False
                        elif inventario1.get_item_at(event.pos).tipo != 'consumivel':
                            inventario1.get_item_at(event.pos).equipar()
                        else:
                            inventario1.get_item_at(event.pos).utilizar()
                            inventario1.remove(inventario1.get_item_at(event.pos))

                    if dragging_item:
                        dragging_item = None

                elif event.button == 3:
                    if inventario1.inventory_open and inventario1.inventory_rect.collidepoint(event.pos):
                        inventario1.remove(inventario1.get_item_at(event.pos))
                    dragging_item = None
                #print("DNSKLANDKLSANDLKASNDKLSANKLDNSAKL")
                inventario1.pressed_counter = 0

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
                player.get_hit(5.5)

        if len(player_hits) > 0:
            a = (player_hits.keys())
            b = (player_hits.values())

            player.balas.remove(a)
            for value in b:
                for item in inimigos:
                    if value[0] == item:
                        if player.dano>=20:
                            item.get_hit(2)
                        elif player.dano>=10:
                            item.get_hit(1.5)
                        else:
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

        if inventario1.inventory_open or xp.show_menu or menu_opcoes.pausado:
            all_sprites.update(True)
        elif dialogo_a_abrir:
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

        # CASO NÃO FIQUE LEGAL FUTURAMENTE, TROQUE PARA 1        
        lerp_factor = 0.1  # ajuste esse valor conforme necessário (0 < lerp_factor < 1)
        target_center = player.rect.center
        new_center_x = camera.centerx + (target_center[0] - camera.centerx) * lerp_factor
        new_center_y = camera.centery + (target_center[1] - camera.centery) * lerp_factor
        camera.center = (new_center_x, new_center_y)
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
            if click and not menu_opcoes.pausado and not inventario1.inventory_open:
                click_hold += 1
                if not canal_carregar_arco.get_busy() and click_hold <= 30 and not menu_opcoes.pausado:
                    som_carregar_arco.set_volume(menu_opcoes.volume_efeitos)
                    canal_carregar_arco.play(som_carregar_arco, loops=0)
                elif click_hold > 30:
                    canal_carregar_arco.stop()
                player.atacando = True
                player.hold_arrow(mouse_pos,camera)
                player.atacando_melee = False
            elif click_mouse_2:
                player.atacando_melee = True
                player.hold_arrow(mouse_pos,camera)
                cooldown_som_balançar_espada = pygame.time.get_ticks()
            elif click_hold > 30:
                player.shoot(mouse_pos)
                if not canal_atirar_flecha.get_busy() and not menu_opcoes.pausado:
                    som_atirar_flecha.set_volume(menu_opcoes.volume_efeitos - 0.9)
                    canal_atirar_flecha.play(som_atirar_flecha, loops=0)
                click_hold = 0
                player.atacando = False
                player.atacando_melee = False
            elif click_hold <=30:
                player.atacando = False
                click_hold = 0
        else:
            if contador_melee == 0:
                cooldown_som_balançar_espada = pygame.time.get_ticks()
                primeiro_ataque_espada = 0

            contador_melee += 1

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - cooldown_som_balançar_espada >= delay_som_balançar_espada and primeiro_ataque_espada == 0 and not menu_opcoes.pausado:
                som_balançar_espada.set_volume(menu_opcoes.volume_efeitos)
                canal_balançar_espada.play(som_balançar_espada, loops=0)
                cooldown_som_balançar_espada = tempo_atual
                primeiro_ataque_espada = 1

            elif tempo_atual - cooldown_som_balançar_espada >= delay_som_balançar_espada + 335 and primeiro_ataque_espada == 1 and not menu_opcoes.pausado:
                som_balançar_espada.set_volume(menu_opcoes.volume_efeitos)
                canal_balançar_espada.play(som_balançar_espada, loops=0)
                cooldown_som_balançar_espada = tempo_atual

            if contador_melee != 7*7:
                player.atacando_melee = True
            else:
                contador_melee = 0
                player.sheet_sec.index = 0
                if not click_mouse_2:
                    player.atacando_melee = False
                    primeiro_ataque_espada = 0
                else:
                    player.atacando_melee = True
                    player.hold_arrow(mouse_pos,camera)

        # Renderização
        screen.fill((0, 0, 0))
        
        # Desenhar tiles do mapa com offset da câmera
        for x, y, image in map_tiles:
            screen.blit(image, (x - camera.left, y - camera.top))

        for inimigo in inimigos:
            if inimigo.rect.colliderect(player.rect):
                player.get_hit(10+player.defesa)
                player.knockbacked(inimigo.dx, inimigo.dy)
                # inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y
                # player.rect.topleft = (old_x, old_y)
                inimigo.atacando_melee = True
                inimigo.frame_change = 4
            else:
                inimigo.atacando_melee = False
                inimigo.frame_change = 8

        player.draw(screen, camera)
        boss.draw_raios(screen, camera)

        for inimigo in inimigos:
            inimigo.draw_balas(screen, camera)
        player.draw_balas(screen, camera)

        for inimigo in inimigos:
            inimigo.sheet.draw(screen, inimigo.rect.x - camera.left, inimigo.rect.y - camera.top)

        for bau in baus:
            screen.blit(bau.image, (bau.rect.x - camera.left, bau.rect.y - camera.top))

        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            font = pygame.font.Font(os.path.join(assets, '8bitOperatorPlus8-Regular.ttf'),27)
            render = font.render("Interagir", True, (0,0,0))
            screen.blit(interagir_bg,(300,450))
            screen.blit(render,(325,457))

        if boss.HP > 0:
            pygame.draw.rect(screen,(0,0,0),(280,45,700,25))
            pygame.draw.rect(screen,(255,0,0),(280,45,35*boss.HP,25))
            fonte = pygame.font.Font(os.path.join(assets, '8-BIT WONDER.TTF'),30)
            text_surface = fonte.render("O Professor", True, (0, 0, 0))
            screen.blit(text_surface, (483,68,400,100))

            fonte2 = pygame.font.Font(os.path.join(assets, '8-BIT WONDER.TTF'),30)
            text_surface = fonte2.render("O Professor", True, (255, 255, 255))
            screen.blit(text_surface, (485,70,400,100))

        else:
            if not cutscene_final_rodada:
                tocar_cutscene_cv2('cutscenes/cutscene_final.mp4', 'cutscenes/cutscene_boss1.mp3', screen)
                cutscene_final_rodada = True
                running = False
                menu_opcoes.rodando = False
                from main import g
                g

        if inventario1.inventory_open:
            inventario1.draw_inventory(screen)
        if bau_perto:
            if bau_perto.inventario.inventory_open:
                bau_perto.image = bau_perto.bau_aberto
                bau_perto.inventario.draw_inventory(screen)
            else:
                bau_perto.image = bau_perto.bau_fechado

        # if botao_ativo:
        #     inventario1.draw_button(screen)

        if xp.show_menu and menu.tamanho_menu_img_x < 600 and menu.tamanho_menu_img_y < 400:
            menu.tamanho_menu_img_x += 30  # Ajuste a velocidade do zoom
            menu.tamanho_menu_img_y += 20
            menu.menu_img = pygame.transform.scale(menu.menu_img_original, (menu.tamanho_menu_img_x, menu.tamanho_menu_img_y))
        elif not xp.show_menu and menu.tamanho_menu_img_x > 0 and menu.tamanho_menu_img_y > 0:
            menu.tamanho_menu_img_x = max(0, menu.tamanho_menu_img_x - 30)
            menu.tamanho_menu_img_y = max(0, menu.tamanho_menu_img_y - 20)

            if menu.tamanho_menu_img_x > 0 and menu.tamanho_menu_img_y > 0:
                menu.menu_img = pygame.transform.scale(menu.menu_img_original, (menu.tamanho_menu_img_x, menu.tamanho_menu_img_y))

        if menu_opcoes.pausado:
            menu_opcoes.atualizar()
            menu_opcoes.desenhar(screen)
                
        # Atualiza o jogo se o menu NÃO estiver aberto
        if xp.show_menu:
            # Exibe o menu na tela 
            screen.blit(menu.menu_img,((WIDTH // 2) - (menu.tamanho_menu_img_x // 2),(HEIGHT // 2) - (menu.tamanho_menu_img_y // 2)))
            if menu.tamanho_menu_img_x > 500 and menu.tamanho_menu_img_y > 333:
                # Posição do menu
                menu.desenhar_valores(screen, xp.font_nivel, xp.text_nivel, xp.nivel, xp.pontos_disponiveis)
                menu.atualizar_sprites()
                menu.desenhar_botoes(screen)
                menu.resetar_botoes()

        if menu_opcoes.pausado:
            menu_opcoes.atualizar()
            menu_opcoes.desenhar(screen)

        if dragging_item:
            inventario1.draw_dragging_item(screen, dragging_item)

        if not menu_opcoes.pausado:
            player.draw_health(screen)
            player.draw_stamina(screen)
            if not dialogo_a_abrir:
                xp.render()
            else:
                if dialogo_a_abrir.texto_open == False:
                    xp.render()

        for npc in npcs:
            npc.dialogo.coisa()
        pygame.display.flip()

if __name__ == "__main__":
    inicio()