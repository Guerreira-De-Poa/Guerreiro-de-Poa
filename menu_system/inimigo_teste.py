import pygame
from balas import Bala

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, player_rect, player, x, y, ataque, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.bullet_img = pygame.image.load('../../bullet.png').convert_alpha()

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
        self.balas.update()  # Atualiza a posição de todas as balas

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

# class Inimigo(pygame.sprite.Sprite):
#     def __init__(self, *groups, player_rect,screen,camera):
#         super().__init__(*groups)
#         self.image = pygame.image.load('enemy_sprite/Biomech Dragon Splice.png')
#         self.rect = self.image.get_rect() 
#         self.bullet_img = pygame.image.load("bullet.png").convert_alpha()
        
#         self.speed = 2
#         self.player_rect = player_rect
#         self.bullet_speed = 5

#         self.balas = pygame.sprite.Group()

#         self.bullet_pos = pygame.math.Vector2(0, 0)
#         self.target_pos = pygame.math.Vector2(self.player_rect.centerx, self.player_rect.centery)
#         self.direction = (self.target_pos - self.bullet_pos).normalize()

#         self.rect.y -=1

#         self.i = 0
#         self.camera = camera
#         self.screen = screen

#     def update(self):
#         #print(f'Player rect:{self.player_rect.y}\nSelf.rect:{self.rect.x} {self.rect.y}\n')
#         #print(f'Self.CENTER: {self.rect.centerx} {self.rect.centery}\n\n')
#         #print(self.rect.centery == self.rect.center[1])
#         if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
        
#             if self.player_rect.centery > self.rect.centery:
#                 self.rect.y +=self.speed
#             elif self.player_rect.centery < self.rect.centery:
#                 self.rect.y -=self.speed
#             else:
#                 pass

#         else:
#             if self.player_rect.centerx > self.rect.centerx:
#                 self.rect.x +=self.speed
#             elif self.player_rect.centerx < self.rect.centerx:
#                 self.rect.x -=self.speed
#             else:
#                 pass

#         self.balas.update()
#         # self.i+=1
#         # if self.i == 60:
#         #     self.shoot()

#     def shoot(self):
#         new_bala = Bala(self.rect.centerx, self.rect.centery, self.direction, self.bullet_speed, self.bullet_img)
#         self.balas.add(new_bala)

#     def draw_balas(self):
#         for bala in self.balas:
#             if bala.active:
#                 self.screen.blit(bala.image, (bala.rect.x - self.camera.left, bala.rect.y - self.camera.top))

#         print(len(self.balas))


#         # # Atualiza a posição da bala na direção calculada
#         # self.bullet_pos += self.direction * self.bullet_speed
        
#         # # Ajusta a posição da bala considerando a câmera
#         # self.screen.blit(self.bullet_img, (self.bullet_pos.x - self.camera.left, self.bullet_pos.y - self.camera.top))

