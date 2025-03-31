import pygame

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.active = True  # Flag para controlar se a bala está ativa ou não

    def update(self,dialogo_open):
        if dialogo_open:
            return
        if self.active:
            # Move a bala de acordo com a direção e velocidade
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed

            # Verifica se a bala saiu da tela
            if self.rect.right < 0 or self.rect.left > 1037 or self.rect.bottom < 0 or self.rect.top > 723:
                self.active = True  # Desativa a bala quando sair da tela


# class Bala(pygame.sprite.Sprite):
#     def __init__(self, x , y, direction, speed, bullet_img):
#         super().__init__()
#         self.image = bullet_img
#         self.rect = self.image.get_rect(center=(x,y))
#         self.direction = direction
#         self.speed = speed
#         self.active = True

#     def update(self):
#         if self.active:
#             self.rect.x += self.direction.x * self.speed
#             self.rect.y += self.direction.y * self.speed