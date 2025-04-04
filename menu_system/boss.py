import pygame
from inimigo_teste import Inimigo
from balas import Bala
from random import randint

class Boss1(Inimigo):
    def __init__(self, player_rect, player, x, y, ataque, sprite_sheet):
        super().__init__(player_rect, player, x, y, ataque, sprite_sheet)
        self.sheet = sprite_sheet
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)  # A imagem inicial
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem para movimentação
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()

        self.HP = 5

        self.player = player

        self.rect.center = (x,y)

        self.speed = 4
        self.player_rect = player_rect
        self.bullet_speed = 5

        # Criar um grupo para gerenciar as balas
        self.balas = pygame.sprite.Group()

        self.mover = True

        self.gerar_local_a_mover()

        self.ataque = False

        self.atacar_ranged = ataque

        self.modo_ataque = 1

        self.frame_count = 0  # Contador de frames
        self.sprite_atual = 0  # Contador para alternar entre sprites de animação
        self.direction = 'DOWN'  # Direção de movimento (cima, baixo, esquerda, direita)

        self.frame_change = 5 #Quantidade de frames até a troca de sprite

        self.contagem_frames_ataque = 0

        self.contagem_ataques = 0

        self.contagem_tempo_parado = 0

    def gerar_local_a_mover(self):
        self.local_a_mover = [randint(200,800),randint(400,1000)]

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
        self.old_pos_x, self.old_pos_y = self.rect.topleft[0], self.rect.topleft[1]
        if dialogo_open:
            return
        self.frame_count+=1
        # Atualiza as balas
        self.balas.update(dialogo_open)  # Atualiza a posição de todas as balas

        if not self.contagem_ataques >=5:

            if self.mover:
                if self.local_a_mover_y-self.rect.centery != 0 and self.local_a_mover_x-self.rect.centerx < 200:
                
                    if self.local_a_mover_y > self.rect.centery:
                        self.rect.y +=self.speed
                        self.sheet.action = 2
                    elif self.local_a_mover_y < self.rect.centery:
                        self.rect.y -=self.speed
                        self.sheet.action = 0
                    else:
                        pass

                else:
                    if self.local_a_mover_x > self.rect.centerx:
                        self.rect.x +=self.speed
                        self.sheet.action = 3
                    elif self.local_a_mover_x < self.rect.centerx:
                        self.rect.x -=self.speed
                        self.sheet.action = 1
                    else:
                        pass
        if self.ataque:
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
        if self.contagem_ataques >=5:
            print(self.contagem_tempo_parado)
            if self.contagem_tempo_parado < 180:
                self.contagem_tempo_parado+=1
                self.mover = False
                self.ataque = True
                if self.contagem_tempo_parado % 60 == 0:
                    self.atacar()
            else:
                self.mover = True
                self.ataque = False
                self.contagem_tempo_parado = 0
                self.contagem_ataques = 0

        if self.frame_count % self.frame_change == 0:
            self.sheet.update()
        
        while (self.rect.centerx,self.rect.centery)== tuple(self.local_a_mover):
            self.contagem_ataques +=1
            self.ataque = True
            self.atacar()
            self.ataque = False
            self.gerar_local_a_mover()
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

    def remover_todas_balas(self):
        #print(self.balas.sprites()[0])
        for bala in self.balas:
            self.balas.remove(bala)

    def atacar(self):
        if self.ataque:
            self.shoot(self.player_rect)