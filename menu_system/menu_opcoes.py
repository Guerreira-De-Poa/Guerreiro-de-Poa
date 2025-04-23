import pygame
import sys

pygame.init()

width, height = 1200, 800

tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pressione 0 para sair")

branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
cinza = (169, 169, 169)
escurecedor = pygame.Surface((1200, 800), pygame.SRCALPHA)
preto_opaco = (0, 0, 0, 80)  # Preto com alpha (transparência)
escurecedor.fill(preto_opaco)

mostrar_quadrado = False  # Começa sem mostrar o quadrado
rodando = True
pausado = False  # Variável para controlar se o jogo está pausado ou não
som_ligado = True  # Controle de som, por padrão está ligado

pos_mouse = (0, 0)
pos_menus = []
mouse_rect = pygame.Rect(pos_mouse[0], pos_mouse[1], 1, 1)

retangulo_transparente = pygame.Rect(981, 127, 35, 42)

controles_img = pygame.image.load("menu_opcoes_imagens/Controles_guerreiro_poa.png")
tamanho_img = pygame.transform.scale(controles_img, (850, 567))
ativar_controles_img = False

clock = pygame.time.Clock()

# Função para desenhar o menu de opções
def desenhar_menu():
    pos_menus.clear()
    fonte = pygame.font.Font(None, 60)
    texto_paused = fonte.render("Jogo Pausado", True, preto)
    tela.blit(texto_paused, (width // 2 - texto_paused.get_width() // 2, height // 2 - 200))

    continuar = pygame.image.load("menu_opcoes_imagens/Continuar.png")
    tela.blit(continuar, (425, 288))
    audio = pygame.image.load("menu_opcoes_imagens/Audio.png")
    tela.blit(audio, (425, 368))
    opcao_controles = pygame.image.load("menu_opcoes_imagens/Controles.png")
    tela.blit(opcao_controles, (425, 448))
    sair = pygame.image.load("menu_opcoes_imagens/Sair.png")
    tela.blit(sair, (425, 528))
    # Opções do menu
    opcoes = [continuar, audio, opcao_controles, sair]
    
    for i, opcao in enumerate(opcoes):
        # texto = fonte.render(opcao, True, preto)
        retangulo_opcoes = pygame.Rect(width // 2 - 175, height // 2 - 112 + i * 80, 350, 74)
        pos_menus.append(retangulo_opcoes)
        # tela.blit(texto, (width // 2 - texto.get_width() // 2, height // 2 - 100 + i * 80))

# Função para lidar com as teclas do menu
def menu_eventos():
    global pausado, som_ligado, rodando
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_0:
                rodando = False
            elif evento.key == pygame.K_ESCAPE:
                pausado = not pausado  # Alterna o estado de pausa
            elif evento.key == pygame.K_DOWN and pausado:
                # Aqui podemos adicionar a navegação entre as opções
                pass
            elif evento.key == pygame.K_UP and pausado:
                # Aqui podemos adicionar a navegação entre as opções
                pass
            elif evento.key == pygame.K_RETURN:
                # if pausado:
                #     # Se a opção "Voltar para o Jogo" for selecionada
                #     pausado = False
                # Se a opção "Som" for selecionada
                if som_ligado:
                    som_ligado = False
                else:
                    som_ligado = True

# Loop principal
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_0:
                rodando = False
            elif evento.key == pygame.K_ESCAPE:
                pausado = not pausado  # Alterna o estado de pausa
                print(pos_menus)
        elif pausado and evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            print(pos_mouse)
            mouse_rect = pygame.Rect(pos_mouse[0], pos_mouse[1], 1, 1)
            if mouse_rect.colliderect(pos_menus[0]):
                pausado = False
            if mouse_rect.colliderect(pos_menus[1]):
                som_ligado = not som_ligado
            if mouse_rect.colliderect(pos_menus[2]):
                ativar_controles_img = True
            if mouse_rect.colliderect(pos_menus[3]):
                rodando = False


    tela.fill(branco)  # limpa a tela

    if pausado:
        pos_mouse = pygame.mouse.get_pos()
        pos_mouse_rect = pygame.Rect(pos_mouse[0], pos_mouse[1], 1, 1)
        tela.blit(escurecedor, (0, 0))
        
        espadinha = pygame.image.load("menu_opcoes_imagens/espadinha_menu_opcoes.png")
        desenhar_menu()  # Exibe o menu de opções quando o jogo estiver pausado
        menu_eventos()


        if ativar_controles_img == True:
            tela.blit(tamanho_img, (width // 2 - 425, height // 2 - 284))
            if mouse_rect.colliderect(retangulo_transparente):
                ativar_controles_img = False
        if pos_mouse_rect.colliderect(pos_menus[0]):
            tela.blit(espadinha, (325, 303))
            continuar = pygame.image.load("menu_opcoes_imagens/Continuar_selecionado.png")
            tela.blit(continuar, (425, 288))
        elif pos_mouse_rect.colliderect(pos_menus[1]):
            tela.blit(espadinha, (325, 383))
            audio = pygame.image.load("menu_opcoes_imagens/Audio_selecionado.png")
            tela.blit(audio, (425, 368))
        elif pos_mouse_rect.colliderect(pos_menus[2]):
            tela.blit(espadinha, (325, 463))
            opcao_controles = pygame.image.load("menu_opcoes_imagens/Controles_selecionado.png")
            tela.blit(opcao_controles, (425, 448))
        elif pos_mouse_rect.colliderect(pos_menus[3]):
            tela.blit(espadinha, (325, 543))
            sair = pygame.image.load("menu_opcoes_imagens/Sair_selecionado.png")
            tela.blit(sair, (425, 528))

    else:
        if mostrar_quadrado:
            pygame.draw.rect(tela, preto, (width // 2 - 300, height // 2 - 200, 600, 400), 0, 30)  # desenha o quadrado

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
