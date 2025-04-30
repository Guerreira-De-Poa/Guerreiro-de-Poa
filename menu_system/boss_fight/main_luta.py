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
from itens import Item
from game_over import Game_over

from XP import XP
from menu_status import Menu

from menu_opcoes import MenuOpcoes

pause = False
pygame.mixer.music.stop()


def inicio():
    pygame.mixer.music.load("musicas/In the Hall of the Mountain King.mp3")
    pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop

    # Efeitos Sonoros
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
        
    boss_parado=False
    global pause
    # Inicialização do Pygame
    pygame.init()

    # Configurações da tela
    # Configurações da tela
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
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
    '33': (64, 256), '34': (128, 256), '35': (192, 256),
    '36': (256, 256), '37': (320, 256), '38': (384, 256),
    '39': (448, 256), '40': (0, 320), '41': (64, 320),
    '42': (128, 320), '43': (192, 320), '44': (256, 320),
    '45': (320, 320), '46': (384, 320), '47': (448, 320),
    '48': (0, 384), '49': (64, 384), '50': (128, 384),
    '51': (192, 384), '52': (256, 384), '53': (320, 384),
    '54': (384, 384), '55': (448, 384), '56': (0, 448),
    '57': (64, 448), '58': (128, 448), '59': (192, 448),
    '60': (256, 448),
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
        layer_order = ['Background', 'colisao', 'Sand', 'Cliff', 'Rocks', 'Grass', 'Miscs']
        
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
    lista_1 = [7 for i in range(4)]
    lista_2 = [8 for i in range(4)]
    lista_3 = [6 for i in range(8)]
    lista_4 = [13 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    # Criar o jogador
    try:
        player_sprite_path = os.path.join(current_dir, '..', '..', 'personagem_carcoflecha(2).png')
        player_sprite_path2 = os.path.join(current_dir, '..', '..', 'sprites_ataque_espada.png')
        
        player_sprite = SpriteSheet(player_sprite_path, 0, 514, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
        player_sprite_ataques = SpriteSheet(player_sprite_path2, 18, 38, 128, 128, 12,[6,6,6,6], (255,255,255))
        #######
        # ACIMA ALTERA, MAIS OU MENOS, A POSIÇÃO DO SPRITE DO JOGADOR EM RELAÇÃO NA ONDE ELE ESTÁ
        if save_carregado:
            print("SAVE CARREGADO")
            player = Personagem(player_sprite, save_carregado['atributos'][0], save_carregado['atributos'][1], save_carregado['atributos'][2], save_carregado['atributos'][3], save_carregado['atributos'][4],save_carregado['atributos'][5],player_sprite_ataques)

            itens_carregados = []
            for item in save_carregado['itens']:
                novo_item = Item(item[0],item[1],item[2],item[3],player)
                itens_carregados.append(novo_item)
            inventario1 = Inventario((50, 50, 50), 50, [itens_carregados[i] for i in range(len(itens_carregados))])
            
            xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT,save_carregado['nivel'],save_carregado['pontos_disponiveis'])
            menu = Menu(5, 5, 5, 5, 5, 6.25, 5.0, 20, 6.25, 10.0, player)
        else:
            print("SAVE NAO CARREGADO")
            player = Personagem(player_sprite, atributos["ataque"], atributos["defesa"], atributos["vida_max"],atributos['vida_atual'], atributos["stamina"], atributos["velocidade"],player_sprite_ataques)
            inventario1 = Inventario((50, 50, 50), 50, [])
            xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            menu = Menu(5, 5, 5, 5, 5, 6.25, 5.0, 20, 6.25, 10.0, player)
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    menu = Menu(5, 5, 5, 5, 5, 6.25, 5.0, 20, 6.25, 10.0, player)

    # Posicionar o jogador em uma posição válida no mapa

    player.rect.x,player.rect.y = 1535,1320

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
    menu_opcoes = MenuOpcoes(SCREEN_WIDTH, SCREEN_HEIGHT, screen, running)

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    spritesheet_inimigo_arco2 = SpriteSheet('boss_agua(atqs_esp).png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))

    boss = Boss1(player.rect,player,1220,1000,True,spritesheet_inimigo_arco2, 30, 300, 200)


    inimigos = pygame.sprite.Group()

    player_group = pygame.sprite.Group()

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_group.add(player)

    all_sprites.add(boss)
    inimigos.add(boss)

    # boss2 = Boss1(player.rect,player,400,400,True,spritesheet_inimigo_arco)
    # all_sprites.add(boss2)
    # inimigos.add(boss2)

    contador = 0

    click_hold = 0

    interagir_bg = pygame.image.load("caixa_dialogo_pequena.jpg")

    npcs = pygame.sprite.Group()

    baus = pygame.sprite.Group()

    dialogo_group = []

    #CONFIG INVENTARIO

    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Botão para abrir o inventário 2
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 140, 60)

    # Variáveis de controle de arrastar itens
    dragging_item = None
    dragging_from = None

    # Criar as instâncias dos inventários

    print(boss.local_a_mover)

    contador_ataque_melee = 0

    dash = 0
    cooldown_dash = 0
    velocidade_anterior = 0

    contador_melee = 0

    def salvar_game():
        itens = []

        for item in inventario1.items:
            item_ = [item.tipo,item.nome,item.atributos,item.equipado]
            itens.append(item_)

        Dicionario_para_save = {
            
            'atributos':[
                player.dano,
                player.defesa,
                player.MAX_HP,
                player.HP,
                player.max_stamina,
                player.velocidade_corrida,
            ],

            'itens': itens,

            'menu_valores': menu.valores,

            'menu_atributos': menu.atributos,

            'nivel': xp.nivel,

            'pontos_disponiveis': xp.pontos_disponiveis

        }
            # Salvar
        with open("save.json", "w") as f:
            json.dump(Dicionario_para_save, f, indent=4)

    while menu_opcoes.rodando:
        pygame.mixer.music.set_volume(menu_opcoes.volume_musica)  # 50% do volume máximo

        if player.HP <= 0:
            running = False
            Game_over(inicio)
            menu_opcoes.rodando = False
            
        #print("LEN = ",len([player.sheet.action]),"NUM = ",player.sheet.index % len(player.sheet.cells[player.sheet.action]))
        # print(player.sheet.action)
        # print(player.sheet.cells[0])
        
        player.atualizar_stamina()

        bau_perto = False

        for bau in baus:
            if bau.interagir_rect.colliderect(player.rect):
                bau_perto = bau

        clock.tick(60) # Delta time em segundos

        botao_ativo = False

        dialogo_a_abrir = False

        screen.fill((100, 100, 100))  # Preenche o fundo com uma cor sólida

        dialogo_hitbox =  False

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
                    bau_perto.inventario.inventory_open = False

        # Obter teclas pressionadas
        keys = pygame.key.get_pressed()
        
        # Resetar direção
        player.direction = None
        player.nova_direcao = False

                # Adicione no início do código, com outras configurações
        DEBUG_MODE = True  # Mude para False para desativar o deb

        if keys[pygame.K_w]:
            player.direction = 'UP'
        elif keys[pygame.K_s]:
            player.direction = 'DOWN'
        elif keys[pygame.K_a]:
            player.direction = 'LEFT'
        elif keys[pygame.K_d]:
            player.direction = 'RIGHT'
        else:
            player.direction = None  # Nenhuma direção se nenhuma tecla for pressionada

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
                elif keys[pygame.K_z]:
                    DEBUG_MODE = not DEBUG_MODE
                elif event.key == pygame.K_p:
                    pause = not pause

                    #COMANDOS INVENTARIO
                elif event.key in (pygame.K_LALT, pygame.K_RALT):
                    inventario1.inventory_open = not inventario1.inventory_open
                # elif event.key == pygame.K_ESCAPE:
                #     running = False

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

        contador+=1

        #print(player.dash)

        if cooldown_dash>0:
            cooldown_dash+=1
            if cooldown_dash == 90:
                cooldown_dash = 0

        if player.dash == True:
            print(cooldown_dash)
            player.speed = 15
            dash+=1
            if dash == 10:
                player.dash = False
                player.speed = velocidade_anterior
                dash=0

        player_hits =  pygame.sprite.groupcollide(player.balas,inimigos, False, False)
        
        for inimigo in inimigos:
            enemy_hits = pygame.sprite.groupcollide(inimigo.balas, player_group, False, False)

            if len(enemy_hits)>0:
                a = (enemy_hits.keys())
                inimigo.balas.remove(a)
                
                player.get_hit(1)

        if len(player_hits) > 0:
            a = (player_hits.keys())
            b = (player_hits.values())

            player.balas.remove(a)
            for value in b:
                for item in inimigos:
                    if value[0] == item:
                        item.get_hit(1)
            i = 0
            for inimigo in inimigos:
                i+=1

        

        for inimigo in inimigos:
            xp.atualizar_xp(inimigo, 300)
            if inimigo.HP <= 0:
                inimigo.morto = True
                # inimigo.image = pygame.Surface((32, 32), pygame.SRCALPHA)
                # inimigo.remover_todas_balas()
                # inimigos.remove(inimigo)
                # all_sprites.remove(inimigo)
            if inimigo.rect.colliderect(player.range_melee) and player.atacando_melee:
                if player.sheet_sec.tile_rect in [player.sheet_sec.cells[player.sheet_sec.action][-3],player.sheet_sec.cells[player.sheet_sec.action][-2],player.sheet_sec.cells[player.sheet_sec.action][-1]]:
                    print(True)
                    inimigo.get_hit(1)
                    #inimigo.rect.x, inimigo.rect.y = inimigo.old_pos_x, inimigo.old_pos_y
            
        # Salvar a posição anterior para colisão
        old_x, old_y = player.rect.x, player.rect.y
        

        # Atualizar jogador
        #all_sprites.update(pause) ######## pause maroto

        if inventario1.inventory_open or xp.show_menu or menu_opcoes.pausado:
            all_sprites.update(True)
        elif dialogo_a_abrir:
            all_sprites.update(dialogo_a_abrir.texto_open)
        else:
            all_sprites.update(False)
        
        # Verificar colisões com retângulo customizado
        for wall in walls:
            if player.collision_rect.colliderect(wall):
                # Colisão detectada, voltar para a posição anterior
                player.rect.x, player.rect.y = old_x, old_y
                break

        for npc in npcs:
            if player.collision_rect.colliderect(npc):
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

        click = pygame.mouse.get_pressed()[0]

        click_mouse_2 = pygame.mouse.get_pressed()[2]

        mouse_errado = pygame.mouse.get_pos()

        mouse_pos =[0,0]

        if camera.left > 0:
            mouse_pos[0] = mouse_errado[0]+camera.left
        else:
            mouse_pos[0] = mouse_errado[0]-camera.left

        mouse_pos[1] = mouse_errado[1]+camera.top
    
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
        screen.fill((0, 0, 0))  # Fundo preto
        
        # Desenhar o mapa (apenas tiles visíveis)
        for x, y, image in map_tiles:
            # Verificar se o tile está dentro da visão da câmera
            if (camera.left - TILE_SIZE <= x < camera.right and 
                camera.top - TILE_SIZE <= y < camera.bottom):
                screen.blit(image, (x - camera.left, y - camera.top))

        for inimigo in inimigos:
            if inimigo.rect.colliderect(player.rect):
                if not player.ivuln:
                    player.get_hit(1)
                    inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y
                    player.rect.topleft = (old_x,old_y)
                inimigo.atacando_melee = True
                inimigo.frame_change = 4
            else:
                inimigo.atacando_melee = False
                inimigo.frame_change = 8

        player.draw(screen, camera)
        #print(player.rect.x)

        for inimigo in inimigos:
            inimigo.draw_balas(screen,camera)
        player.draw_balas(screen,camera)

        for inimigo in inimigos:
            if not inimigo.morto:
                inimigo.sheet.draw(screen, inimigo.rect.x - camera.left, inimigo.rect.y - camera.top)
            else:
                inimigo.sheet.action = 2
                inimigo.morte_counter += 1
                if inimigo.morte_counter % 4 == 0:
                    inimigo.sheet.draw(screen, (inimigo.rect.x - camera.left)-5, inimigo.rect.y - camera.top)
                else:
                    inimigo.sheet.draw(screen, inimigo.rect.x - camera.left, inimigo.rect.y - camera.top)
            if inimigo.morte_counter == 100:
                inimigo.image = pygame.Surface((32, 32), pygame.SRCALPHA)
                inimigo.remover_todas_balas()
                inimigos.remove(inimigo)
                all_sprites.remove(inimigo)
            
        # for vida in range(player.HP):
        #     screen.blit(vida_imagem,(18 + 32*vida,0))

        for bau in baus:
            screen.blit(bau.image, (bau.rect.x - camera.left, bau.rect.y - camera.top))

        if player.rect.y > 1500:
            if boss.HP > 0:
                player.rect.y = 1500
            else:
                running = False
                from mapa_main.main_mapa import inicio as VilaInicio
                salvar_game()
                VilaInicio(True)


        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            
            font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf',48)
            render = font.render("Interagir", True, (0,0,0))
            screen.blit(interagir_bg,(300,450))
            screen.blit(render,(325,457))

        if boss.morte_counter < 100:
            pygame.draw.rect(screen,(0,0,0),(280,45,700,25))
            pygame.draw.rect(screen,(255,0,0),(280,45,140*boss.HP,25))
            fonte = pygame.font.Font('8-BIT WONDER.TTF',30)
            text_surface = fonte.render("O Ligeiro", True, (255, 255, 255))
            screen.blit(text_surface, (508,68,400,100))

            fonte2 = pygame.font.Font('8-BIT WONDER.TTF',30)
            text_surface = fonte2.render("O Ligeiro", True, (0, 0, 0))
            screen.blit(text_surface, (510,70,400,100))
        elif boss.morte_counter == 100:
            boss.morte_counter+=1

            espada = Item('arma', 'Espada',{'dano': 5},False,player)
            armadura = Item('armadura', 'Armadura',{'defesa': 0.5},False,player)
            pocao = Item('consumivel', 'Poção', {'vida': 10},False,player)

            bau_saida = Bau(screen,1540,885,[espada,armadura,pocao])

            baus.add(bau_saida)
            ##############

            # ADICIONAMOS A FUNÇÃO DE FIM DE JOGO, O BOSS MORREU

            ##############

            # pygame.mixer.music.stop()
            # running = False
            # screen.fill((0, 0, 0))
            # fonte = pygame.font.Font('8-BIT WONDER.TTF',30)
            # text_surface = fonte.render("O Ligeiro", True, (255, 255, 255))
            # screen.blit(text_surface, (288,68,400,100))

            # fonte2 = pygame.font.Font('8-BIT WONDER.TTF',30)
            # text_surface = fonte2.render("O Ligeiro", True, (0, 0, 0))
            # screen.blit(text_surface, (290,70,400,100))
            # pygame.display.flip()
            # pygame.time.delay(500)
            # from mapa_main.main_mapa import inicio as mapa_principal # PARA CORRIGIR O PROBLEMA DE IMPORTAÇÃO CIRCULAR
            # mapa_principal()

        # Desenhar os inventários e o botão
        if inventario1.inventory_open:
            inventario1.draw_inventory(screen)
        if bau_perto:
            if bau_perto.inventario.inventory_open:
                bau_perto.image = bau_perto.bau_aberto
                bau_perto.inventario.draw_inventory(screen)
            else:
                bau_perto.image = bau_perto.bau_fechado

        # if botao_ativo:
        #     inventario1.draw_button(screen)  # Agora o método `draw_button` é da classe Inventario1
        if menu_opcoes.pausado:
            menu_opcoes.atualizar()
            menu_opcoes.desenhar(screen)

        if dragging_item:
            inventario1.draw_dragging_item(screen, dragging_item)  # Agora o método `draw_dragging_item` é da classe Inventario1

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