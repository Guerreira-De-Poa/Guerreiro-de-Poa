import pygame

pygame.init()
screen = pygame.display.set_mode((800, 1000))
clock = pygame.time.Clock()

# Carrega sua spritesheet
spritesheet = pygame.image.load('Tiny_Swords-certo\spritesheet.png').convert_alpha()
spritesheet_rect = spritesheet.get_rect()

# Variáveis para navegação
zoom = 2
offset_x, offset_y = 0, 0
dragging = False
last_mouse_pos = (0, 0)
selected_tile = None
t = 64 # altere conforme o tamanho do tile

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo
                mouse_x, mouse_y = event.pos
                # Calcula a posição na spritesheet considerando o zoom e offset
                tile_x = (mouse_x - offset_x) // (t * zoom)
                tile_y = (mouse_y - offset_y) // (t * zoom)
                if 0 <= tile_x < (spritesheet_rect.width // t) and 0 <= tile_y < (spritesheet_rect.height // t):
                    selected_tile = (tile_x * t, tile_y * t)
                    print(f"Tile selecionado: ({selected_tile[0]}, {selected_tile[1]}) - ID sugerido: {tile_y * (spritesheet_rect.width // t) + tile_x}")
            
            elif event.button == 4:  # Roda do mouse para cima
                zoom = min(zoom + 0.1, 5)
            elif event.button == 5:  # Roda do mouse para baixo
                zoom = max(zoom - 0.1, 1)
        
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - last_mouse_pos[0]
                dy = mouse_y - last_mouse_pos[1]
                offset_x += dx
                offset_y += dy
                last_mouse_pos = (mouse_x, mouse_y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
    
    # Desenha a spritesheet com zoom
    scaled_sheet = pygame.transform.scale(
        spritesheet, 
        (int(spritesheet_rect.width * zoom), int(spritesheet_rect.height * zoom))
    )
    screen.fill((40, 40, 40))
    screen.blit(scaled_sheet, (offset_x, offset_y))
    
    # Desenha grade
    for x in range(0, int(spritesheet_rect.width * zoom), int(t * zoom)):
        pygame.draw.line(screen, (255, 255, 255, 100), (x + offset_x, offset_y), 
                         (x + offset_x, offset_y + spritesheet_rect.height * zoom), 1)
    for y in range(0, int(spritesheet_rect.height * zoom), int(t * zoom)):
        pygame.draw.line(screen, (255, 255, 255, 100), (offset_x, y + offset_y), 
                         (offset_x + spritesheet_rect.width * zoom, y + offset_y), 1)
    
    # Destaca tile selecionado
    if selected_tile:
        highlight_rect = pygame.Rect(
            selected_tile[0] * zoom + offset_x,
            selected_tile[1] * zoom + offset_y,
            t * zoom, t * zoom)
        pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 2)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()