import pygame
import math
from balas import Bala

# Classe que herda de pygame.sprite.Sprite
class Personagem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()  # Chama o inicializador da classe pai
        self.sheet = sprite_sheet
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)  # A imagem inicial
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem para movimentação
        
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()
        self.bullet_speed = 5

        #self.hitbox = pygame.image.load("hitbox.png")
        #self.hitbox_rect = self.hitbox.get_rect()

        self.atacando = False

        self.HP = 10

        self.balas = pygame.sprite.Group()

        self.speed = 2  # Velocidade de movimento
        self.posX = 400  # Posição inicial
        self.posY = 300
        self.rect.topleft = (self.posX, self.posY)  # Define a posição inicial

        self.frame_count = 0  # Contador de frames
        self.sprite_atual = 0  # Contador para alternar entre sprites de animação
        self.direction = 'DOWN'  # Direção de movimento (cima, baixo, esquerda, direita)

        self.frame_change = 10 #Quantidade de frames até a troca de sprite

        self.nova_direcao = False

        self.run = False
        self.atacar = False

        self.ivuln = False
        self.iframes = 90
        self.contador_iframes = 0

        self.dodge_iframes = 0

        self.mouse_pos = (0,0)

        self.mousex, self.mousey = self.mouse_pos

        #print(self.rect.left, self.rect.top)

        self.center_x, self.center_y = 800 // 2, 600 // 2

        self.segurando = False
        self.contador_ataque = 0

    def update(self, dialogo_open):
        if dialogo_open:
            return
        self.balas.update(dialogo_open)
        # Atualiza o contador de frames
        self.frame_count += 1
        self.moving = False

        if not self.atacando:
            if self.direction == 'UP'and self.run == False:
                self.sheet.action = 0
                self.rect.y -= self.speed  # Move para cima
                self.moving = True
            elif self.direction == 'DOWN'and self.run == False:
                self.sheet.action = 2
                self.rect.y += self.speed  # Move para baixo
                self.moving = True
            elif self.direction == 'LEFT'and self.run == False:
                self.sheet.action = 1
                self.rect.x -= self.speed  # Move para a esquerda
                self.moving = True
            elif self.direction == 'RIGHT'and self.run == False:
                self.sheet.action = 3
                self.rect.x += self.speed  # Move para a direita
                self.moving = True
                
            elif self.direction == 'UP'and self.run == True:
                self.sheet.action = 30
                self.rect.y -= self.speed  # Move para cima
                self.moving = True
            elif self.direction == 'DOWN'and self.run == True:
                self.sheet.action = 32
                self.rect.y += self.speed  # Move para baixo
                self.moving = True
            elif self.direction == 'LEFT'and self.run == True:
                self.sheet.action = 31
                self.rect.x -= self.speed  # Move para a esquerda
                self.moving = True
            elif self.direction == 'RIGHT'and self.run == True:
                self.sheet.action = 33
                self.rect.x += self.speed  # Move para a direita
                self.moving = True


        if self.atacando:
            if self.sheet.tile_rect == self.sheet.cells[self.sheet.action][-3]:
                self.segurando = True

            if -math.pi / 4 <= self.angle < math.pi / 4:
                #DIREITA
                self.sheet.action = 11

            elif self.angle >= 3 * math.pi / 4 or self.angle < -3 * math.pi / 4:
                #ESQUERDA
                self.sheet.action = 9

            elif math.pi / 4 <= self.angle < 3 * math.pi / 4:
                #BAIXO
                self.sheet.action = 10

            else:
                #Cima
                self.sheet.action = 8


        # if self.atacando:
        #     if self.sheet.action == 0 or self.sheet.action == 30:
        #         self.sheet.action = 8
        #     elif self.sheet.action == 1 or self.sheet.action == 31:
        #         self.sheet.action = 9
        #     elif self.sheet.action == 2 or self.sheet.action == 32:
        #         self.sheet.action = 10
        #     elif self.sheet.action == 3 or self.sheet.action == 33:
        #         self.sheet.action = 11

            #self.sprite_atual = (self.sprite_atual + 1) % 2
        # A cada 10 frames, troca de sprite para evitar animação rápida demais

        if self.moving:
            if self.frame_count % self.frame_change == 0 or self.nova_direcao == True:  
                self.sheet.update()
                self.nova_direcao = False
        elif self.atacando:
            if self.frame_count % self.frame_change == 0:  
                #print(self.sheet.action)
                if self.sheet.tile_rect != self.sheet.cells[self.sheet.action][-3]:
                    self.sheet.update()
        else:
            if self.sheet.action in [30,31,32,33]:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action-30][0]
            else:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action][0]

        for bala in self.balas:
            if not bala.active:
                self.balas.remove(bala)

        self.collision_rect = self.rect.inflate(-40, -20)

        if self.ivuln == True:
            self.contador_iframes +=1
            if self.contador_iframes == self.iframes:
                self.ivuln = False

    def hold_arrow(self,mouse_pos, camera):
        #print(mouse_pos)
        self.mouse_pos = mouse_pos
        self.mousey = self.mouse_pos[1]
        self.mousex = self.mouse_pos[0]

        self.rel_x = (self.mousex - self.center_x)-camera.left
        self.rel_y = (self.mousey - self.center_y)-camera.top

        # Calcula o ângulo em radianos
        self.angle = math.atan2(self.rel_y, self.rel_x)  # Retorna ângulo de -π a π

    def get_sprite(self):
        rect = pygame.Rect(self.sheet.tile_rect)
        sprite = pygame.Surface((32,32), pygame.SRCALPHA)
        sprite.blit(self.sheet.sheet, (0, 0), rect)

    def correr(self):
        if self.run:
            self.run = False
            self.speed = 2
            self.frame_change = 10

        elif self.run == False:
            self.run = True
            self.speed = 4
            self.frame_change = 5

        return self.run

    def shoot(self,mouse_pos):
        # if len(self.balas) > 0:
        #     return

        #TESTE

        # self.atacando = False

        # if not self.atacar:
        #     self.atacar = True
        # else:
        #     self.contador_ataque += 1
        #     if self.contador_ataque == 40:
        #         self.contador_ataque = 0
        #         self.atacar = False
        #     return
        
        # self.hold_arrow(mouse_pos)
        # self.atacando = True

        #FIM TESTE

        self.mouse_pos = mouse_pos

        self.bullet_pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(mouse_pos)
        self.direction = (self.target_pos - self.bullet_pos).normalize() if self.target_pos != self.bullet_pos else pygame.math.Vector2(0, 0)

        #print(self.player_rect)

        # Cria uma nova bala com direção e posição adequadas
        new_bala = Bala(self.rect.centerx, self.rect.centery, self.direction, self.bullet_speed, self.bullet_img)
        self.balas.add(new_bala)

        if self.sheet.tile_rect != self.sheet.cells[self.sheet.action][0]:
            self.sheet.update()

    def draw_balas(self, screen, camera):
        for bala in self.balas:
            if bala.active:
                # Ajuste da posição com a câmera
                screen.blit(bala.image, (bala.rect.x - camera.left, bala.rect.y - camera.top))
                pygame.draw.rect(screen, (255, 0, 0), bala.rect, 1)

    def remover_todas_balas(self):
        for bala in self.balas:
            self.balas.remove(bala)

    def get_hit(self):
        #print('rect center : ',self.rect.center)
        if self.ivuln == False:
            self.contador_iframes = 0
            self.HP -= 1
            self.ivuln = True
            # self.ivuln = True
            # #print(self.HP)
            # self.rect.width = 0  # "Desativa" a hitbox (remove colisão)
            # self.rect.height = 0
            #print('rect 0 0 center',self.rect.center)