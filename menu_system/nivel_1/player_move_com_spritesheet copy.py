import pygame
import sys
import json
import os

pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Adicionando o diretório pai ao sys.path
sys.path.append(pasta_pai)

# Agora podemos importar diretamente a função 'inicio' do arquivo 'main_luta.py'
from boss_fight.main_luta import inicio as boss_fight

# Chamando a função importada

from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem

from npcs import * 
from dialogo import *
from inimigo_teste import *
from inventario1 import Inventario
from boss import Boss1
from bau import Bau

from XP import XP

pause = False

def inicio():
    
    boss_parado=False
    global pause
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

    xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Classe para carregar a spritesheet do mapa
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

    xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

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
    lista_1 = [7 for i in range(4)]
    lista_2 = [6 for i in range(4)]
    lista_3 = [7 for i in range(8)]
    lista_4 = [13 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    # Criar o jogador
    try:
        player_sprite_path = os.path.join(current_dir, '..', '..', 'personagem_carcoflecha.png')
        player_sprite = SpriteSheet(player_sprite_path, 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
        #######
        # ACIMA ALTERA, MAIS OU MENOS, A POSIÇÃO DO SPRITE DO JOGADOR EM RELAÇÃO NA ONDE ELE ESTÁ 
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

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    vida_imagem = pygame.image.load('love-always-wins(1).png')

    spritesheet_inimigo_arco_png = pygame.image.load("inimigo_com_arco.png")
    spritesheet_inimigo_arco = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco0 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco1 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco2 = SpriteSheet('inimigo_com_arco.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco3 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco4 = SpriteSheet('inimigo_com_arco.png', 0, 522, 64, 64, 4,lista_1+lista_2+lista_3+lista_4+lista_5, (0, 0, 0))

    inimigos = pygame.sprite.Group()

    player_group = pygame.sprite.Group()

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_group.add(player)

    #all_sprites.add(enemy0, enemy1, enemy2, enemy3)
    #inimigos.add(enemy0, enemy1, enemy2, enemy3)

    # boss2 = Boss1(player.rect,player,400,400,True,spritesheet_inimigo_arco)
    # all_sprites.add(boss2)
    # inimigos.add(boss2)

    contador = 0

    click_hold = 0

    interagir_bg = pygame.image.load("caixa_dialogo_pequena.jpg")

    omori = pygame.image.load('npc.png')

    texto = {
        'personagem':'Morador de Poá',
        'texto_1':['Ei você', 'Você parece um guerreiro formidável', 'Por favor nos ajude', 'Nossa vila está sendo invadida'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
        }

    texto_1 = {
        'personagem':'Morador de Poá',
        'texto_1':['Obrigado por nos salvar', 'Fale com o carinha que mora logo ali','Ele viu onde o chefe dos invasores fica', 'Se você derrotar o chefe', 'Eles nunca irão nos invadir de novo' ],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
        }

    texto_2 = {
        'personagem':'Morador de Poá',
        'texto_1':['Você foi o guerreiro que nos salvou certo?', 'Muito obrigado', 'Eu posso te levar ao chefe deles', 'Isso fará com que eles desistam de nos invadir'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Me leve até lá']
        }
    
    ########### 
    # de alguma forma, agora te que deixar o dicionario texto...
    ###########

    npc0 = NPC(omori,screen,1248,545,texto_2, 2)
    npc1 = NPC(omori,screen,2115, 2150,texto, 3)

    all_sprites.add(npc0,npc1)
    npcs = pygame.sprite.Group()
    npcs.add(npc0,npc1) 

    dialogo_group = []

    for npc in npcs:
        if npc.dialogo:
            dialogo_group.append(npc.dialogo)

    #################

    # TEORICAMENTE, caso for true, começa a missão
    # for npc in npcs:
    #     if npc.dialogo.missao_ativada:
    #         print("ok")

    #################

    print(dialogo_group)
    print(f"Total de tiles carregados: {len(map_tiles)}")

    #CONFIG INVENTARIO

    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Botão para abrir o inventário 2
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 140, 60)

    # Variáveis de controle de arrastar itens
    dragging_item = None
    dragging_from = None

    # Criar as instâncias dos inventários
    inventario1 = Inventario((50, 50, 50), 50, ["Espada", "Poção", "Escudo"])
    inventario2 = Inventario((0, 100, 0), 400)

    baus = pygame.sprite.Group()

    iterado_teste = 0

    enemy0 = Inimigo(player.rect, player, 200,100, False,spritesheet_inimigo_arco)
    enemy1 = Inimigo(player.rect, player, 100,754, False,spritesheet_inimigo_arco1)
    enemy2 = Inimigo(player.rect, player, 570,102, True,spritesheet_inimigo_arco2)
    enemy3 = Inimigo(player.rect, player, 650,266, False,spritesheet_inimigo_arco3)
    all_sprites.add(enemy0, enemy1, enemy2, enemy3)
    inimigos.add(enemy0, enemy1, enemy2, enemy3)

    while running:


        missao_1 = npc1.dialogo.missao_ativada
        missao_2 = npc0.dialogo.missao_ativada

        if missao_2 == True:
            running = False

        if missao_1 == True and iterado_teste == 0:
            iterado_teste+=1
            npc.dialogo.frase = ''
            npc1.dialogo.texto = texto_1
            npc1.dialogo.iter_texto = 0
            npc1.dialogo.texto_index = 0
            npc1.dialogo.letra_index = 0

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
                if event.key == pygame.K_w:
                    player.nova_direcao = True
                elif event.key == pygame.K_s:
                    player.nova_direcao = True
                elif event.key == pygame.K_a:
                    player.nova_direcao = True
                elif event.key == pygame.K_d:
                    player.nova_direcao = True
                elif event.key == pygame.K_LSHIFT:
                    player.correr()
                elif event.key == pygame.K_SPACE:
                    if dialogo_a_abrir:
                        dialogo_a_abrir.trocar_texto()
                    elif botao_ativo:
                        if bau_perto:
                            bau_perto.inventario.inventory_open = not bau_perto.inventario.inventory_open
                elif keys[pygame.K_z]:
                    DEBUG_MODE = not DEBUG_MODE
                elif event.key == pygame.K_p:
                    pause = not pause

                    #COMANDOS INVENTARIO
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

        if contador % 70 == 0:
            for inimigo in inimigos:
                if inimigo.ataque:
                    inimigo.atacar()
                pass
        # if contador % 500 == 0:
        #     for inimigo in inimigos:
        #         if inimigo.mover:
        #             inimigo.mover = False
        #             boss_parado = True
        #         elif inimigo.ataque:
        #             inimigo.mover = True

        player_hits =  pygame.sprite.groupcollide(player.balas,inimigos, False, False)
        
        for inimigo in inimigos:
            enemy_hits = pygame.sprite.groupcollide(inimigo.balas, player_group, False, False)

            if len(enemy_hits)>0:
                a = (enemy_hits.keys())
                inimigo.balas.remove(a)
                
                player.get_hit()

        if len(player_hits) > 0:
            a = (player_hits.keys())
            b = (player_hits.values())

            player.balas.remove(a)
            for value in b:
                for item in inimigos:
                    if value[0] == item:
                        item.HP-=1
            i = 0
            for inimigo in inimigos:
                i+=1

        for inimigo in inimigos:
            xp.atualizar_xp(inimigo)
            if inimigo.HP == 0:
                inimigo.image = pygame.Surface((32, 32), pygame.SRCALPHA)
                inimigo.remover_todas_balas()
                inimigos.remove(inimigo)
                all_sprites.remove(inimigo)


        player.sheet.draw(screen, player.rect.x - camera.left , player.rect.y - camera.top)

        # Salvar a posição anterior para colisão
        old_x, old_y = player.rect.x, player.rect.y
        

        # Atualizar jogador
        #all_sprites.update(pause) ######## pause maroto

        if dialogo_a_abrir:
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

        mouse_errado = pygame.mouse.get_pos()

        mouse_pos =[0,0]

        if camera.left > 0:
            mouse_pos[0] = mouse_errado[0]+camera.left
        else:
            mouse_pos[0] = mouse_errado[0]-camera.left

        mouse_pos[1] = mouse_errado[1]+camera.top

        # if click:
        #     player.shoot(mouse_pos)
        # else:
        #     if click_hold > 0:
        #         player.shoot(mouse_pos)
        #         print(mouse_pos)
        #     click_hold = 0
        #     player.atacando = False

        if click:
            click_hold +=1
            player.atacando = True
            player.hold_arrow(mouse_pos,camera)
        else:
            if click_hold > 30:
                player.shoot(mouse_pos)
                print(mouse_pos)
            click_hold = 0
            player.atacando = False
        
        # Renderização
        screen.fill((0, 0, 0))  # Fundo preto
        
        # Desenhar o mapa (apenas tiles visíveis)
        for x, y, image in map_tiles:
            # Verificar se o tile está dentro da visão da câmera
            if (camera.left - TILE_SIZE <= x < camera.right and 
                camera.top - TILE_SIZE <= y < camera.bottom):
                screen.blit(image, (x - camera.left, y - camera.top))

        # Dentro do game loop, na seção de renderização (após desenhar o jogador):
        # if DEBUG_MODE:
        #     # 1. Desenhar colisores do mapa (vermelho)
        #     for wall in walls:
        #         if camera.colliderect(wall):
        #             debug_wall_rect = pygame.Rect(
        #                 wall.x - camera.left,
        #                 wall.y - camera.top,
        #                 wall.width,
        #                 wall.height
        #             )
        #             pygame.draw.rect(screen, (255, 0, 0), debug_wall_rect, 1)
            
        #     # 2. Desenhar colisor do jogador (azul)
        #     debug_player_rect = pygame.Rect(
        #         player.rect.x - camera.left,
        #         player.rect.y - camera.top,
        #         player.rect.width,
        #         player.rect.height
        #     )
        #     pygame.draw.rect(screen, (0, 0, 255), debug_player_rect, 2)
            
        #     # 3. Mostrar informações de debug
        #     font = pygame.font.SysFont(None, 24)
        #     debug_info = [
        #         f"Posição: ({player.rect.x}, {player.rect.y})",
        #         f"Direção: {player.direction}",
        #         f"Velocidade: {player.speed}",
        #         f"Colisores: {len(walls)}",
        #         "Z: Debug ON/OFF"
        #     ]
            
        #     for i, text in enumerate(debug_info):
        #         text_surface = font.render(text, True, (255, 255, 255))
        #         screen.blit(text_surface, (10, 10 + i * 25))

        #     for inimigo in inimigos:
        #         debug_enemy_rect = pygame.Rect(
        #             inimigo.rect.x - camera.left,
        #             inimigo.rect.y - camera.top,
        #             inimigo.rect.width,
        #             inimigo.rect.height
        #         )
        #         pygame.draw.rect(screen, (255, 255, 0), debug_enemy_rect, 2)

        for inimigo in inimigos:
            if inimigo.rect.colliderect(player.rect):
                player.get_hit()
                inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y
                player.rect.topleft = (old_x,old_y)
                inimigo.atacando_melee = True
                inimigo.frame_change = 4
            else:
                inimigo.atacando_melee = False
                inimigo.frame_change = 10

        for inimigo in inimigos:
            if camera.colliderect(inimigo.rect):
                screen.blit(inimigo.image, (inimigo.rect.x - camera.left, inimigo.rect.y - camera.top))

        # Desenhar o jogador
        player.sheet.draw(screen, player.rect.x - camera.left, player.rect.y - camera.top)

        for npc in npcs:
            screen.blit(npc.image,(npc.rect.x - camera.left, npc.rect.y - camera.top))

        for inimigo in inimigos:
            inimigo.draw_balas(screen,camera)
        player.draw_balas(screen,camera)

        for inimigo in inimigos:
            screen.blit(inimigo.image, (inimigo.rect.x - camera.left, inimigo.rect.y - camera.top))
            print(inimigo.sheet.tile_rect)
            #print(inimigo.rect.x-camera.left,inimigo.rect.y-camera.top)
            #1570,2102

        for vida in range(player.HP):
            screen.blit(vida_imagem,(18 + 32*vida,0))
        for npc in npcs:
            npc.dialogo.coisa()

        for bau in baus:
            screen.blit(bau.image, (bau.rect.x - camera.left, bau.rect.y - camera.top))

        for npc in npcs:
            npc_big_rect = pygame.Rect(
                npc.dialogo_rect.x - camera.left,
                npc.dialogo_rect.y - camera.top,
                npc.dialogo_rect.width,
                npc.dialogo_rect.height
            )
            if npc.dialogo_rect.colliderect(player.rect):
                pygame.draw.rect(screen, (0, 0, 255), npc_big_rect, 2)

        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            
            font = pygame.font.Font(None,48)
            render = font.render("Interagir", True, (0,0,0))
            screen.blit(interagir_bg,(300,450))
            screen.blit(render,(325,457))

        # Desenhar os inventários e o botão
        if inventario1.inventory_open:
            inventario1.draw_inventory(screen)
        if bau_perto:
            if bau_perto.inventario.inventory_open:
                bau_perto.image = bau_perto.bau_aberto
                bau_perto.inventario.draw_inventory(screen)
            else:
                bau_perto.image = bau_perto.bau_fechado

        if botao_ativo:
            inventario1.draw_button(screen)  # Agora o método `draw_button` é da classe Inventario1

        if dragging_item:
            inventario1.draw_dragging_item(screen, dragging_item)  # Agora o método `draw_dragging_item` é da classe Inventario1


        xp.render()
        pygame.display.flip()

    boss_fight()

if __name__ == "__main__":
    inicio()
#----------------------------------------------------------------------------------------------------------------------------------------------------
#     if player.rect.left <= -15:
#         player.rect.left = -15

#     if player.rect.right >= bg.get_width()-10:
#         player.rect.right = bg.get_width()-10

#     if player.rect.bottom >= bg.get_height()-28:
#         player.rect.bottom = bg.get_height()-28

#     if player.rect.top <= -15:
#         player.rect.top = -15

#     screen.blit(bg, (0, 0), camera)

#     # if player.ivuln == True:
#     #     if player.contador_iframes < player.iframes:
#     #         player.contador_iframes += 1
#     #     else:
#     #         player.ivuln = False
#     #         player.contador_iframes = 0
#     #         player.rect.width = 64 
#     #         player.rect.height = 64


#     # if player.ivuln: 
#     #     camera.center = (player.rect.x+32,player.rect.y + 32)
#     #     print(camera.center)
#     # elif not player.ivuln:
#     camera.center = player.rect.center