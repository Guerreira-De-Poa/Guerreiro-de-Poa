import pygame
import os
import sys
assets = os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.path.append(assets)

class SpriteSheet:
    def __init__(self, filename, pos_x, pos_y, largura_sprite, altura_sprite, m, lista_acoes, color_key=None, multiplas_linhas = True):
        """
        Classe para manipular spritesheets e criar animações.
        
        Parâmetros:
        filename (str): Caminho do arquivo da spritesheet.
        pos_x (int): Posição X inicial do primeiro sprite na spritesheet.
        pos_y (int): Posição Y inicial do primeiro sprite na spritesheet.
        largura_sprite (int): Largura de cada tile (quadro da animação).
        altura_sprite (int): Altura de cada tile.
        m (int): Margem entre os tiles (se houver).
        total_sprites (int): Número total de total_sprites na animação.
        color_key (tuple, opcional): Cor de transparência a ser definida (R, G, B).
        """
        self.sheet = pygame.image.load(os.path.join(assets, filename))  # Carrega a imagem da spritesheet
        self.lista_acoes = lista_acoes
        self.action = 0
        self.cells = []
        
        # Define a cor de transparência se fornecida
        if color_key:
            self.sheet = self.sheet.convert()
            self.sheet.set_colorkey(color_key)
        else:
            self.sheet = self.sheet.convert_alpha()
        
        # Cria uma lista de retângulos para cada tile dentro da spritesheet
        if multiplas_linhas == True:
            iterador = 0
            for action in lista_acoes:
                self.cells.append([(pos_x + largura_sprite*i, pos_y + altura_sprite*iterador,largura_sprite-m,altura_sprite) for i in range(action)])
                iterador +=1
        else:
            iterador = 0
            for action in lista_acoes:
                self.cells.append([(pos_x + largura_sprite * i, pos_y, largura_sprite - m, altura_sprite) for i in range(action)])
                iterador +=1

        #self.cells = [[(pos_x+largura_sprite*i)]]
        #self.cells = [(pos_x + largura_sprite * i, pos_y, largura_sprite - m, altura_sprite) for i in range(total_sprites)]
        self.index = 0  # Índice do quadro atual da animação
        self.tile_rect = self.cells[0][1]

        # print(len(self.cells))
    
    def update(self):
        """ Atualiza o quadro atual da animação. """
        self.tile_rect = self.cells[self.action][self.index % len(self.cells[self.action])]  # Alterna entre os quadros disponíveis
        if self.tile_rect == self.cells[self.action][0]:
            self.tile_rect = self.cells[self.action][1]
        self.index += 1  # Avança para o próximo quadro
    
    # def draw(self, surface, x, y):
    #     """ Desenha o sprite atual na posição especificada. """
    #     rect = pygame.Rect(self.tile_rect)  # Cria um retângulo baseado no quadro atual
    #     #rect.center = (x, y)  # Define o centro do retângulo na posição desejada
    #     rect.topleft = (x, y)
    #     surface.blit(self.sheet, rect, self.tile_rect)  # Desenha o sprite na tela
    def draw(self, surface, x, y):
        """ Desenha o sprite atual na posição especificada. """
        rect = pygame.Rect(self.tile_rect)  # Cria um retângulo baseado no quadro atual

        #rect.center = (x, y)  # Define o centro do retângulo na posição desejada
        rect.topleft = (x, y)
        surface.blit(self.sheet, rect, self.tile_rect)  # Desenha o sprite na tela









# import pygame

# class SpriteSheet:
#     def __init__(self, filename, pos_x, pos_y, largura_sprite, altura_sprite, m, lista_acoes, color_key=None, multiplas_linhas = True):
#         """
#         Classe para manipular spritesheets e criar animações.
        
#         Parâmetros:
#         filename (str): Caminho do arquivo da spritesheet.
#         pos_x (int): Posição X inicial do primeiro sprite na spritesheet.
#         pos_y (int): Posição Y inicial do primeiro sprite na spritesheet.
#         largura_sprite (int): Largura de cada tile (quadro da animação).
#         altura_sprite (int): Altura de cada tile.
#         m (int): Margem entre os tiles (se houver).
#         total_sprites (int): Número total de total_sprites na animação.
#         color_key (tuple, opcional): Cor de transparência a ser definida (R, G, B).
#         """
#         self.sheet = pygame.image.load(filename)  # Carrega a imagem da spritesheet
#         self.lista_acoes = lista_acoes
#         self.action = 0
#         self.cells = []
#         self.largura_sprite = largura_sprite
        
#         # Define a cor de transparência se fornecida
#         if color_key:
#             self.sheet = self.sheet.convert()
#             self.sheet.set_colorkey(color_key)
#         else:
#             self.sheet = self.sheet.convert_alpha()
        
#         # Cria uma lista de retângulos para cada tile dentro da spritesheet
#         if multiplas_linhas == True:
#             iterador = 0
#             for action in lista_acoes:
#                 self.cells.append([(pos_x + largura_sprite*i, pos_y + altura_sprite*iterador,largura_sprite-m,altura_sprite) for i in range(action)])
#                 iterador +=1
#         else:
#             iterador = 0
#             for action in lista_acoes:
#                 self.cells.append([(pos_x + largura_sprite * i, pos_y, largura_sprite - m, altura_sprite) for i in range(action)])
#                 iterador +=1

#         #self.cells = [[(pos_x+largura_sprite*i)]]
#         #self.cells = [(pos_x + largura_sprite * i, pos_y, largura_sprite - m, altura_sprite) for i in range(total_sprites)]
#         self.index = 0  # Índice do quadro atual da animação
#         self.tile_rect = self.cells[0][1]

#         print(len(self.cells))
    
#     def update(self):
#         """ Atualiza o quadro atual da animação. """
#         self.tile_rect = self.cells[self.action][self.index % len(self.cells[self.action])]  # Alterna entre os quadros disponíveis
#         if self.tile_rect == self.cells[self.action][0]:
#             self.tile_rect = self.cells[self.action][1]
#         self.index += 1  # Avança para o próximo quadro
    
#     def draw(self, surface, x, y, scale=1):
#         """ Desenha o sprite atual na posição especificada. """
#         rect = pygame.Rect(self.tile_rect)  # Cria um retângulo baseado no quadro atual
#         tile_image = self.sheet.subsurface(rect)

#         if scale != 1:
#             novo_tam = (int(rect.width*scale), int(rect.height*scale))
#             tile_image = pygame.transform.scale(tile_image, novo_tam)
#             draw_rect = tile_image.get_rect(center=(x, y))
#         else:
#             draw_rect = pygame.Rect(x, y, rect.width, rect.height)
#         #rect.center = (x, y)  # Define o centro do retângulo na posição desejada
#         # rect.topleft = (x, y)
#         # surface.blit(self.sheet, rect, self.tile_rect)  # Desenha o sprite na tela
#         surface.blit(tile_image, draw_rect)