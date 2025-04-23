import pygame
import random
import math

class RaioSprite(pygame.sprite.Sprite):
    def __init__(self, boss, pos, danger_sheet, strike_sheet,
                 danger_fc, strike_fc, damage):
        super().__init__()
        self.player = boss.player
        self.player_rect = boss.player_rect

        # Spritesheets de aviso e de impacto
        self.danger_sheet = danger_sheet
        self.strike_sheet = strike_sheet

        # Frames por quadro
        self.danger_fc = danger_fc
        self.strike_fc = strike_fc
        self.frame_count = 0

        # Dano e estado
        self.damage = damage
        self.damaged = False
        self.state = 'danger'

        # Configura imagem inicial (aviso)
        self.danger_sheet.index = 0
        self.danger_sheet.update()
        self.image = self.danger_sheet.sheet.subsurface(self.danger_sheet.tile_rect)
        self.rect = self.image.get_rect(center=pos)

        self.alert_pos = pos

    def update(self):
        self.frame_count += 1

        if self.state == 'danger':
            if self.frame_count % self.danger_fc == 0:
                self.danger_sheet.update()
                self.image = self.danger_sheet.sheet.subsurface(self.danger_sheet.tile_rect)
            if self.frame_count >= len(self.danger_sheet.cells[0]) * self.danger_fc:
                # passa para animação de impacto
                self.state = 'strike'
                self.frame_count = 0
                self.strike_sheet.index = 0
                self.strike_sheet.update()
                self.image = self.strike_sheet.sheet.subsurface(self.strike_sheet.tile_rect)

        else:  # state == 'strike'
            if self.frame_count % self.strike_fc == 0:
                self.strike_sheet.update()
                self.image = self.strike_sheet.sheet.subsurface(self.strike_sheet.tile_rect)
            # aplica dano uma vez
            if not self.damaged and self.rect.colliderect(self.player_rect):
                self.player.get_hit(self.damage)
                self.damaged = True
            # remove quando animação acabar
            if self.frame_count >= len(self.strike_sheet.cells[0]) * self.strike_fc:
                self.kill()


class Raios:
    def __init__(self, boss,
                 danger_sheet, strike_sheet,
                 map_min_x, map_max_x, map_min_y, map_max_y,
                 safe_radius=400,
                 min_count=4, max_count=7,
                 wave_cooldown=5000,
                 danger_fc=20, strike_fc=30,
                 damage=5):
        self.boss = boss
        self.group = boss.raios             # usa o sprite.Group definido em Boss2
        self.danger_sheet = danger_sheet
        self.strike_sheet = strike_sheet
        self.min_x, self.max_x = map_min_x, map_max_x
        self.min_y, self.max_y = map_min_y, map_max_y
        self.safe_radius = safe_radius
        self.min_count, self.max_count = min_count, max_count
        self.cooldown = wave_cooldown
        self.danger_fc, self.strike_fc = danger_fc, strike_fc
        self.damage = damage
        self.next_wave = pygame.time.get_ticks() + self.cooldown

    def update(self):
        now = pygame.time.get_ticks()
        if now >= self.next_wave:
            self._spawn_wave()
            self.next_wave = now + self.cooldown
        self.group.update()

    def _spawn_wave(self):
        bx, by = self.boss.rect.center
        for _ in range(random.randint(self.min_count, self.max_count)):
            # gera posição fora da safe zone
            while True:
                x = random.randint(self.min_x, self.max_x)
                y = random.randint(self.min_y, self.max_y)
                if math.hypot(x - bx, y - by) >= self.safe_radius:
                    break
            raio = RaioSprite(
                boss=self.boss,
                pos=(x, y),
                danger_sheet=self.danger_sheet,
                strike_sheet=self.strike_sheet,
                danger_fc=self.danger_fc,
                strike_fc=self.strike_fc,
                damage=self.damage
            )
            self.group.add(raio)