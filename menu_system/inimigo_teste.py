import pygame
from balas import Bala
from spritesheet_explicada import SpriteSheet

import sys
import os

import os
import sys

assets = os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.path.append(assets)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, player_rect, player, x, y, ataque, sprite_sheet, dano, xp, vida):
        super().__init__()
        self.sheet = sprite_sheet
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)  # A imagem inicial
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem para movimentação
        self.bullet_img = pygame.image.load(os.path.join(assets, 'bullet.png')).convert_alpha()

        self.HP = vida

        self.player = player

        self.xp = xp

        self.rect.topleft = (x,y)
        
        self.dano = dano

        self.speed = 1
        self.player_rect = player_rect
        self.bullet_speed = 5

        # Criar um grupo para gerenciar as balas
        self.balas = pygame.sprite.Group()

        self.mover = not ataque

        self.ataque = False

        self.atacar_ranged = ataque

        self.atacando_melee = False

        self.frame_count = 0  # Contador de frames
        self.sprite_atual = 0  # Contador para alternar entre sprites de animação
        self.direction = 'DOWN'  # Direção de movimento (cima, baixo, esquerda, direita)

        self.frame_change = 10 #Quantidade de frames até a troca de sprite

        self.ivuln = False
        self.iframes = 30
        self.contador_iframes = 0


    def shoot(self,player_rect):
        # if len(self.balas) > 0:
        #     return
        self.player_rect = player_rect
        self.bullet_pos = pygame.math.Vector2(self.rect.center)
        self.target_pos = pygame.math.Vector2(self.player_rect.centerx, self.player_rect.centery)
        self.direction = (self.target_pos - self.bullet_pos).normalize() if self.target_pos != self.bullet_pos else pygame.math.Vector2(0, 0)
        #print(self.player_rect)
        # Cria uma nova bala com direção e posição adequadas
        new_bala = Bala(self.rect.centerx, self.rect.centery, self.direction, self.bullet_speed, self.bullet_img)
        self.balas.add(new_bala)

    def update(self ,dialogo_open):
        self.old_pos_x, self.old_pos_y = self.rect.topleft[0], self.rect.topleft[1]
        if dialogo_open:
            return
        self.frame_count+=1
        # Atualiza as balas
        self.balas.update(dialogo_open)  # Atualiza a posição de todas as balas

        if self.atacar_ranged == True:
            if self.player_rect.x -900 <= self.rect.x or self.player_rect.x + 900 >= self.rect.x:
                if self.player_rect.y -900 <= self.rect.y or self.player_rect.y + 900 >= self.rect.y:
                    self.ataque = True

        if self.mover:
            if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
            
                if self.player_rect.centery > self.rect.centery:
                    self.rect.y +=self.speed
                    self.sheet.action = 2
                elif self.player_rect.centery < self.rect.centery:
                    self.rect.y -=self.speed
                    self.sheet.action = 0
                else:
                    pass

            else:
                if self.player_rect.centerx > self.rect.centerx:
                    self.rect.x +=self.speed
                    self.sheet.action = 3
                elif self.player_rect.centerx < self.rect.centerx:
                    self.rect.x -=self.speed
                    self.sheet.action = 1
                else:
                    pass

        elif self.ataque:
            if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
            
                if self.player_rect.centery > self.rect.centery:
                    self.sheet.action = 10
                elif self.player_rect.centery < self.rect.centery:
                    self.sheet.action = 8
                else:
                    pass

            else:
                if self.player_rect.centerx > self.rect.centerx:
                    self.sheet.action = 11
                elif self.player_rect.centerx < self.rect.centerx:
                    self.sheet.action = 9
                else:
                    pass

        if self.atacando_melee:
            if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
            
                if self.player_rect.centery > self.rect.centery:
                    self.sheet.action = 6
                elif self.player_rect.centery < self.rect.centery:
                    self.sheet.action =4
                else:
                    pass

            else:
                if self.player_rect.centerx > self.rect.centerx:
                    self.sheet.action = 7
                elif self.player_rect.centerx < self.rect.centerx:
                    self.sheet.action = 5
                else:
                    pass

        if self.ivuln == True:
            self.contador_iframes +=1
            if self.contador_iframes == self.iframes:
                self.ivuln = False

        if self.frame_count % self.frame_change == 0:
            self.sheet.update()

        for bala in self.balas:
            if not bala.active:
                self.balas.remove(bala)

    def draw_balas(self, screen, camera):
        for bala in self.balas:
            if bala.active:
                # Ajuste da posição com a câmera
                screen.blit(bala.image, (bala.rect.x - camera.left, bala.rect.y - camera.top))

    def remover_todas_balas(self):
        #print(self.balas.sprites()[0])
        for bala in self.balas:
            self.balas.remove(bala)

    def atacar(self):
        if self.ataque:
            self.shoot(self.player_rect)

    def get_hit(self, dano):
        if self.ivuln == False:
            # print(self.HP)
            self.contador_iframes = 0
            self.HP -= dano
            self.ivuln = True