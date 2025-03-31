import pygame
from balas import Bala

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, player_rect, player, x, y, ataque, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()

        self.HP = 10

        self.player = player

        self.rect.topleft = (x,y)

        self.speed = 1
        self.player_rect = player_rect
        self.bullet_speed = 5

        # Criar um grupo para gerenciar as balas
        self.balas = pygame.sprite.Group()

        self.mover = True

        self.ataque = ataque


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
        if dialogo_open:
            return
        # Atualiza as balas
        self.balas.update(dialogo_open)  # Atualiza a posição de todas as balas

        if self.mover:
            if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
            
                if self.player_rect.centery > self.rect.centery:
                    self.rect.y +=self.speed
                elif self.player_rect.centery < self.rect.centery:
                    self.rect.y -=self.speed
                else:
                    pass

            else:
                if self.player_rect.centerx > self.rect.centerx:
                    self.rect.x +=self.speed
                elif self.player_rect.centerx < self.rect.centerx:
                    self.rect.x -=self.speed
                else:
                    pass

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