import pygame
from inimigo_teste import Inimigo
from balas import Bala
from random import randint

class Boss1(Inimigo):
    def __init__(self, player_rect, player, x, y, ataque, image):
        super().__init__(player_rect, player, x, y, ataque, image)
        self.image = image
        self.rect = self.image.get_rect()
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()

        self.HP = 10

        self.player = player

        self.rect.center = (x,y)

        self.speed = 4
        self.player_rect = player_rect
        self.bullet_speed = 5

        # Criar um grupo para gerenciar as balas
        self.balas = pygame.sprite.Group()

        self.mover = True

        self.gerar_local_a_mover()

        self.ataque = ataque

        self.modo_ataque = 1

    def gerar_local_a_mover(self):
        self.local_a_mover = [randint(200,800),randint(200,800)]

        for i in range(2):
            if not self.local_a_mover[i] % 2 == 0:
                self.local_a_mover[i]+=1
        while True:
            for i in range(2):
                if not self.local_a_mover[i] % self.speed == 0:
                    self.local_a_mover[i]+=1
            if self.local_a_mover[0] % self.speed == 0 and self.local_a_mover[1] % self.speed == 0:
                #print(self.local_a_mover == False,'\n\n')
                break

        self.local_a_mover_x, self.local_a_mover_y = self.local_a_mover


    def shoot(self,player_rect):
        # if len(self.balas) > 0:
        #     return

        if self.modo_ataque == 1:
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
            if self.local_a_mover_y-self.rect.centery != 0 and self.local_a_mover_x-self.rect.centerx < 200:
            
                if self.local_a_mover_y > self.rect.centery:
                    self.rect.y +=self.speed
                elif self.local_a_mover_y < self.rect.centery:
                    self.rect.y -=self.speed
                else:
                    pass

            else:
                if self.local_a_mover_x > self.rect.centerx:
                    self.rect.x +=self.speed
                elif self.local_a_mover_x < self.rect.centerx:
                    self.rect.x -=self.speed
                else:
                    pass
        
        while (self.rect.centerx,self.rect.centery)== tuple(self.local_a_mover):
            self.gerar_local_a_mover()
            self.atacar()
            # else:
            #     print('(',self.rect.centerx,self.rect.centery,')',self.local_a_mover)

        for bala in self.balas:
            if not bala.active:
                self.balas.remove(bala)

    def draw_balas(self, screen, camera):
        for bala in self.balas:
            if bala.active:
                # Ajuste da posição com a câmera
                screen.blit(bala.image, (bala.rect.x - camera.left, bala.rect.y - camera.top))

    def relocal_a_mover_todas_balas(self):
        #print(self.balas.sprites()[0])
        for bala in self.balas:
            self.balas.remove(bala)

    def atacar(self):
        if self.ataque:
            self.shoot(self.player_rect)