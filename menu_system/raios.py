import pygame

class Raios(pygame.sprite.Sprite):
    def __init__(self, danger_sheet, raio_sheet, pos, frame_duration=5, scale=3):
        super().__init__()
        self.danger_sheet = danger_sheet
        print(danger_sheet)
        self.raio_sheet = raio_sheet
        self.pos = pos
        self.scale = scale

        self.frame_duration = frame_duration
        self.frame_atual = 0
        self.tick = 0
        self.stage = 'danger'

        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        self.danger_frames = self.load_frames(self.danger_sheet)
        self.raio_frames = self.load_frames(self.raio_sheet)

    def load_frames(self, sheet):
        frames = []
        for i in range(sheet.largura_sprite // 64):
            frame = sheet.subsurface((i * 64, 0, 64, 64))
            if self.scale != 1:
                frame = pygame.transform.scale(frame, (int(64*self.scale), int(64*self.scale)))
            frames.append(frame)
        return frames
    
    def update(self):
        self.tick += 1
        if self.stage == 'danger':
            if self.tick % self.frame_duration == 0:
                self.frame_atual += 1
                if self.frame_atual >= len(self.danger_frames):
                    self.frame_atual = 0
                    self.stage = 'raio'
                else:
                    self.image = self.danger_frames[self.frame_atual]

        elif self.stage == 'raio':
            if self.tick % self.frame_duration == 0:
                self.frame_atual += 1
                if self.frame_atual >= len(self.raio_frames):
                    self.kill()
                else:
                    self.image = self.raio_frames[self.frame_atual]