import pygame
import sys
import json
import os
import cv2

os.environ['SDL_VIDEO_CENTERED'] = '1'


pasta_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Adicionando o diretório pai ao sys.path
sys.path.append(pasta_pai)

# Agora podemos importar diretamente a função 'inicio' do arquivo 'main_luta.py'
from boss_fight.main_luta import inicio as boss_fight

# chama ultimo nivel
from ultimo_nivel.ultimo import inicio as ultimo_nivel

assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","assets"))

# Adicionando o diretório pai ao sys.path
sys.path.append(assets)

# Chamando a função importada

from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem

from npcs import * 
from dialogo import *
from inimigo_teste import *
from inventario1 import Inventario
from itens import Item
from boss import Boss1
from bau import Bau
from game_over import Game_over

from XP import XP
from menu_status import Menu

from cutscenes.tocar_cutscene import tocar_cutscene_cv2

from menu_opcoes import MenuOpcoes

pause = False

pygame.mixer.music.stop()

# Ler
# with open('save.json', 'r') as f:
#     estado = json.load(f)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def inicio():
    ####
    # PRA MUSICA FUNCIONAR: ANTES DO LOOP, QUEBRE O SOM, COMEÇOU? PEGA A MUSICA
    pygame.mixer.music.load("musicas/The Four Seasons, Winter - Vivaldi.mp3")
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
    
    if not map_tiles:
        print("Erro: Nenhum tile foi carregado para renderização!")
        pygame.quit()
        sys.exit()

    lista_1 = [7 for i in range(4)]
    lista_2 = [4 for i in range(4)]
    lista_2_alt = [6 for i in range (4)]
    lista_3 = [6 for i in range(8)]
    lista_4 = [13 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    with open('save.json', 'r') as f:
        try:
            save_carregado = json.load(f)
            print(save_carregado)
        except:
            save_carregado = False
            print("ERRO AO CARREGAR SAVE")

    atributos = {
            "ataque": 6.25,
            "defesa": 5.0,
            "vida_max": 20,
            "vida_atual": 10,
            "stamina": 6.25,
            "velocidade": 10
    }

    #print(save_carregado)

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

    # Posicionar o jogador em uma posição válida no mapa
    player.rect.x = 1025
    player.rect.y = 1080

    # Configuração da câmera
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Game loop
    clock = pygame.time.Clock()
    running = True
    menu_opcoes = MenuOpcoes(SCREEN_WIDTH, SCREEN_HEIGHT, screen, running)

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    spritesheet_inimigo_arco = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco0 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco1 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco2 = SpriteSheet('inimigo_com_arco.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco3 = SpriteSheet('inimigo_com_adaga.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    spritesheet_inimigo_arco4 = SpriteSheet('inimigo_com_arco.png', 0, 522, 64, 64, 4,lista_1+lista_2_alt+lista_3+lista_4+lista_5, (0, 0, 0))
    inimigos = pygame.sprite.Group()


    player_group = pygame.sprite.Group()

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_group.add(player)

    enemy0 = Inimigo(player.rect, player, 566,322, False,spritesheet_inimigo_arco, 10, 750, 50)
    enemy1 = Inimigo(player.rect, player, 150,754, False,spritesheet_inimigo_arco1, 13, 500, 20)
    enemy2 = Inimigo(player.rect, player, 1170,152, True,spritesheet_inimigo_arco2, 8, 650, 30)
    enemy4 = Inimigo(player.rect, player, 870,152, True,spritesheet_inimigo_arco2, 8, 650, 30)
    enemy3 = Inimigo(player.rect, player, 650,266, False,spritesheet_inimigo_arco3, 9, 600, 40)
    all_sprites.add(enemy0, enemy1, enemy2, enemy3,enemy4)
    inimigos.add(enemy0, enemy1, enemy2, enemy3,enemy4)
    #all_sprites.add(enemy0, enemy1, enemy2, enemy3)
    #inimigos.add(enemy0, enemy1, enemy2, enemy3)

    # boss2 = Boss1(player.rect,player,400,400,True,spritesheet_inimigo_arco)
    # all_sprites.add(boss2)
    # inimigos.add(boss2)

    contador = 0

    click_hold = 0

    interagir_bg = pygame.image.load(os.path.join(assets, "caixa_dialogo_pequena2.png"))

    # omori = pygame.image.load('npc_amarelo.png')
    # omori1 = pygame.image.load('npc_cinza.png')
    # omori2 = pygame.image.load('npc_vermelho1.png')

    # # DIALOGO NPC QUE APARECE DE PRIMEIRA
    # texto = {
    #     'personagem':'Morador de Poá',
    #     'texto_1':['Ei você', 'Você parece um guerreiro formidável', 'Por favor nos ajude', 'Nossa vila está sendo invadida'],
    #     'personagem_1': "Guerreiro de Poá",
    #     'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
    #     }

    # # DIALOGO NPC QUE APARECE DEPOIS QUE O JOGADOR AJUDA O NPC (PRIMEIRO)
    # texto_1 = {
    #     'personagem':'Morador de Poá',
    #     'texto_1':['Obrigado por nos salvar', 'Fale com o carinha que mora logo ali','Ele viu onde o chefe dos invasores fica', 'Se você derrotar o chefe', 'Eles nunca irão nos invadir de novo' ],
    #     'personagem_1': "Guerreiro de Poá",
    #     'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
    #     }

    # # NPC ANTES DO LIGEIRO

    # texto_2 = {
    #     'personagem':'Morador de Poá',
    #     'texto_1':['Você foi o guerreiro que nos salvou certo?', 'Muito obrigado', 'Eu posso te levar ao chefe deles', 'Isso fará com que eles desistam'],
    #     'personagem_1': "Guerreiro de Poá",
    #     'texto_2':['Me leve até lá']
    #     }
    
    # # NPC ANTES DO GABRIEL
    # texto_3 = {
    #     'personagem':'Morador de Poá',
    #     'texto_1':['Muito obrigado por nos salvar!', 'Mas agora, é a sua hora de brilhar...', 'Gabriel está neste castelo', 'pronto para aniquilar Poá', 'Apenas você pode derrotá-lo', 'Boa sorte'],
    #     'personagem_1': "Guerreiro de Poá",
    #     'texto_2':['Me leve até lá']
    #     }
    
    # ########### 
    # # de alguma forma, agora te que deixar o dicionario texto...
    # ###########
 
    # # posição dos npcs
    # npc0 = NPC(omori1,screen,1151,845,texto_2, 2) # npc ligeiro
    # npc1 = NPC(omori,screen,1955, 2150,texto, 3) # npc inicio
    # npc2 = NPC(omori2,screen,1954, 744,texto_3, 4) # npc gabriel

    # all_sprites.add(npc0,npc1)
    # npcs = pygame.sprite.Group()
    # npcs.add(npc0,npc1,npc2 ) 

    # dialogo_group = []

    # for npc in npcs:
    #     if npc.dialogo:
    #         dialogo_group.append(npc.dialogo)

    #################

    # TEORICAMENTE, caso for true, começa a missão
    # for npc in npcs:
    #     if npc.dialogo.missao_ativada:
    #         print("ok")

    #################

    # print(dialogo_group)
    # print(f"Total de tiles carregados: {len(map_tiles)}")

    #CONFIG INVENTARIO

    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Botão para abrir o inventário 2
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 140, 60)

    # Variáveis de controle de arrastar itens
    dragging_item = None
    dragging_from = None

    inventario2 = Inventario((0, 100, 0), 400)

    baus = pygame.sprite.Group()

    espada = Item('arma', 'Espada',{'dano': 5},False,player)
    armadura = Item('armadura', 'Armadura',{'defesa': 0.5},False,player)
    pocao2 = Item('consumivel', 'Poção', {'vida': 10},False,player)
    pocao3 = Item('consumivel', 'Poção', {'vida': 10},False,player)

    bau_saida = Bau(screen,1500,140,[pocao2,pocao3])

    baus.add(bau_saida)

    iterado_teste = 0

    contador_ataque_melee = 0

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

    inimigos_spawnados = False

    dash = 0
    cooldown_dash = 0
    velocidade_anterior = 0

    while menu_opcoes.rodando:
        pygame.mixer.music.set_volume(menu_opcoes.volume_musica)  # 50% do volume máximo
        if player.HP <= 0:
            running = False
            Game_over(inicio)
            menu_opcoes.rodando = False

        if len(inimigos) == 0 and player.rect.y < 135:
            if player.rect.x > 930 and player.rect.x < 1109:
                salvar_game()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("musicas/sfx-menu12.mp3")
                pygame.mixer.music.play(1)  # -1 significa que a música vai tocar em loop
                pygame.mixer.music.set_volume(0.2)  # 50% do volume máximo
                # ULTIMO NIVEL!
                running = False
                screen.fill((0, 0, 0))
                pygame.display.flip()
                pygame.time.delay(500)
                print('ok')
                tocar_cutscene_cv2('cutscenes/cutscene_bossFinal.mp4', 'cutscenes/cutscene_bossFinal.mp3', screen)
                ultimo_nivel() # AQUI É MELHOR
        elif player.rect.y >= 1040:
            player.rect.y -= player.speed
        # else:
        #     if player.rect.x > 930 and player.rect.x < 1109 and player.rect.y <=135:
        #         player.rect.y = 150

        menu.update()
        player.atualizar_stamina()

        click = pygame.mouse.get_pressed()[0]

        click_mouse_2 = pygame.mouse.get_pressed()[2]

        mouse_errado = pygame.mouse.get_pos()

        mouse_pos =[0,0]

        if camera.left > 0:
            mouse_pos[0] = mouse_errado[0]+camera.left
        else:
            mouse_pos[0] = mouse_errado[0]-camera.left

        mouse_pos[1] = mouse_errado[1]+camera.top

        if click or click_mouse_2:
            #print("DMSALDML")
            if inventario1.inventory_open or bau_perto:
                if bau_perto:
                    bau_perto.inventario.pressed_counter +=1
                else:
                    inventario1.pressed_counter +=1

                if dragging_item == None:
                    if inventario1.inventory_open and inventario1.pressed_counter >= 10:
                        item = inventario1.get_item_at(pygame.mouse.get_pos())

                        if item:
                            dragging_item = item
                            dragging_from = "inventory1"

                    if bau_perto:
                        if bau_perto.inventario.inventory_open and inventario1.pressed_counter >= 10:
                            item = bau_perto.inventario.get_item_at(pygame.mouse.get_pos())
                            if item:
                                dragging_item = item
                                dragging_from = "inventory2"

        bau_perto = False

        for bau in baus:
            if bau.interagir_rect.colliderect(player.rect):
                bau_perto = bau

        clock.tick(60) # Delta time em segundos

        botao_ativo = False

        dialogo_a_abrir = False

        screen.fill((100, 100, 100))  # Preenche o fundo com uma cor sólida

        dialogo_hitbox =  False

        # for npc in npcs:
        #     if npc.dialogo_rect.colliderect(player.rect):
        #         dialogo_hitbox = npc

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

                # if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d] and event.key == pygame.K_LSHIFT:
                
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
                elif event.key == pygame.K_t:
                    player.arcoEquipado = not player.arcoEquipado
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
                elif event.key == pygame.K_DOWN and inventario1.scroll_index < len(inventario1.items) - inventario1.visible_items and not menu_opcoes.pausado:
                    inventario1.item_index +=1
                    inventario1.scroll_index += 1
                elif event.key == pygame.K_UP and inventario1.scroll_index > 0 and not menu_opcoes.pausado:
                    inventario1.item_index -=1
                    if inventario1.item_index < inventario1.visible_items-1:
                        print(inventario1.item_index,inventario1.visible_items + 2)
                        inventario1.scroll_index -= 1

                elif event.key == pygame.K_DOWN and inventario1.item_index < len(inventario1.items)-1 and not menu_opcoes.pausado:
                    inventario1.item_index +=1
                elif event.key == pygame.K_UP and inventario1.item_index > 0 and not menu_opcoes.pausado:
                    inventario1.item_index -=1

                elif event.key == pygame.K_RETURN:
                    if inventario1.inventory_open:
                        if inventario1.items[inventario1.item_index].tipo != 'consumivel':
                            inventario1.items[inventario1.item_index].equipar()
                        else:
                            inventario1.items[inventario1.item_index].utilizar()
                            inventario1.remove(inventario1.items[inventario1.item_index])


                # elif event.key == pygame.K_ESCAPE:
                #     running = False

                if event.key == pygame.K_m:
                    xp.show_menu = not xp.show_menu
                    if xp.show_menu:
                        menu.valores_copy = menu.valores.copy()
            
            elif event.type == pygame.KEYUP and not event.type == pygame.KEYDOWN:
                if event.key in teclas_movimento:
                    teclas_pressionadas.discard(event.key)
                    if len(teclas_pressionadas) == 0:
                        canal_andar.stop()
            
            menu_opcoes.processar_eventos(event)

            if not player.arcoEquipado:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player.shoot(mouse_pos, camera)

                
            if xp.show_menu and menu.tamanho_menu_img_x == 600 and menu.tamanho_menu_img_y == 400:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for atributo, botoes in menu.botoes.items():
                        # Botão de diminuir
                        if botoes["diminuir"]["rect"].collidepoint(event.pos) and xp.pontos_disponiveis < xp.pontos_disponiveis_copy:
                            if menu.valores[atributo] > menu.valores_copy[atributo]:  # Impede de reduzir abaixo do inicial
                                menu.valores[atributo] -= 1
                                botoes["diminuir"]["pressionado"] = True
                                xp.pontos_disponiveis += 1  # Devolve um ponto

                                if atributo == "ataque":
                                    menu.atributos[atributo] -= 1.25
                                    player.dano = menu.atributos[atributo]
                                if atributo == "defesa":
                                    menu.atributos[atributo] -= 1
                                    player.defesa = menu.atributos[atributo]
                                if atributo == "vida":
                                    menu.atributos[atributo] -= 3
                                    player.MAX_HP = menu.atributos[atributo]
                                    player.HP -= 3
                                if atributo == "stamina":
                                    menu.atributos[atributo] -= 1.25
                                    player.stamina = menu.atributos[atributo]
                                if atributo == "velocidade":
                                    menu.atributos[atributo] -= 2
                                    player.velocidade_corrida = menu.atributos[atributo]

                        # Botão de aumentar
                        if botoes["aumentar"]["rect"].collidepoint(event.pos) and xp.pontos_disponiveis > 0:
                            menu.valores[atributo] += 1
                            botoes["aumentar"]["pressionado"] = True

                            if menu.valores[atributo] > menu.valores_max[atributo]:
                                menu.valores[atributo] = menu.valores_max[atributo]
                                menu.atributos[atributo] = menu.atributos_max[atributo]
                                # xp.pontos_disponiveis += 0
                            else:
                                xp.pontos_disponiveis -= 1  # Gasta um ponto

                            if atributo == "ataque":
                                menu.atributos[atributo] += 1.25
                                player.dano = menu.atributos[atributo]
                            if atributo == "defesa":
                                menu.atributos[atributo] += 0.15
                                player.defesa = menu.atributos[atributo]
                            if atributo == "vida":
                                menu.atributos[atributo] += 3
                                player.MAX_HP = menu.atributos[atributo]
                                player.HP += 3
                            if atributo == "stamina":
                                menu.atributos[atributo] += 1.25
                                player.max_stamina = menu.atributos[atributo]
                            if atributo == "velocidade" and menu.valores["velocidade"] <= 6:
                                menu.atributos[atributo] += 2
                                player.velocidade_corrida = menu.atributos[atributo]
                            # else:
                                # menu.valores[atributo] = menu.valores_max[atributo]
                                # xp.pontos_disponiveis = xp.pontos_disponiveis

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

        #print(inventario1.item_index)

        contador+=1

        if contador % 62 == 0:
            for inimigo in inimigos:
                if inimigo.ataque and not xp.show_menu and not menu_opcoes.pausado and not inventario1.inventory_open:
                    inimigo.atacar()
                pass

        if cooldown_dash>0:
            cooldown_dash+=1
            if cooldown_dash == 90:
                cooldown_dash = 0

        if player.dash == True:
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
                
                player.get_hit(inimigo.dano)

        if len(player_hits) > 0:
            a = (player_hits.keys())
            b = (player_hits.values())

            player.balas.remove(a)
            for value in b:
                for item in inimigos:
                    if value[0] == item:
                        item.get_hit(player.dano)
                        print(item.HP)
            i = 0
            for inimigo in inimigos:
                i+=1

        for inimigo in inimigos:
            xp.atualizar_xp(inimigo, 300)
            if inimigo.HP <= 0:
                inimigo.image = pygame.Surface((32, 32), pygame.SRCALPHA)
                inimigo.remover_todas_balas()
                inimigos.remove(inimigo)
                all_sprites.remove(inimigo)
            if inimigo.rect.colliderect(player.range_melee) and player.atacando_melee:
                if player.sheet_sec.tile_rect in [player.sheet_sec.cells[player.sheet_sec.action][-3],player.sheet_sec.cells[player.sheet_sec.action][-2],player.sheet_sec.cells[player.sheet_sec.action][-1]]:
                    #print(True)
                    inimigo.get_hit(player.dano)
                    inimigo.rect.x, inimigo.rect.y = inimigo.old_pos_x, inimigo.old_pos_y

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

        # for npc in npcs:
        #     if player.collision_rect.colliderect(npc):
        #         # Colisão detectada, voltar para a posição anterior
        #         player.rect.x, player.rect.y = old_x, old_y
        #         break

                
        # Atualizar câmera
        lerp_factor = 0.1  # ajuste esse valor conforme necessário (0 < lerp_factor < 1)
        target_center = player.rect.center
        new_center_x = camera.centerx + (target_center[0] - camera.centerx) * lerp_factor
        new_center_y = camera.centery + (target_center[1] - camera.centery) * lerp_factor
        camera.center = (new_center_x, new_center_y)
        
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
                    som_atirar_flecha.set_volume(menu_opcoes.volume_efeitos)
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
                if inimigo.sheet.tile_rect in [inimigo.sheet.cells[inimigo.sheet.action][-1]]:
                    player.get_hit(inimigo.dano)

                inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y

                if not player.ivuln:
                    player.rect.x,player.rect.y = old_x,old_y
                    
                inimigo.atacando_melee = True
                inimigo.frame_change = 10
            else:
                inimigo.atacando_melee = False
                inimigo.frame_change = 10

        for inimigo in inimigos:
            if camera.colliderect(inimigo.rect):
                screen.blit(inimigo.image, (inimigo.rect.x - camera.left, inimigo.rect.y - camera.top))

        # Desenhar o jogador
        player.draw(screen, camera)

        # for npc in npcs:
        #     screen.blit(npc.image,(npc.rect.x - camera.left, npc.rect.y - camera.top))

        for inimigo in inimigos:
            inimigo.draw_balas(screen,camera)
        player.draw_balas(screen,camera)

        for inimigo in inimigos:
            inimigo.sheet.draw(screen, inimigo.rect.x - camera.left, inimigo.rect.y - camera.top)
            #print(inimigo.rect.x-camera.left,inimigo.rect.y-camera.top)
            #1570,2102

        for bau in baus:
            screen.blit(bau.image, (bau.rect.x - camera.left, bau.rect.y - camera.top))


        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            
            font = pygame.font.Font(None,48)
            render = font.render("Interagir", True, (0,0,0))
            screen.blit(interagir_bg,(494,600))
            screen.blit(render,(525,627))

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

        if dragging_item:
            inventario1.draw_dragging_item(screen, dragging_item)  # Agora o método `draw_dragging_item` é da classe Inventario1

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

        if not menu_opcoes.pausado:
            player.draw_health(screen)
            player.draw_stamina(screen)
            if not dialogo_a_abrir:
                xp.render()
            else:
                if dialogo_a_abrir.texto_open == False:
                    xp.render()


        #print(menu.atributos,menu.valores)

        # for npc in npcs:
        #     npc.dialogo.coisa()

        pygame.display.flip()

if __name__ == "__main__":
    inicio()