import pygame

class Inventario:
    def __init__(self, cor_fundo, pos_x, items=[]):
        pygame.init()

        self.Cor_fundo = cor_fundo
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 60)

        self.inventory_open = False
        self.inventory_rect = pygame.Rect(pos_x, 100, 300, 400)
        self.items = items

        self.visible_items = 5

        self.scroll_index = 0

        self.pressed_counter = 0

    def draw_inventory(self, screen):
        pygame.draw.rect(screen, self.Cor_fundo, self.inventory_rect, border_radius=15)

        #print(self.items)

        for i in range(self.visible_items):
            if i >=len(self.items) or len(self.items) == 0:
                return
            x,y = self.inventory_rect.left + 40, self.inventory_rect.top + 40 + i * 80
            text = self
            text = self.font.render(self.items[self.scroll_index + i], True, self.WHITE)
            screen.blit(text, (x, y))

        # for i, item in enumerate(self.items):
        #     x, y = self.inventory_rect.left + 40, self.inventory_rect.top + 40 + i * 80
        #     text = self.font.render(item, True, self.WHITE)
        #     screen.blit(text, (x, y))

    def get_item_at(self, pos):
        for i in range(self.visible_items):
            x,y = self.inventory_rect.left + 40, self.inventory_rect.top + 40 + i * 80
            if i >=len(self.items) or len(self.items) == 0:
                return
            if pygame.Rect(x, y, 300, 80).collidepoint(pos):
                return self.items[self.scroll_index + i]
        return None

    def draw_button(self, screen):
        button_rect = pygame.Rect(screen.get_width() - 150, screen.get_height() - 100, 140, 60)
        pygame.draw.rect(screen, (200, 0, 0), button_rect, border_radius=10)
        text = self.font.render("Abrir", True, self.WHITE)
        screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

    def draw_dragging_item(self, screen, dragging_item):
        text = self.font.render(dragging_item, True, self.WHITE)
        screen.blit(text, pygame.mouse.get_pos())

    def remove(self,item):
        if len(self.items) == 0 or item not in self.items:
            return
        self.items.remove(item)
