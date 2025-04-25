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

from antes_ligeiro.luta_antes_ligeiro import inicio as mapa_antes_ligeiro

from antes_ultimo.antes_ultimo import inicio as mapa_antes_final

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
    pygame.mixer.music.set_volume(0.05)  # 50% do volume máximo

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
    spritesheet_path = os.path.join(current_dir, 'spritesheet.png')  # Nome correto da sua spritesheet

    # Carregar o arquivo JSON do mapa
    try:
        with open(map_path, 'r') as f:
            map_data = json.load(f)
    except Exception as e:
        # print(f"Erro ao carregar mapa: {e}")
        pygame.quit()
        sys.exit()

    # Configurações do mapa
    TILE_SIZE = map_data['tileSize']
    MAP_WIDTH = map_data['mapWidth']
    MAP_HEIGHT = map_data['mapHeight']

    atributos = {
            "ataque": 6.25,
            "defesa": 5.0,
            "vida_max": 20,
            "vida_atual": 20,
            "stamina": 96.25,
            "velocidade": 10
    }

    # Classe para carregar a spritesheet do mapa
    class MapSpriteSheet:
        def __init__(self, filename):
            try:
                self.sheet = pygame.image.load(filename).convert_alpha()
                # print(f"Spritesheet {filename} carregada com sucesso!")
            except Exception as e:
                # print(f"Erro ao carregar spritesheet: {e}")
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
    '60': (256, 448), '61': (320, 448), '62': (384, 448),
    '63': (448, 448), '64': (0, 512), '65': (64, 512),
    '66': (128, 512), '67': (192, 512), '68': (256, 512),
    '69': (320, 512), '70': (384, 512), '71': (448, 512),
    '72': (0, 576), '73': (64, 576), '74': (128, 576),
    '75': (192, 576), '76': (256, 576), '77': (320, 576),
    '78': (384, 576), '79': (448, 576), '80': (0, 640),
    '81': (64, 640), '82': (128, 640), '83': (192, 640),
    '84': (256, 640), '85': (320, 640), '86': (384, 640),
    '87': (448, 640), '88': (0, 704), '89': (64, 704),
    '90': (128, 704), '91': (192, 704), '92': (256, 704),
    '93': (320, 704), '94': (384, 704), '95': (448, 704),
    '96': (0, 768), '97': (64, 768), '98': (128, 768),
    '99': (192, 768), '100': (256, 768), '101': (320, 768),
    '102': (384, 768), '103': (448, 768), '104': (0, 832),
    '105': (64, 832), '106': (128, 832), '107': (192, 832),
    '108': (256, 832), '109': (320, 832), '110': (384, 832),
    '111': (448, 832), '112': (0, 896), '113': (64, 896),
    '114': (128, 896), '115': (192, 896), '116': (256, 896),
    '117': (320, 896), '118': (384, 896), '119': (448, 896),
    '120': (0, 960), '121': (64, 960), '122': (128, 960),
    '123': (192, 960), '124': (256, 960), '125': (320, 960),
    '126': (384, 960), '127': (448, 960), '128': (0, 1024),
    '129': (64, 1024), '130': (128, 1024), '131': (192, 1024),
    '132': (256, 1024), '133': (320, 1024), '134': (384, 1024),
    '135': (448, 1024), 
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
        layer_order = ['Background', 'Background-colisoes',  'Sand', 'Layer_18', 'Cliff', 'Rocks', 'Grass', 'Miscs (Copy)', 'placas', 'Buildings (Copy)', 'torres', 'Miscs', 'detalinhos', 'pedra_mar', 'casas', 'arvores']
        
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
    lista_2 = [4 for i in range(4)]
    lista_2_alt = [6 for i in range (4)]
    lista_3 = [6 for i in range(8)]
    lista_4 = [13 for j in range(4)]
    lista_5 = [7 for k in range(14)]

    # with open('save.json', 'r') as f:
    #     try:
    #         save_carregado = json.load(f)
    #         print(save_carregado)
    #     except:
    #         save_carregado = False
    #         print("ERRO AO CARREGAR SAVE")

    save_carregado = False

    #print(save_carregado)

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
            
        else:
            print("SAVE NAO CARREGADO")
            player = Personagem(player_sprite, atributos["ataque"], atributos["defesa"], atributos["vida_max"],atributos['vida_atual'], atributos["stamina"], atributos["velocidade"],player_sprite_ataques)
            inventario1 = Inventario((50, 50, 50), 50, [])
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    xp = XP(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    menu = Menu(5, 5, 5, 5, 5, 6.25, 5.0, 20, 6.25, 10.0, player)


    # Posicionar o jogador em uma posição válida no mapa
    player.rect.x = 33 * TILE_SIZE
    player.rect.y = 36 * TILE_SIZE

    # Configuração da câmera
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Game loop
    clock = pygame.time.Clock()
    running = True
    menu_opcoes = MenuOpcoes(SCREEN_WIDTH, SCREEN_HEIGHT, screen, running)

    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    imagem_inimigo = pygame.image.load('Biomech Dragon Splice.png')

    vida_imagem = pygame.image.load('love-always-wins(1).png')


    spritesheet_inimigo_arco_png = pygame.image.load("inimigo_com_arco.png")
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

    #all_sprites.add(enemy0, enemy1, enemy2, enemy3)
    #inimigos.add(enemy0, enemy1, enemy2, enemy3)

    # boss2 = Boss1(player.rect,player,400,400,True,spritesheet_inimigo_arco)
    # all_sprites.add(boss2)
    # inimigos.add(boss2)

    contador = 0

    click_hold = 0

    interagir_bg = pygame.image.load("caixa_dialogo_pequena2.png")

    omori = pygame.image.load('npc_amarelo.png')
    omori1 = pygame.image.load('npc_cinza.png')
    omori2 = pygame.image.load('npc_vermelho1.png')

    # DIALOGO NPC QUE APARECE DE PRIMEIRA
    texto = {
        'personagem':'Morador de Poá',
        'texto_1':['Ei você', 'Você parece um guerreiro formidável', 'Por favor nos ajude', 'Nossa vila está sendo invadida'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
        }

    # DIALOGO NPC QUE APARECE DEPOIS QUE O JOGADOR AJUDA O NPC (PRIMEIRO)
    texto_1 = {
        'personagem':'Morador de Poá',
        'texto_1':['Obrigado por nos salvar', 'Fale com o carinha que mora logo ali','Ele viu onde o chefe dos invasores fica', 'Se você derrotar o chefe', 'Eles nunca irão nos invadir de novo' ],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Não se preocupe senhor', 'Eu irei ajuda-los']
        }

    # NPC ANTES DO LIGEIRO

    texto_2_antes = {
        'personagem':'Morador de Poá',
        'texto_1':['Calma aí', 'Você ainda não fez a primeira missão', 'Fale com o morador perto da praia'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Eu irei ajudar!']
        }

    texto_2 = {
        'personagem':'Morador de Poá',
        'texto_1':['Você foi o guerreiro que nos salvou certo?', 'Muito obrigado', 'Eu posso te levar ao chefe deles', 'Ele mora logo ali naquela ilha ao norte', 'Isso fará com que eles desistam'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Me leve até lá']
        }
    
    # NPC ANTES DO GABRIEL
    texto_3 = {
        'personagem':'Morador de Poá',
        'texto_1':['Muito obrigado por nos salvar!', 'Mas agora, é a sua hora de brilhar...', 'Gabriel está neste castelo', 'pronto para aniquilar Poá', 'Apenas você pode derrotá-lo', 'Boa sorte'],
        'personagem_1': "Guerreiro de Poá",
        'texto_2':['Me leve até lá']
        }
    
    ########### 
    # de alguma forma, agora te que deixar o dicionario texto...
    ###########
 
    # posição dos npcs
    npc0 = NPC(omori1,screen,1151,845,texto_2, 2) # npc ligeiro
    npc1 = NPC(omori,screen,1955, 2150,texto, 3) # npc inicio
    npc2 = NPC(omori2,screen,1954, 744,texto_3, 4) # npc gabriel

    npcteste = NPC(omori1,screen,1151, 845,texto_2_antes) # npc inicio    
   
    all_sprites.add(npc0,npc1)
    npcs = pygame.sprite.Group()
    npcs.add(npc0,npc1,npc2, npcteste)  

    dialogo_group = []

    for npc in npcs:
        if npc.dialogo:
            dialogo_group.append(npc.dialogo)

    ### CHAVE ENTRADA LIGEIRO
    chave_entrada = False

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

        }
            # Salvar
        with open("save.json", "w") as f:
            json.dump(Dicionario_para_save, f, indent=4)

    inimigos_spawnados = False

    tocar_cutscene_cv2('cutscenes/cutscene_inicio.mp4', 'cutscenes/cutscene_inicio.mp3', screen)

    while menu_opcoes.rodando:
        if player.HP == 0:
            running = False

        if len(inimigos) == 0 and player.rect.y < 64:
            mapa_antes_ligeiro()
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
                    bau_perto.pressed_counter +=1
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
            

        missao_1 = npc1.dialogo.missao_ativada
        missao_2 = npc0.dialogo.missao_ativada
        missao_3 = npc2.dialogo.missao_ativada

        # Remover o NPC do ligeiro (e adiciona caso necessário)
        if inimigos_spawnados == False:
            all_sprites.remove(npc0)
            npcs.remove(npc0)
        elif inimigos_spawnados == True:
            all_sprites.add(npc0)
            npcs.add(npc0)

        if missao_3 == True:
            mapa_antes_final()
            ultimo_nivel() # AQUI É MELHOR
        if missao_2 == True and chave_entrada == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("musicas/sfx-menu12.mp3")
            pygame.mixer.music.play(-1)  # -1 significa que a música vai tocar em loop
            pygame.mixer.music.set_volume(0.2)  # 50% do volume máximo
            ####################
            #
            # ADICIONA NIVEL 1 - BOSS FIGHT "CHEFE 1"
            #
            ####################
            running = False
            ####################
            #
            #PARA ADICIONAR CUTSCENES
            #
            ####################
            screen.fill((0, 0, 0))
            fundo_loading = pygame.image.load('tela_loading_ligeiro.png').convert_alpha()
            fundo_loading = pygame.transform.scale(fundo_loading, (1152, 648))
            screen.blit(fundo_loading, (0, 0))
            pygame.display.flip()
            pygame.time.delay(1500)
            print('ok')
            tocar_cutscene_cv2('cutscenes/cutscene_boss1.mp4', 'cutscenes/cutscene_boss1.mp3', screen)
            boss_fight() # AQUI É MELHOR

        if missao_1 == True and iterado_teste == 0:
            iterado_teste+=1
            npc.dialogo.frase = ''
            npc1.dialogo.texto = texto_1
            npc1.dialogo.iter_texto = 0
            npc1.dialogo.texto_index = 0
            npc1.dialogo.letra_index = 0

        if missao_1 == True and len(inimigos) == 0:
            if not inimigos_spawnados:
                inimigos_spawnados = True
                enemy0 = Inimigo(player.rect, player, 1566,2322, False,spritesheet_inimigo_arco, 10, 750, 50)
                enemy1 = Inimigo(player.rect, player, 2150,1754, False,spritesheet_inimigo_arco1, 13, 500, 20)
                enemy2 = Inimigo(player.rect, player, 1570,2102, True,spritesheet_inimigo_arco2, 8, 650, 30)
                enemy3 = Inimigo(player.rect, player, 2650,2266, False,spritesheet_inimigo_arco3, 9, 600, 40)
                all_sprites.add(enemy0, enemy1, enemy2, enemy3)
                inimigos.add(enemy0, enemy1, enemy2, enemy3)
                
                # Remover o NPC teste
                all_sprites.remove(npcteste)
                npcs.remove(npcteste)
                
                # Adicionar o NPC do Ligeiro se ainda não estiver no grupo
                if npc0 not in npcs:
                    all_sprites.add(npc0)
                    npcs.add(npc0)
                    
                # Atualizar o grupo de diálogos
                dialogo_group = [npc.dialogo for npc in npcs if npc.dialogo]

            

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
                salvar_game()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ativar efeitos sonoros
                if event.key in teclas_movimento:
                    teclas_pressionadas.add(event.key)
                    
                    if not canal_andar.get_busy():
                        som_andar.set_volume(0.5)
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
                elif event.key == pygame.K_LSHIFT:
                    player.correr()
                elif event.key == pygame.K_t:
                    player.arcoEquipado = not player.arcoEquipado
                elif event.key == pygame.K_SPACE:
                    if dialogo_a_abrir:
                        dialogo_a_abrir.trocar_texto()
                    elif botao_ativo:
                        if bau_perto:
                            bau_perto.inventario.inventory_open = not bau_perto.inventario.inventory_open
                            inventario1.inventory_open = True
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
                elif event.key == pygame.K_UP and inventario1.scroll_index > 0:
                    inventario1.item_index -=1
                    if inventario1.item_index < inventario1.visible_items-1:
                        print(inventario1.item_index,inventario1.visible_items + 2)
                        inventario1.scroll_index -= 1

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


                
                menu_opcoes.processar_eventos(event)

                if event.key == pygame.K_m:
                    xp.show_menu = not xp.show_menu
                    if xp.show_menu:
                        menu.valores_copy = menu.valores.copy()
            
            elif event.type == pygame.KEYUP and not event.type == pygame.KEYDOWN:
                if event.key in teclas_movimento:
                    teclas_pressionadas.discard(event.key)
                    if len(teclas_pressionadas) == 0:
                        canal_andar.stop()

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
                                menu.atributos[atributo] += 1
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
                            elif inventario1.inventory_open and inventario1.inventory_rect.collidepoint(event.pos) and dragging_from == "inventory1":
                                inventario1.items.append(dragging_item)
                            dragging_item = None
                            dragging_from = None
                            if bau_perto.inventario.inventory_open and inventario1.pressed_counter <= 10:
                                if inventario1.get_item_at(event.pos) == None:
                                    inventario1.inventory_open = False
                                else:
                                    bau_perto.remove(inventario1.get_item_at(event.pos))

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

        if contador % 70 == 0:
            for inimigo in inimigos:
                if inimigo.ataque:
                    inimigo.atacar()
                pass

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
                        # print(item.HP)
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
            if click:
                click_hold += 1
                if not canal_carregar_arco.get_busy() and click_hold <= 30:
                    som_carregar_arco.set_volume(1)
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
                if not canal_atirar_flecha.get_busy():
                    som_atirar_flecha.set_volume(0.05)
                    canal_atirar_flecha.play(som_atirar_flecha, loops=0)
                click_hold = 0
                player.atacando = False
                player.atacando_melee = False
        else:
            if contador_melee == 0:
                cooldown_som_balançar_espada = pygame.time.get_ticks()
                primeiro_ataque_espada = 0

            contador_melee += 1

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - cooldown_som_balançar_espada >= delay_som_balançar_espada and primeiro_ataque_espada == 0:
                som_balançar_espada.set_volume(0.5)
                canal_balançar_espada.play(som_balançar_espada, loops=0)
                cooldown_som_balançar_espada = tempo_atual
                primeiro_ataque_espada = 1

            elif tempo_atual - cooldown_som_balançar_espada >= delay_som_balançar_espada + 335 and primeiro_ataque_espada == 1:
                som_balançar_espada.set_volume(0.5)
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

        # print(contador_melee)
        
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

                if not player.ivuln:
                    inimigo.rect.topleft = inimigo.old_pos_x, inimigo.old_pos_y
                    
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

        ####
        # paramantro para passaor de fase pro ligeiro
        ####

        if player.rect.y < 150:
            chave_entrada = True
            print("teste")

        for npc in npcs:
            screen.blit(npc.image,(npc.rect.x - camera.left, npc.rect.y - camera.top))

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

        if botao_ativo:
            inventario1.draw_button(screen)  # Agora o método `draw_button` é da classe Inventario1

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
            menu_opcoes.desenhar()
                
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

        for npc in npcs:
            npc.dialogo.coisa()

        pygame.display.flip()
    
    Game_over(inicio)

if __name__ == "__main__":
    inicio()