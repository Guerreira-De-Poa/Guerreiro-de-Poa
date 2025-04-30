import pygame
import random
import math

class RaioSprite(pygame.sprite.Sprite):
    def __init__(self, boss, pos,
                 danger_sheet, strike_sheet,
                 danger_fc, strike_fc,
                 damage,
                 alert_scale=4.0,
                 strike_scale=4.0):
        super().__init__()
        # referências ao jogador
        self.player = boss.player
        self.player_rect = boss.player_rect

        # configuração de sprites e timings
        self.danger_sheet = danger_sheet
        self.strike_sheet = strike_sheet
        self.danger_fc = danger_fc
        self.strike_fc = strike_fc

        # dano e estado
        self.damage = damage
        self.damaged = False
        self.state = 'danger'
        self.frame_count = 0

        # posição base e fatores de escala
        self.alert_pos    = pos
        self.alert_scale  = alert_scale
        self.strike_scale = strike_scale

        self.spawn_time = pygame.time.get_ticks()
        # inicializa imagem e rect
        self._set_image(self.danger_sheet, self.alert_scale)

        self.hit_rect = self.rect.copy()

    def _set_image(self, sheet, scale):
        # avança animação
        sheet.update()
        frame = sheet.sheet.subsurface(sheet.tile_rect)
        # escala
        w,h = frame.get_size()
        frame = pygame.transform.scale(frame, (int(w*scale), int(h*scale)))
        # align bottom-center to original alert bottom
        alert_frame = self.danger_sheet.sheet.subsurface(self.danger_sheet.tile_rect)
        alert_rect  = alert_frame.get_rect(center=self.alert_pos)
        cx = self.alert_pos[0]
        bottom = alert_rect.bottom
        # define image e rect
        self.image = frame
        self.rect  = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.bottom  = bottom

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time

        # duração total de cada fase em ms
        alert_ms  = len(self.danger_sheet.cells[self.danger_sheet.action]) * self.danger_fc
        strike_ms = len(self.strike_sheet.cells[self.strike_sheet.action]) * self.strike_fc

        if elapsed < alert_ms:
            # fase de warning
            sheet = self.danger_sheet
            idx   = min(elapsed // self.danger_fc,
                        len(sheet.cells[sheet.action]) - 1)
            rect  = sheet.cells[sheet.action][idx]
            surf  = sheet.sheet.subsurface(rect)
            # escalona e alinha bottom como antes...
        elif elapsed < alert_ms + strike_ms:
            # fase de strike
            sheet = self.strike_sheet
            t     = elapsed - alert_ms
            idx   = min(t // self.strike_fc,
                        len(sheet.cells[sheet.action]) - 1)
            rect  = sheet.cells[sheet.action][idx]
            surf  = sheet.sheet.subsurface(rect)
            # escalona, alinha bottom e aplica dano se for o primeiro frame...
            if not self.damaged and self.hit_rect.colliderect(self.player_rect):
                self.player.get_hit(self.damage)
                self.damaged = True
        else:
            self.kill()
            return

        scale = self.alert_scale if elapsed < alert_ms else self.strike_scale
        w, h = surf.get_size()
        surf_scaled = pygame.transform.scale(surf, (int(w*scale), int(h*scale)))

        # 2) define imagem
        self.image = surf_scaled

        # 3) reposiciona rect pelo bottom-center
        #    precisamos do bottom do alerta original:
        alert_frame = self.danger_sheet.sheet.subsurface(
            self.danger_sheet.cells[self.danger_sheet.action][0]
        )
        alert_rect  = alert_frame.get_rect(center=self.alert_pos)
        cx, bottom = alert_rect.centerx, alert_rect.bottom

        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.bottom  = bottom

class Raios:
    def __init__(self, boss,
                 danger_sheet, strike_sheet,
                 map_min_x, map_max_x,
                 map_min_y, map_max_y,
                 safe_radius=40,
                 min_count=4, max_count=7,
                 wave_cooldown=5000,
                 danger_fc=20, strike_fc=30,
                 damage=5,
                 alert_scale=4.0,
                 strike_scale=4.0,
                 min_spacing=500):
        self.boss = boss
        self.group = boss.raios
        self.danger_sheet = danger_sheet
        self.strike_sheet = strike_sheet
        self.min_x, self.max_x = map_min_x, map_max_x
        self.min_y, self.max_y = map_min_y, map_max_y
        self.safe_radius = safe_radius
        self.min_count, self.max_count = min_count, max_count
        self.cooldown = wave_cooldown
        self.danger_fc, self.strike_fc = danger_fc, strike_fc
        self.damage = damage
        self.alert_scale = alert_scale
        self.strike_scale = strike_scale
        self.min_spacing = min_spacing
        self.next_wave = pygame.time.get_ticks() + self.cooldown

    def update(self,f):
        if f:
            return
        now = pygame.time.get_ticks()
        if now >= self.next_wave:
            self._spawn_wave()
            self.next_wave = now + self.cooldown
        self.group.update()

    def _spawn_wave(self):
        bx,by = self.boss.rect.center
        count = random.randint(self.min_count, self.max_count)
        positions = []
        while len(positions) < count:
            x = random.randint(self.min_x, self.max_x)
            y = random.randint(self.min_y, self.max_y)
            if math.hypot(x-bx, y-by) < self.safe_radius:
                continue
            if any(math.hypot(x-px, y-py) < self.min_spacing for px,py in positions):
                continue
            positions.append((x,y))
        for pos in positions:
            raio = RaioSprite(
                boss=self.boss,
                pos=pos,
                danger_sheet=self.danger_sheet,
                strike_sheet=self.strike_sheet,
                danger_fc=self.danger_fc,
                strike_fc=self.strike_fc,
                damage=self.damage,
                alert_scale=self.alert_scale,
                strike_scale=self.strike_scale
            )
            self.group.add(raio)