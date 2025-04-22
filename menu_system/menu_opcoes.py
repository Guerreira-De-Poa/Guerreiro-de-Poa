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

mostrar_quadrado = False  # Começa sem mostrar o quadrado
rodando = True
pausado = False  # Variável para controlar se o jogo está pausado ou não
som_ligado = True  # Controle de som, por padrão está ligado

# Função para desenhar o menu de opções
def desenhar_menu():
    fonte = pygame.font.Font(None, 60)
    texto_paused = fonte.render("Jogo Pausado", True, preto)
    tela.blit(texto_paused, (width // 2 - texto_paused.get_width() // 2, height // 2 - 200))

    # Opções do menu
    opcoes = ["Voltar para o Jogo", "Som: " + ("Ligado" if som_ligado else "Desligado"), "Controles", "Sair"]
    
    for i, opcao in enumerate(opcoes):
        texto = fonte.render(opcao, True, preto)
        pygame.draw.rect(tela, cinza, (width // 2 - 200, height // 2 - 100 + i * 80, 400, 60), 0, 20)
        tela.blit(texto, (width // 2 - texto.get_width() // 2, height // 2 - 100 + i * 80))

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
                if pausado:
                    # Se a opção "Voltar para o Jogo" for selecionada
                    pausado = False
                # Se a opção "Som" for selecionada
                elif som_ligado:
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

    tela.fill(branco)  # limpa a tela

    if pausado:
        desenhar_menu()  # Exibe o menu de opções quando o jogo estiver pausado
    else:
        if mostrar_quadrado:
            pygame.draw.rect(tela, preto, (width // 2 - 300, height // 2 - 200, 600, 400), 0, 30)  # desenha o quadrado

    pygame.display.flip()

pygame.quit()
sys.exit()
