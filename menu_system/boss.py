import pygame
from inimigo_teste import Inimigo
from balas import Bala
from raios import *
from spritesheet_explicada import SpriteSheet
from random import randint

class Boss1(Inimigo):
    def __init__(self, player_rect, player, x, y, ataque, sprite_sheet, dano, xp, vida):
        super().__init__(player_rect, player, x, y, ataque, sprite_sheet, dano, xp, vida)
        self.sheet = sprite_sheet
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)  # A imagem inicial
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem para movimentação
        self.bullet_img = pygame.image.load('boss_agua(Slash).png').convert_alpha()

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

        self.ivuln = False
        self.iframes = 30
        self.contador_iframes = 0

        self.morto = False
        self.morte_counter = 0

    def gerar_local_a_mover(self):
        self.local_a_mover = [randint(1200,1600),randint(400,1000)]

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
        if dialogo_open or self.morto:
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
                    self.sheet.action = 6
                elif self.player_rect.centery < self.rect.centery:
                    self.sheet.action = 4
                else:
                    pass

            else:
                if self.player_rect.centerx > self.rect.centerx:
                    self.sheet.action = 7
                elif self.player_rect.centerx < self.rect.centerx:
                    self.sheet.action = 5
                else:
                    pass

            if self.atacando_melee:
                if self.player_rect.centery-self.rect.centery != 0 and self.player_rect.centerx-self.rect.centerx < 200:
                
                    if self.player_rect.centery > self.rect.centery:
                        self.sheet.action = 6
                    elif self.player_rect.centery < self.rect.centery:
                        self.sheet.action = 4
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
            #print(self.contagem_tempo_parado)
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
        
        if (self.rect.centerx,self.rect.centery)== tuple(self.local_a_mover):
            self.contagem_ataques +=1
            self.ataque = True
            self.atacar()
            self.ataque = False
            self.gerar_local_a_mover()
            # else:
            #     print('(',self.rect.centerx,self.rect.centery,')',self.local_a_mover)

        if self.ivuln == True:
            self.contador_iframes +=1
            if self.contador_iframes == self.iframes:
                self.ivuln = False

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
            self.contador_iframes = 0
            self.HP -= dano
            self.ivuln = True

class Boss2(Inimigo):
    def __init__(self, player_rect, player, x, y, ataque, sprite_sheet, dano, xp, vida):
        super().__init__(player_rect, player, x, y, ataque, sprite_sheet, dano, xp, vida)
        self.sheet = sprite_sheet

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(center=(x, y))

        self.HP = vida
        self.player = player
        self.player_rect = player_rect
        self.speed = 3
        self.pulo_speed = self.speed * 3

        self.raios = pygame.sprite.Group()
        danger_ss = SpriteSheet('DangerAnimation.png', 0, 0, 32, 32, 0, [6], (0,0,0), False)
        strike_ss = SpriteSheet('thunderSpriteSheet.png', 0, 0, 128, 256, 0, [5], (0,0,0), False)
        self.raios_controller = Raios(
            boss=self,
            danger_sheet=danger_ss,
            strike_sheet=strike_ss,
            map_min_x=20, map_max_x=1600,
            map_min_y=40, map_max_y=1200,
            safe_radius=500,
            min_count=4, max_count=7,
            wave_cooldown=5000,
            danger_fc=180,
            strike_fc=180,
            damage=50,
            alert_scale=5.0,
            strike_scale=2.8,
            min_spacing=300
        )

        self.mover = True
        self.gerar_local_a_mover()
        self.ataque = False
        self.pulando = False
        self.cooldown = False
        self.modo_ataque = 1
        self.frame_count = 0
        self.frame_change = 10
        self.contagem_ataques = 0
        self.acumulo_pulos = 0
        self.ivuln = False
        self.iframes = 30
        self.contador_iframes = 0
        self.contagem_tempo_parado = 0
        self.dx = 0
        self.dy = 0

    def gerar_local_a_mover(self):
        self.local_a_mover = [randint(120,2120),randint(200,1000)]

        for i in range(2):
            if not self.local_a_mover[i] % 2 == 0:
                self.local_a_mover[i] += 1
        while True:
            for i in range(2):
                if not self.local_a_mover[i] % self.speed == 0:
                    self.local_a_mover[i] += 1
            if self.local_a_mover[0] % self.speed == 0 and self.local_a_mover[1] % self.speed == 0:
                break
        self.local_a_mover_x, self.local_a_mover_y = self.local_a_mover

        self.prioridade = random.choice(['x', 'y'])


    def pulo_inicio(self, player_rect):
        self.player_rect = player_rect
        self.pos_inicial = pygame.math.Vector2(self.rect.center)
        self.pos_alvo = pygame.math.Vector2(player_rect.center)
        self.direction = (self.pos_alvo - self.pos_inicial).normalize()
        self.pulo_dist_restante = (self.pos_alvo - self.pos_inicial).length()
        if not (100 < self.pulo_dist_restante < 500):
            self.acumulo_pulos += 1
            self.contagem_ataques = 0
            self.cooldown = True
            return  # sem zerar contagem_ataques

        self.phase = 0
        self.phase_timer = 0

        self.dx, self.dy = self.direction.x, self.direction.y
        if abs(self.dy) < abs(self.dx):
            self.sheet.action = 21 if self.dx > 0 else 19
        else:
            self.sheet.action = 20 if self.dy > 0 else 18

        self.sheet.index = 0
        self.sheet.update()

        self.pulando = True
    
    def update(self, dialogo_open):

        self.raios_controller.update()
        if dialogo_open:
            return
        
        self.old_pos_x, self.old_pos_y = self.rect.x, self.rect.y

        # Tratamento do pulo em fases
        if self.pulando:
            self.phase_timer += 1

            if self.phase == 0:
                if self.phase_timer >= 10:
                    self.phase = 1
                    self.phase_timer = 0
                    self.sheet.update()   # passa para quadro 1 (agachar)
            elif self.phase == 1:
                if self.phase_timer >= 20:
                    self.phase = 2
                    self.phase_timer = 0
                    self.sheet.update()   # passa para quadro 2 (pronto)
            elif self.phase == 2:
                # mantém quadro 2 travado e já inicia o movimento
                self.pulo_durante()
                if self.phase_timer >= 15:
                    self.phase = 3
                    self.phase_timer = 0
                    self.sheet.update()   # passa para quadro 3 (meio)
            elif self.phase == 3:
                # continua no quadro 3 e movendo
                self.pulo_durante()
                if self.phase_timer >= 15:
                    self.phase = 4
                    self.phase_timer = 0
                    self.sheet.update()   # passa para quadro 4 (descida)
            elif self.phase == 4:
                # mantém quadro 4 e continua movimentando até finalizar
                self.pulo_durante()
                # quando terminar, durante_pulo() chama self.fim_pulo()
            return  # sai do update enquanto estiver pulando

        elif self.cooldown:
            self.contagem_tempo_parado += 1
            if self.contagem_tempo_parado >= 30:
                self.cooldown = False
                self.contagem_tempo_parado = 0
                self.mover = True
                self.gerar_local_a_mover()
            return  # ainda não anda nem ataca neste frame

        if self.contagem_ataques >= 1:
            self.mover = False
            self.ataque = True
            self.contagem_ataques = 0
            self.acumulo_pulos += 1
            self.pulo_inicio(self.player_rect)
            return  # só no próximo frame o pulo será executado

        elif self.mover:
            self.dx = self.local_a_mover_x - self.rect.centerx
            self.dy = self.local_a_mover_y - self.rect.centery

            if self.rect.centerx != self.local_a_mover_x:
                distancia_x = self.local_a_mover_x - self.rect.centerx
                if abs(distancia_x) <= self.speed:
                    self.rect.centerx = self.local_a_mover_x
                else:
                    step = self.speed if distancia_x > 0 else -self.speed
                    self.rect.centerx += step
                self.sheet.action = 3 if distancia_x > 0 else 1

            elif self.rect.centery != self.local_a_mover_y:
                distancia_y = self.local_a_mover_y - self.rect.centery
                if abs(distancia_y) <= self.speed:
                    self.rect.centery = self.local_a_mover_y
                else:
                    step = self.speed if distancia_y > 0 else -self.speed
                    self.rect.centery += step
                self.sheet.action = 2 if distancia_y > 0 else 0
            
            if pygame.math.Vector2(self.rect.center).distance_to((self.local_a_mover_x, self.local_a_mover_y)) <= self.speed:
                self.rect.center = (self.local_a_mover_x, self.local_a_mover_y)
                self.mover = False
                self.cooldown = True
                self.contagem_ataques += 1
                return
            
        self.frame_count += 1
        if self.frame_count % self.frame_change == 0:
            self.sheet.update()

        if self.ivuln:
            self.contador_iframes += 1
            if self.contador_iframes >= self.iframes:
                self.ivuln = False

    def draw_raios(self, screen, camera):
        for raio in self.raios:
            screen.blit(raio.image, (raio.rect.x - camera.left, raio.rect.y - camera.top))

    def remover_todos_raios(self):
        for raio in self.raios:
            self.raios.remove(raio)

    def atacar(self):
        if self.ataque and not self.pulando:
            self.pulo_inicio(self.player_rect)

    def get_hit(self, dano):
        if self.ivuln == False:
            self.contador_iframes = 0
            self.HP -= dano
            self.ivuln = True
            self.player.HP += dano

    def pulo_durante(self):
        if self.pulo_dist_restante > self.pulo_speed:
            desloc = self.direction * self.pulo_speed
            self.rect.centerx += desloc.x
            self.rect.centery += desloc.y
            self.pulo_dist_restante -= self.pulo_speed
        else:
            desloc = self.direction * self.pulo_dist_restante
            self.rect.centerx += desloc.x
            self.rect.centery += desloc.y
            self.pulo_fim()  # encerra pulo e entra em cooldown


    def pulo_fim(self):
        self.pulando = False
        self.range_pulo = self.rect.inflate(self.rect.width, self.rect.height)
        if self.player_rect.colliderect(self.range_pulo):
            self.player.get_hit(5)
        if self.acumulo_pulos > 0:
            self.pulo_inicio(self.player_rect)
            self.acumulo_pulos -= 1
        else:
            self.ataque = False
            self.cooldown = True
            self.contagem_tempo_parado = 0